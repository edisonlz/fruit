# coding=utf8

from django.db import models
from sub_channel import IpadSubChannel, IphoneSubChannel, AndroidSubChannel
from fixed_position_video import AndroidFixedPositionVideo
from platform import Status, SubChannelType, VideoType, Platform
from wi_cache.base import CachingManager


class SubChannelModule(models.Model):
    objects = CachingManager()

    title = models.CharField(max_length=100, verbose_name='标题', default='')
    module_type = models.IntegerField(verbose_name='模块类型', default=0)  # 0普通模块/1轮播图模块
    position = models.IntegerField(verbose_name='位置', default=0)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0,
                                max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=u'更新时间')
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        # verbose_name = u"iPad频道"
        # verbose_name_plural = verbose_name
        abstract = True
        app_label = "content"


class IpadSubChannelModule(SubChannelModule):
    objects = CachingManager()
    subchannel = models.ForeignKey(IpadSubChannel, related_name=u'module', verbose_name=u'子频道')
    video_count = models.IntegerField(verbose_name=u'个数', max_length=3, default=0)
    for_membership = models.IntegerField(verbose_name=u"是否是会员专享", default=0, max_length=2)  #0否/1是

    @property
    def is_headline_module(self):
        return self.module_type == 1


        # class Meta:
        #     verbose_name = u"iPad子频道模块"
        #     verbose_name_plural = verbose_name
        #     app_label = "content"


class IphoneSubChannelModuleV4(SubChannelModule):
    UNIT_TYPES = (
        ('horizontal_twos', u"横图模板（2视频/单元）"),
        ('vertical_twos', u"竖图模板（2视频/单元）"),
        ('vertical_threes', u"竖图模板（3视频/单元）"),
        ('huge_image', u"单张大图（1视频/单元）"),
        ('slider_images', u"轮播图"),
    )
    objects = CachingManager()

    subchannel = models.ForeignKey(IphoneSubChannel, related_name='module_v4', verbose_name=u'子频道')
    unit_type_collection = models.CharField(max_length=255, verbose_name=u'UnitType集合', default='')
    slider_video_count = models.IntegerField(verbose_name=u'轮播图模块的视频个数', default=4)

    # class Meta:
    #     # db_table = 'content_iphonesubchannelmodulev4'
    #     verbose_name = u"iPhone子频道v4.x模块"
    #     verbose_name_plural = verbose_name
    #     app_label = "content"


class IphoneSubChannelModule(SubChannelModule):
    subchannel = models.ForeignKey(IphoneSubChannel, related_name='module', verbose_name='子频道')
    iphone_video_count = models.IntegerField(verbose_name=u'iphone模块内视频个数', default=1)
    ipad_video_count = models.IntegerField(verbose_name=u'ipad模块内视频个数', default=1)

    @property
    def is_headline_module(self):
        return self.module_type == 1

        # class Meta:
        #     # db_table = 'content_iphonesubchannelmodulev4'
        #     verbose_name = u"iPhone子频道v3.x模块"
        #     verbose_name_plural = verbose_name
        #     app_label = "content"


