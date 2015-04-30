#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from app.content.models import VideoType, VideoListModule, AndroidGame, IosGame
from base.youkuapi.video import VideoApi
from base.youkuapi.show import ShowApi
from base.youkuapi.playlist import PlaylistApi
from base.youkuapi.parse_item import parse_item_id_and_type
from django.db.models import Max
from bitfield import BitField
# import logging
from app.content.lib.image_helper import ImageHelper
from app.content.lib.model_util import ModelUtil
import re


class BaseVideo(models.Model):
    STATUS = ((0, u'关闭'),
              (1, u'开启'), )
    PAY_TYPE_LIST = ['vod', 'mon']
    objects = CachingManager()

    STATUS_CLOSE = 0
    STATUS_OPEN = 1

    STATUS_RECORD_NORMAL = 0
    STATUS_RECORD_DELETE = 1

    #platform-universal
    title = models.CharField(max_length=100, verbose_name='标题', default='')
    intro = models.CharField(max_length=100, verbose_name='腰封', default='')

    #description = models.CharField(max_length=512, verbose_name='描述', null=True, blank=True)
    subtitle = models.CharField(max_length=100, verbose_name='子标题', default='')
    v_image = models.CharField(max_length=255, verbose_name='竖图', default='')
    h_image = models.CharField(max_length=255, verbose_name='横图', default='')
    s_image = models.CharField(max_length=255, verbose_name='轮播图', default='')

    # video/show/playlist/user/live_broadcast类型将id放到了video_id
    video_id = models.CharField(max_length=100, verbose_name='Item ID', default='')
    video_type = models.IntegerField(verbose_name='视频类型', default=0, db_index=True)

    paid = models.IntegerField(verbose_name='是否付费（是／否）', choices=STATUS, default=0)
    #pay_type = models.CharField(max_length=255, verbose_name='付费类型', default='')
    pay_type = BitField(flags=('vod', 'mon',), default=0)
    #usage:https://github.com/disqus/django-bitfield
    #TODO: IntegerField的值无法由default指定
    has_copyright = models.IntegerField(verbose_name='是否有版权（是／否）', default=0)

    url = models.CharField(max_length=255, verbose_name='URL', default='')
    first_episode_video_id = models.CharField(max_length=100, verbose_name='专辑第一视频ID', default='')
    first_episode_video_pv = models.IntegerField(verbose_name='专辑第一视频PV', default=0)

    position = models.IntegerField(verbose_name='位置', default=0)
    state = models.IntegerField(verbose_name='状态（开／关）', choices=STATUS, default=0)
    image_size = models.IntegerField(verbose_name=u'图片大小类型', default=0)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    #game relative; (android iphone)platform
    game_id = models.CharField(max_length=100, verbose_name='GAME ID', default='')
    attached_game_type = models.CharField(max_length=100, verbose_name='游戏附加类型', default='')
    game_page_id = models.CharField(max_length=100, verbose_name='游戏运营页 ID', default='')

    #(android iphone)platform
    pgc_uid = models.CharField(max_length=100, verbose_name='PGC UID', default='')
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        abstract = True
        app_label = "content"

    #should be called in children instance
    def platform(self):
        return self.box.platform

    #should be called in children instance
    def box_type(self):
        return self.box.box_type

    def copyright_for_view(self):
        if VideoType.to_s(self.video_type) in ['video', 'show']:
            if self.has_copyright == 1:
                return '有'
            else:
                return '无'
        else:
            return '-'

    @property
    def url_to_play(self):
        if self.video_id:
            if self.video_type == VideoType.to_i('video'):
                return "http://v.youku.com/v_show/id_{video_id}.html".format(video_id=self.video_id)
            elif self.video_type == VideoType.to_i('show'):
                return "http://www.youku.com/show_page/id_z{video_id}.html".format(video_id=self.video_id)
            elif self.video_type == VideoType.to_i('playlist'):
                return "http://www.youku.com/playlist_show/id_{video_id}.html".format(video_id=self.video_id)
            else:
                return ''
        else:
            return ''

    def set_video_pay_type(self, pay_type_list):
        '''
            pay_type_list: ["mon",'vod']
            由 list转为对应 int
            vod 0000 0001
            mon 0000 0010
        '''
        mon_flag = 1 if 'mon' in pay_type_list else 0
        vod_flag = 1 if 'vod' in pay_type_list else 0
        return (mon_flag << 1) + vod_flag

    def get_video_pay_type(self):
        '''
        由self.pay_type  BitHandler 转为 字符串
        BaseVideo.PAY_TYPE_LIST = ['vod','mon']
        0000 0001 vod
        0000 0010 mon
        0000 0011 vod + mon
        '''
        pay_type_list = []
        for index, pay_type_str in enumerate(BaseVideo.PAY_TYPE_LIST):
            temp_pay_type = self.pay_type >> index
            if int(temp_pay_type) % 2:  #必须先转int   ps:这里出错没有抛异常 待查
                pay_type_list.append(pay_type_str)
        return ';'.join(pay_type_list)

    def pay_type_for_view(self):
        if VideoType.to_s(self.video_type) in ['video', 'show', 'live_broadcast']:
            if self.paid == 0:
                return '免费'
            else:
                result = '付费'
                if self.pay_type:
                    result += '(' + self.get_video_pay_type() + ')'
                return result
        else:
            return '-'

    def video_type_for_view(self):
        if self.attached_game_type:
            if self.attached_game_type == 'game_details':
                return VideoType.to_s(self.video_type) + '+game_details'
            elif self.attached_game_type == 'game_download':
                return VideoType.to_s(self.video_type) + '+game_download'
            elif self.attached_game_type == 'game_list':
                return VideoType.to_s(self.video_type) + '+game_list'
            else:
                return 'unknown'
        else:
            return VideoType.to_s(self.video_type)

    def is_mon_pay_video(self):
        return self.paid == 1 and (int(self.pay_type >> 1) % 2)

    def is_vod_pay_video(self):
        return self.paid == 1 and (int(self.pay_type) % 2)

    @property
    def need_game_original_id(self):
        return self.video_type in [7, 8, 9] or self.attached_game_type

    @property
    def need_game_page_id(self):
        return self.video_type in [14, 15, 16]

    #should override in subclass if different with this
    def add_url_type_fields(self, params):
        self.url = params.get("url", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get('s_image', '')
        # DO NOT SAVE HERE
        # self.save()

    #should override in subclass if different with this
    def add_video_type_fields(self, params):
        #TODO: FIXIT
        video_url = params.get("url")
        video_id_and_type = parse_item_id_and_type(video_url)
        if video_id_and_type:
            self.video_id, video_type_name = video_id_and_type
            self.video_type = VideoType.to_i(video_type_name)
            if (video_type_name == "video"):
                info = VideoApi.get_video_info(self.video_id)

                self.title = info.get('title', '')
                self.h_image = ImageHelper.convert_to_448_252(info.get('thumburl_v2', ''))
                self.paid = info.get('paid', 0)
                self.pay_type = self.set_video_pay_type(info.get('pay_type', []))
                self.has_copyright = self.check_copyright(info)
            elif (video_type_name == "show"):
                info = ShowApi.get_show_info(self.video_id)
                self.title = info.get('showname', '')
                # show的横图暂时取show的横图，ruby版本中取得是show的第一个视频的横图
                self.h_image = ImageHelper.convert_to_448_252(info.get('show_thumburl', ''))
                self.v_image = ImageHelper.convert_to_200_300(info.get('show_vthumburl', ''))
                #intro/subtitle字段暂时不用保存，后期可以考虑将其作为备选提示给编辑
                # self.intro = info.get("deschead", '')
                # self.subtitle = info.get('showsubtitle', '')
                self.paid = info.get('paid', 0)
                self.pay_type = self.set_video_pay_type(info.get('pay_type', []))
                self.has_copyright = self.check_copyright(info)
            elif (video_type_name == "playlist"):
                info = PlaylistApi.get_playlist_info(self.video_id)
                self.title = info.get('title', '')
                self.first_episode_video_id = info.get('id', '')
                # thumbnail已经是448x252的了
                self.h_image = info.get('thumbnail', '')
            else:
                raise Exception('video_type not match')
                # DO NOT SAVE HERE
                # self.save()

    #should override in subclass if different with this
    def add_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.game_id = 0
        # DO NOT SAVE HERE
        # self.save()

    def check_copyright(self, info, device='mobile'):
        return ModelUtil.check_copyright(self.video_type, info, device)

    #should override in subclass if different with this
    def add_game_gift_type_fields(self, params):
        self.game_page_id = params.get("game_page_id", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        # self.save()

    #should override in subclass if different with this
    def add_user_type_fields(self, params):
        #TODO: user type need ['user_id'] or [save 'user_id' by 'user_link']
        self.video_id = params.get("video_id", '')
        if not self.video_id:
            raise Exception('live_broadcast_id cannot be blank')
            # DO NOT SAVE HERE
            # self.save()

    #should override in subclass if different to this
    def add_live_broadcast_type_fields(self, params):
        self.video_id = params.get('video_id')
        if not self.video_id:
            raise Exception('live_broadcast_id cannot be blank')
            # DO NOT SAVE HERE
            # self.save()

    #should override in subclass if different to this
    def add_game_details_type_fields(self, params, mock_video_fields=False):
        platform = self.get_platform()
        if platform == 'ipad' or platform == 'iphone':
            game_class = IosGame
        elif platform == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_details')

        new_game = game_class.create_or_update(params)
        self.game_id = new_game.id
        if not mock_video_fields:
            self.title = params.get("title", '')
            self.h_image = params.get("h_image", '')

    #should override in subclass if different to this
    def add_game_download_type_fields(self, params):
        platform = self.get_platform()
        if platform == 'ipad' or platform == 'iphone':
            game_class = IosGame
        elif platform == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')

        new_game = game_class.create_or_update(params)
        self.game_id = new_game.id
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get('s_image', '')
        # DO NOT SAVE HERE
        # self.save()
        #TODO: add other video_relatived info

    def update_game_download_type_fields(self, params):
        platform = self.get_platform()
        if platform == 'ipad' or platform == 'iphone':
            game_class = IosGame
        elif platform == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')

        game = game_class.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def add_video_with_game_details_type_fields(self, params):
        self.add_video_type_fields(params)
        self.attached_game_type = 'game_details'
        self.add_game_details_type_fields(params)
        # self.save()

    def get_platform(self):
        lower_class_name = self.__class__.__name__.lower()
        if re.compile('ipad').search(lower_class_name):
            return 'ipad'
        elif re.compile('iphone').search(lower_class_name):
            return 'iphone'
        elif re.compile('android').search(lower_class_name):
            return 'android'
        elif re.compile('win').search(lower_class_name):
            return 'win_phone'
        else:
            raise Exception('unknown platform')

    def update_url_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def update_video_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def update_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.save()

    def add_game_details_type_fields(self, params):
        platform = self.get_platform()
        if platform == 'ipad' or platform == 'iphone':
            game_class = IosGame
        elif platform == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')
        game = game_class.create_or_update(params)
        self.game_id = game.id
        if not self.attached_game_type:  # 判断游戏详情类型，避免视频＋游戏类型覆盖视频的title和h_image
            self.title = params.get('title')
            self.h_image = params.get('h_image')
            # DO NOT SAVE HERE
            # self.save()

    def update_game_details_type_fields(self, params):
        platform = self.get_platform()
        if platform == 'ipad' or platform == 'iphone':
            game_class = IosGame
        elif platform == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')
        game = game_class.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def update_live_broadcast_type_fields(self, params):
        self.live_broadcast_url = params.get("live_broadcast_url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.s_image = params.get("s_image", "")
        self.h_image = params.get("h_image", "")
        self.live_broadcast_bg_image_3_5 = params.get("live_broadcast_bg_image_3_5", "")
        self.live_broadcast_bg_image_4 = params.get("live_broadcast_bg_image_4", "")
        self.live_broadcast_bg_image_4_7 = params.get("live_broadcast_bg_image_4_7", "")
        self.live_broadcast_bg_image_5_5 = params.get("live_broadcast_bg_image_5_5", "")
        self.paid = params.get("paid", "")
        self.save()

    def update_game_gift_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def update_user_type_fields(self, params):
        self.video_id = params.get("video_id", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", "")
        self.save()

    def add_position(self, box_pk):
        video_sets = self.__class__.objects.defer('position').filter(box_id=box_pk)
        if not video_sets:
            current_box_max_position = 0
        else:
            current_box_max_position = video_sets.order_by("-position")[0].position + 1
        self.position = current_box_max_position


    #@classmethod
    #def get_max_position(cls):
    #    return cls.objects.aggregate(Max('position'))['position__max'] or 0

    @classmethod
    def get_max_box_position(cls, target_box):
        return cls.objects.filter(box_id=target_box.id).aggregate(Max('position'))['position__max'] or 0

    @classmethod
    def get_max_sub_channel_position(cls, target_sub_channel):
        return cls.objects.filter(sub_channel_id=target_sub_channel.id).aggregate(Max('position'))['position__max'] or 0

    @classmethod
    def get_max_sub_channel_module_position(cls, target_sub_channel_module):
        return cls.objects.filter(sub_channel_module_id=target_sub_channel_module.id).aggregate(Max('position'))[
                   'position__max'] or 0

    @classmethod
    def get_publish_videos(cls, box):
        video_count = box.publish_video_count()

        box_opened_videos = cls.objects.filter(box_id=int(box.id),
                                               is_delete=cls.STATUS_RECORD_NORMAL,
                                               state=cls.STATUS_OPEN)

        box_videos = box_opened_videos.order_by('-position')[:video_count]
        return box_videos

    @classmethod
    def get_exist_video_in_box(cls, video_type, video_class, box, box_id_column, checked_video):
        """
        根据视频类型获取盒子中已经存在的视频
        """
        existed_video = None
        existed_videos = None
        if video_type in ['video', 'show', 'playlist', 'live_broadcast', 'user']:
            if checked_video.attached_game_type:
                existed_videos = video_class.objects. \
                    filter(**{box_id_column: box.id}). \
                    filter(video_id=checked_video.video_id,
                           video_type=checked_video.video_type,
                           game_id=checked_video.game_id,
                           attached_game_type=checked_video.attached_game_type,
                           is_delete=cls.STATUS_RECORD_NORMAL)
            else:
                existed_videos = video_class.objects. \
                    filter(**{box_id_column: box.id}). \
                    filter(video_type=checked_video.video_type,
                           video_id=checked_video.video_id,
                           is_delete=cls.STATUS_RECORD_NORMAL)
        elif video_type == 'url':
            existed_videos = video_class.objects. \
                filter(**{box_id_column: box.id}). \
                filter(video_type=checked_video.video_type,
                       url=checked_video.url, is_delete=cls.STATUS_RECORD_NORMAL)
        elif video_type == 'video_list':
            existed_videos = video_class.objects. \
                filter(**{box_id_column: box.id}). \
                filter(video_type=checked_video.video_type,
                       video_list_id=checked_video.video_list_id
                       , is_delete=cls.STATUS_RECORD_NORMAL)
        elif video_type in ['game_list', 'game_details', 'game_download']:
            existed_videos = video_class.objects. \
                filter(**{box_id_column: box.id}). \
                filter(video_type=checked_video.video_type,
                       game_id=checked_video.game_id,
                       is_delete=cls.STATUS_RECORD_NORMAL)
        elif video_type in ['game_gift', 'game_album', 'game_activity']:
            existed_videos = video_class.objects. \
                filter(**{box_id_column: box.id}). \
                filter(video_type=checked_video.video_type,
                       game_page_id=checked_video.game_page_id
                       , is_delete=cls.STATUS_RECORD_NORMAL)
        if existed_videos:
            existed_video = existed_videos[0]
        return existed_video

    @classmethod
    def get_exist_home_video(cls, video_type, publish_video_class, box, box_video):
        return cls.get_exist_video_in_box(video_type, publish_video_class, box, 'box_id', box_video)

    @classmethod
    def get_exists_sub_channel_video(cls, video_type, publish_video_class, sub_channel, sub_channel_video):
        return cls.get_exist_video_in_box(video_type, publish_video_class, sub_channel, 'sub_channel_id',
                                          sub_channel_video)

    @classmethod
    def get_exist_sub_channel_module_video(cls, video_type, publish_video_class, sub_channel_module,
                                           sub_channel_module_video):
        return cls.get_exist_video_in_box(video_type, publish_video_class, sub_channel_module, 'sub_channel_module_id',
                                          sub_channel_module_video)

    @classmethod
    def tighten_position_in_box(cls, box, max_position_for_each_box):
        """
        收缩视频位置：重新将所有视频的position调整为从1到n
        """
        current_max_position = cls.get_max_box_position(box)
        if current_max_position > max_position_for_each_box:
            all_videos = cls.objects.filter(box_id=box.id).order_by("position")
            for index, video in enumerate(all_videos):
                video.position = index + 1
                video.save()

    @classmethod
    def remove_redundant_videos_in_box(cls, box, max_video_count_for_each_box, box_id_column='box_id'):
        """
        删除多余视频：如果视频个数大于max_video_count, 删除多余的视频
        调用该函数的时机：
          * 首页资源池视频: 新增视频
          * 首页抽屉视频: 新增视频, 从资源池同步
          * 首页发布视频: 从抽屉视频发布
        """
        redundant_video_count = cls.objects.filter(**{box_id_column: box.id}).count() - max_video_count_for_each_box

        if redundant_video_count > 0:
            delete_videos = cls.objects.filter(**{box_id_column: box.id}).order_by('position')[:redundant_video_count]
            for video in delete_videos:
                video.delete()

    @classmethod
    def get_page_show_v_types(cls, v_type_and_name_list):
        mock_after_list = []
        for item in v_type_and_name_list:
            if item['name'] not in ['show', 'playlist']:
                mock_after_list.append(item)
        return mock_after_list