# coding=utf8

from django.db import models
from channel import IpadChannel, IphoneChannel, AndroidChannel
from platform import Status, SubChannelType, Imgtype
from fixed_position_video import AndroidFixedPositionVideo
from wi_cache.base import CachingManager
from brand_module import BrandModule
from wi_model_util.imodel import get_object_or_none

TYPES = (
    (1, u'抽屉'),
    (2, u'列表'),
    (3, u'筛选条件'),
)

TYPES_DICT = {
    1: u'editable_box',
    2: u'editable_video_list',
    3: u'filter',
}

IMAGE_TYPES = (
    (1, u'横图'),
    (2, u'竖图'),
)

IMAGE_TYPE_DICT = {
    1: u'vertical',
    2: u'horizontal',
}

AREA = [
    (0, u'全部'),
    (1, u'大陆'),
    (2, u'香港'),
    (3, u'台湾'),
    (4, u'韩国'),
    (5, u'美国'),
    (6, u'英国'),
    (7, u'法国'),
    (8, u'泰国'),
    (9, u'新加坡'),
]

VIDEO_TYPE = [
    (0, u'全部'),
    (1, u'古装'),
    (2, u'武侠'),
    (3, u'警匪'),
    (4, u'军事'),
    (5, u'神话'),
    (6, u'科幻'),
    (7, u'悬疑'),
    (8, u'历史'),
    (9, u'儿童'),
    (10, u'农村'),
    (11, u'都市'),
    (12, u'家庭'),
    (13, u'搞笑'),
    (14, u'偶像'),
    (15, u'言情'),
    (16, u'时装'),
    (17, u'优酷出品'),
]

YEAR = [
    (0, u'全部'),
    (1, u'2014'),
    (2, u'2013'),
    (3, u'2012'),
    (4, u'2011'),
    (5, u'2010'),
    (6, u'2009'),
    (7, u'2008'),
    (8, u'2007'),
    (9, u'2006'),
    (10, u'2005'),
    (11, u'2004'),
    (12, u'2003'),
    (13, u'2002'),
    (14, u'2001'),
    (15, u'90年代'),
    (16, u'80年代'),
    (17, u'70年代'),
    (18, u'60年代'),
    (19, u'50年代'),
    (20, u'50年代以前'),
]