# android 子频道模块内按照单元布局，与ipad/iphone不一样
class AndroidSubChannelModule(SubChannelModule):
    MODULE_TYPES = {
        0: u'普通抽屉',
        1: u'轮播图抽屉',
        2: u'游戏抽屉',
        3: u'游戏横幅抽屉',
        # 4 : u'今日精选抽屉'
    }
    subchannel = models.ForeignKey(AndroidSubChannel, related_name='module', verbose_name='子频道')
    unit_type_collection = models.CharField(max_length=255,
                                            verbose_name=u'unit_types')  # unit_type的集合，以逗号分割。目前的unit_type包括：slider_images/quarters/halfs
    jump_type = models.CharField(max_length=100,
                                 verbose_name=u'标题跳转类型')  # 点击抽屉title后的跳转类型.no_jump:无跳转；by_sub_channel：跳转到子频道;by_filter:跳转到('全部'子频道的)筛选结果
    sub_channel_id_for_link = models.IntegerField(verbose_name=u'跳转的子频道id', default=0)  # 点击模块标题要跳转到的子频道的id
    filter_for_link = models.CharField(max_length=255, verbose_name=u'标题跳转筛选条件')  # 点击模块标题要跳转到的'全部子频道'的筛选条件
    slider_video_count = models.IntegerField(verbose_name=u'轮播视频个数', default=5)
    phone_one_unit = models.IntegerField(verbose_name=u'phone只用一个单元', default=0)  # is_phone_use_only_one_unit? 0否/1是

    @classmethod
    def get_subchannel_box_types(cls,channel):
        '''
        是否为游戏频道下的子频道 决定抽屉类型
        '''
        if channel.is_game_channel:
            type_hash = {
                0: u'普通抽屉',
                1: u'轮播图抽屉',
                2: u'游戏抽屉',
                3: u'游戏横幅抽屉',
            }
        else:
            type_hash = {
                0: u'普通抽屉',
                1: u'轮播图抽屉',
            }
        return type_hash
    def get_video_types(self, channel):
        '''
        channel 应该是views里获取的当前module所属的channel
        '''
        if channel.is_game_channel:
            if self.is_game_module:
                types = ['video_with_game_details']
            elif self.is_game_banner_module:
                types = ['game_gift', 'game_list', 'game_download', 'game_details']
            else:
                types = ['video_with_game_details', 'game_gift', 'game_list', 'game_download', 'game_details', 'video',
                         'url']
        else:
            types = ['video_with_game_details', 'game_gift', 'game_list', 'game_download', 'game_details', 'video',
                         'url']
        return VideoType.platformization(Platform.to_i('android'), types)


    def details_for_interface(self, options={}):
        print "== options in CmsAndroidSubChannelModule#details_for_interface:"
        print options
        information = {
            'units': self.units_and_videos_informations(options),
            'is_phone_use_only_one_unit': self.phone_one_unit,
            'module_id': self.id
        }
        if 'slider_images' not in self.unit_type_collection:
            information['title'] = self.title
            #点击title后的跳转：
            #如果有filter字段，前端认为跳转到filter
            #如果sub_channel_id_for_link不为null，前端认为跳转到子频道
            #否则无跳转
        if self.jump_type == 'no_jump':
            information['sub_channel_id_for_link'] = None
        else:
            information['sub_channel_id_for_link'] = self.sub_channel_id_for_link
            if self.jump_type == 'by_filter':
                information['filter'] = self.filter_for_link
        return information

    @property
    def is_headline_module(self):
        return self.module_type == 1

    @property
    def is_game_module(self):
        return self.module_type == 2

    @property
    def is_game_banner_module(self):
        return self.module_type == 3

    def set_image_for_client_for_video(self, videos, unit_type):
        videos_count = len(videos) if videos else 0
        if unit_type == 'slider_images':
            videos_changed_count = self.slider_video_count or 6
            image_column = 's_image'
        elif unit_type == 'halfs':
            videos_changed_count = 2
            image_column = 'v_image'
        elif unit_type == 'quarters':
            videos_changed_count = 4
            image_column = 'h_image'
        else:
            videos_changed_count = 4
            image_column = 'h_image'
        if videos_count < videos_changed_count:
            videos_changed_count = videos_count
        if videos_changed_count > 0:
            for video in videos[0:videos_changed_count]:
                image_for_client = getattr(video, image_column, '') or ''
                setattr(video, 'image_for_client', image_for_client)
        return videos_changed_count

    def set_image_for_client_and_unit_sequence_for_videos(self, videos):
        unit_types = self.unit_type_collection.split(",") or []
        video_list = list(videos) if videos else []
        for index, count in enumerate(self.unit_video_count_collection()):
            if int(count) < 1:
                del unit_types[0]
            else:
                videos_changed_count = self.set_image_for_client_for_video(video_list, unit_types[index])
                for video in video_list[0:videos_changed_count]:
                    setattr(video, 'unit_sequence', index + 1)
                del video_list[0:videos_changed_count]
        return videos


    def unit_video_count_collection(self):
        if self.unit_type_collection:
            unit_type_arr = self.unit_type_collection.split(',')
            return [self.get_unit_video_count_by_unit_type(unit_type) for unit_type in unit_type_arr]
        else:
            return []

            #根据module下每个unit（单元）类型 返回相应类型的视频个数

    def get_unit_video_count_by_unit_type(self, unit_type):
        if unit_type == 'quarters':
            unit_count = 4
        elif unit_type == 'halfs':
            unit_count = 2
        elif unit_type == 'slider_images':
            unit_count = self.slider_video_count or 6
        elif unit_type == 'game_banner':
            unit_count = 1
        else:
            unit_count = 0
        return unit_count


    def units_and_videos_informations(self, options={}):
        videos = self.moduleVideo.filter(state=1, is_delete=False)
        if options['ver'] < '4.1.4':
            videos = videos.extra(where=["video_type not in (7,8,9)"]).extra(
                where=["attached_game_type is null or attached_game_type = ''"])
        if options['ver'] < '4.3':
            videos = videos.extra(where=["video_type not in (14,15,16)"])
        videos = videos.order_by('-position')
        print "== options[:is_show_game_information]: #{options[:is_show_game_information]}"
        print options
        if options['is_show_game']:
            videos = AndroidFixedPositionVideo.replace_position_fixed_videos(videos,
                                                               {'subchannel_type': SubChannelType.to_i('editable_box'),
                                                                'module_id': self.id,
                                                                'ver': options['ver']
                                                               })
        videos = self.set_image_for_client_and_unit_sequence_for_videos(videos)
        unit_types = self.unit_type_collection.split(",") or []
        units_information = []
        for index, count in enumerate(self.unit_video_count_collection()):
            #TODO: 这里强行调整了游戏模块的layout,但这里的逻辑可能放到页面上控制会更好
            layout = unit_types[index]
            #layout = 'game_quarters' if layout == 'quarters' && self.module_type == MODULE_TYPE_OF_GAME
            unit_information = {'layout': layout}
            final_videos = [video for video in videos if video.unit_sequence == index + 1]
            unit_information['contents'] = [video.details_for_interface for video in final_videos]
            units_information.append(unit_information)
        return units_information

    def need_video_count(self):
        if not self.unit_type_collection:
            return 0
        res = 0
        for unit_type in self.unit_type_collection.split(','):
            if unit_type == 'quarters':
                res += 4
            elif unit_type == 'halfs':
                res += 2
            elif unit_type == 'slider_images':
                res += self.slider_video_count
        return res