class SubChannel(models.Model):
    objects = CachingManager()

    title = models.CharField(max_length=100, verbose_name='标题')
    type = models.IntegerField(verbose_name='类型', choices=TYPES, default=1)
    image_type = models.IntegerField(verbose_name='图片类型', choices=IMAGE_TYPES, default=1)
    video_count = models.IntegerField(verbose_name='个数', max_length=3, default=0)  #列表类型子频道中返回给接口的视频个数
    position = models.IntegerField(verbose_name='位置', default=0)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, max_length=2)
    filter_collection = models.CharField(max_length=255, verbose_name='筛选条件',
                                         default='')  #以;做类分割，以:做值分割。e.g.  area:韩国;tv_gener:古装
    is_show_filters = models.BooleanField(verbose_name='是否露出筛选条件', default=False)  #类型为filter时 是否漏出筛选条件
    #generic fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    # 下面的两个控制同时对 模块和列表 类型的视频生效
    MaxVideoCountInSubChannel = 300
    MaxPositionInBox = 1000000

    class Meta:
        # verbose_name = u"iPad子频道"
        # verbose_name_plural = verbose_name
        abstract = True
        app_label = "content"

    @property
    def get_type(self):
        return TYPES_DICT.get(self.type)

    @property
    def is_editable_box(self):
        return self.type == 1

    @property
    def is_editable_video_list(self):
        return self.type == 2

    @property
    def is_filter(self):
        return self.type == 3


    @property
    def get_image_state(self):
        return IMAGE_TYPE_DICT.get(self.image_type)

    def filter_collection_to_dict(self):
        '''
        将filter字段变成字典的形式
        e.g.: u'area:韩国;tv_genre:言情;releaseyear:' => {'area':'韩国', 'tv_genre':'言情', 'releaseyear':''}
        '''
        if not self.filter_collection:
            return {}
        result = {}
        for sub_filter in self.filter_collection.split('|'):
            k, v = sub_filter.split(':')
            result[k] = v or ''
        return result

    def location_information(self, brand_module, platform, channel_entity_id=None):
        channels = None
        channel_entity = None
        sub_channel_entity = None
        target_sub_channel_id = 0
        state_for_platform = 0
        sub_channel_id = 0
        sub_channel = None
        if platform == 'android':
            channels = AndroidChannel.objects.filter(is_delete=0, content_type=1, show_type=1).order_by('-position')
            target_sub_channel_id = brand_module.subchannel_id_of_android
            channel_entity = AndroidChannel
            sub_channel_entity = AndroidSubChannel
            state_for_platform = brand_module.state_for_android
        elif platform == 'iphone':
            channels = IphoneChannel.objects.filter(is_delete=0, show_type=1).order_by('-position')
            target_sub_channel_id = brand_module.subchannel_id_of_iphone
            channel_entity = IphoneChannel
            sub_channel_entity = IphoneSubChannel
            state_for_platform = brand_module.state_for_iphone
        elif platform == 'ipad':
            channels = IpadChannel.objects.filter(is_delete=0, show_type=1).order_by('-position')
            target_sub_channel_id = brand_module.subchannel_id_of_ipad
            channel_entity = IpadChannel
            sub_channel_entity = IpadSubChannel
            state_for_platform = brand_module.state_for_ipad
        else:
            raise ValueError('params["platform"] is not valid')

        if not channel_entity_id and target_sub_channel_id > 0:
            sub_channel = get_object_or_none(sub_channel_entity, pk=target_sub_channel_id)
            sub_channel_id = sub_channel.id
            channel = get_object_or_none(channel_entity, pk=sub_channel.channel_id)
        else:
            channel = get_object_or_none(channel_entity, pk=channel_entity_id) if channel_entity_id else None
            channel = channels[0] if not channel else None
        sub_channels = sub_channel_entity.objects.filter(is_delete=0, type=1, channel_id=channel.id).order_by(
            '-position')
        location_is_valid = (target_sub_channel_id > 0) and (state_for_platform == 1) and (
        sub_channel_id == target_sub_channel_id)

        return {
            'channels': channels,
            'channel': channel,
            'sub_channels': sub_channels,
            'sub_channel': sub_channel,
            'location_is_valid': location_is_valid
        }


class IpadSubChannel(SubChannel):
    channel = models.ForeignKey(IpadChannel, related_name='subchannel', verbose_name='频道')

    is_choiceness = models.IntegerField(verbose_name=u"是否精选子频道", default=0, max_length=2)  #0否/1是
    for_membership = models.IntegerField(verbose_name=u"是否是会员专享", default=0, max_length=2)  #0否/1是


class IphoneSubChannel(SubChannel):
    channel = models.ForeignKey(IphoneChannel, related_name='subchannel', verbose_name='频道')
    is_choiceness = models.IntegerField(verbose_name=u"是否精选子频道", default=0, max_length=2)  # 0 否/1是
    module_with_units = models.IntegerField(verbose_name=u"是否v4.0模板", default=0,
                                            max_length=2)  # 是否使用v4.0模板(每个模块有多个单元了)? 0否/1是


class AndroidSubChannel(SubChannel):
    channel = models.ForeignKey(AndroidChannel, related_name='subchannel', verbose_name='频道')
    highlight = models.IntegerField(verbose_name=u"是否高亮", default=0, max_length=2)  #0否/1是

    @property
    def interface_information(self):
        result = {
            'title': self.title,
            'sub_channel_type': SubChannelType.to_s(self.type),
            'sub_channel_id': self.id,
            'image_state': Imgtype.to_s(self.image_type),
            'highlight': self.highlight,
            'display_type': 'list'
        }
        if self.type == SubChannelType.to_i('filter'):
            result['filter'] = self.filter_collection
        return result

    def details_for_interface(self, options):
        current_options = {'ver': '3.0', 'is_show_game': False}
        current_options.update(options)
        #子频道类型为人工运营模块
        if self.type == SubChannelType.to_i('editable_box'):
            sub_channel_modules = self.module.filter(state=1, is_delete=False).order_by('-position')
            print 'in sub_channel_details edit_box'
            print sub_channel_modules
            print options['ver']
            if current_options['ver'] < '4.1.3':
                #4.1.3之前版本
                sub_channel_modules = sub_channel_modules.extra(
                    where=['module_type not in (2,3)'])  #2 type of game  3 type of game_banner
                print 'after'
                if self.channel.cid == 99:  #游戏频道 cid
                    sub_channel_modules = sub_channel_modules.exclude(module_type=1)
            sub_channel_modules = sub_channel_modules.order_by('-position')
            result = {
                'sub_channel_title': self.title,
                'sub_channel_type': SubChannelType.to_s(self.type),
                'modules': [the_module.details_for_interface(options) for the_module in sub_channel_modules]
            }
            if options['ver'] >= '4.1.3':
                from sub_channel_module_tag import AndroidSubChannelModuleTag

                result['game_entrances'] = \
                    AndroidSubChannelModuleTag.game_entrances_for_interface(self.id, self.channel.cid)
            if options['ver'] >= '4.0':
                has_brands_headline = BrandModule.sub_channel_has_brands_headline('android', self)
                result['has_brands_headline'] = 1 if has_brands_headline else 0
            return result
        elif self.type == SubChannelType.to_i('editable_video_list'):
            #android 列表类型(editable_video_list)的子频道 所包含的视频存储在AndroidSubChannelVideo
            subchannel_videos = self.subchannelVideo.filter(is_delete=0).order_by('-position')
            # 旧版本靠这个标识(show_game_information)来控制是否加入固定位置视频
            if options['is_show_game']:
                subchannel_videos = AndroidFixedPositionVideo.replace_position_fixed_videos(subchannel_videos,
                  {'subchannel_type': SubChannelType.to_i('editable_video_list'),
                   'ver': options['ver'], 'subchannel_id': self.id,})
            #限制最大输出视频个数
            default_video_limit = 50
            if len(subchannel_videos) > default_video_limit:
                subchannel_videos = subchannel_videos[0:50]
            if self.image_type == 1:
                #标识横图还是竖图 决定输出视频的图片类型是横图还是竖图
                image_type = 'h_image'
                image_type_for_interface = 'horizontal'  #这里是为了与ruby版接口的返回数据文案一致
            else:
                image_type = 'v_image'
                image_type_for_interface = 'vertical'
            #获取视频详情数组
            video_details_array = []
            for video in subchannel_videos:
                temp = AndroidSubChannel.detail_of_list_type_video(video, image_type)
                video_details_array.append(temp)

            result = {
                'sub_channel_title': self.title,
                'image_state': image_type_for_interface,
                'sub_channel_type': SubChannelType.to_s(self.type),
                'results': video_details_array
            }
            return result
        else:
            return {}

    @staticmethod
    def detail_of_list_type_video(video, image_type):
        video_information = {
            'content_id' : video.video_id,
            'content_type' : str(video.video_type),
            'title' : video.title,
            'image' : getattr(video,image_type),
            'intro' : video.intro,
            #:playlist_videoid : self.playlist_videoid,
            'url' : video.url,
            'pv' : video.first_episode_video_pv,
            'second_title' : video.subtitle,
            'paid' : video.paid
        }
        video_information['playlist_videoid'] = ''
        if video.video_type == 3:
            video_information['playlist_videoid'] = video.first_episode_video_id
        return video_information
