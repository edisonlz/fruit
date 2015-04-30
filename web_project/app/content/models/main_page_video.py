#coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType, AndroidVideoListModule, AndroidGame
from app.content.models import HomeBox
from app.content.lib.model_util import ModelUtil

from base_video import BaseVideo


class AndroidBoxVideo(BaseVideo):
    box = models.ForeignKey(HomeBox, verbose_name='模块 ID')
    video_list_id = models.IntegerField(verbose_name='VIDEO LIST ID', default=0)
    channel_id = models.IntegerField(verbose_name=u'编辑推荐的channel id', default=0) #好像没有用？
    pid = models.CharField(max_length=100, verbose_name='针对特定pid的视频', null=True, blank=True)

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
            'live_broadcast',
            'video_with_game_list', 'video_with_game_download', 'video_with_game_details',
            'game_gift',  #'game_album', 'game_activity',
            # 'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ('show', 'playlist', 'video_with_game_list', 'video_with_game_download')

    @classmethod
    def video_types(cls, mock=False,is_game_box=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
            if not is_game_box:
                types.remove('video_with_game_details')
                types.remove('game_gift')
        return VideoType.platformization(Platform.to_i('android'), types)

    def check_video_type(self, mock=False):
        return AndroidBoxVideo.video_types(mock).has_key(self.video_type)

    #重写base_video中的方法
    def update_video_type_fields(self, params):
        #调用父类的update_video_type_fields()
        super(AndroidBoxVideo, self).update_video_type_fields(params)
        self.pgc_uid = params.get("pgc_uid", "")
        self.save()

    def update_live_broadcast_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.paid = params.get("paid", "")
        self.save()

    def add_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")

    def update_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.save()




class IpadBoxVideo(BaseVideo):
    box = models.ForeignKey(HomeBox, verbose_name='模块 ID')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            # 'game_list', 'game_download', 'game_details',
            'live_broadcast',
            # 'video_with_game_list',
            # 'video_with_game_download',
            # 'video_with_game_details',
            # 'game_gift',  #'game_album', 'game_activity',
            # 'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ('show', 'playlist', 'video_with_game_list', 'video_with_game_details')

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('ipad'), types)

    def check_video_type(self, mock=False):
        return IpadBoxVideo.video_types(mock).has_key(self.video_type)

    def check_copyright(self, video_info, device_type='pad'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'pad')

    def update_live_broadcast_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.s_image = params.get("s_image", "")
        self.h_image = params.get("h_image", "")
        self.paid = params.get("paid", "")
        self.save()


class IphoneBoxVideo(BaseVideo):
    box = models.ForeignKey(HomeBox, verbose_name='模块 ID')
    live_broadcast_url = models.CharField(max_length=255, verbose_name='直播url', default='')
    live_broadcast_bg_image_3_5 = models.CharField(max_length=255, verbose_name='聊天背景图(3.5)', default='')
    live_broadcast_bg_image_4 = models.CharField(max_length=255, verbose_name='聊天背景图(4)', default='')
    live_broadcast_bg_image_4_7 = models.CharField(max_length=255, verbose_name='聊天背景图(4.7)', default='')
    live_broadcast_bg_image_5_5 = models.CharField(max_length=255, verbose_name='聊天背景图(5.5)', default='')


    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list',
            # 'game_download',
            'game_details',
            'live_broadcast',
            'video_with_game_list',
            # 'video_with_game_download',
            'video_with_game_details',
            'game_gift',  #'game_album', 'game_activity',
            'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ('show', 'playlist', 'video_with_game_list', 'video_with_game_details', 'game_download')

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('iphone'), types)

    def check_video_type(self, mock=False):
        return IphoneBoxVideo.video_types(mock).has_key(self.video_type)

    #重写base_video中的方法
    def update_video_type_fields(self, params):
        #调用父类的update_video_type_fields()
        super(IphoneBoxVideo, self).update_video_type_fields(params)
        self.pgc_uid = params.get("pgc_uid", "")
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


class WinPhoneBoxVideo(BaseVideo):
    """
    由于业务调整，我们不对win平台的数据进行管理，模块内的视频数据从iphone获取
    """
    box = models.ForeignKey(HomeBox, verbose_name='模块 ID')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return ( 'video', 'show', 'playlist', 'url', )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ( 'show', 'playlist', )

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('win_phone'), types)

    def check_video_type(self, mock=False):
        return WinPhoneBoxVideo.video_types(mock).has_key(self.video_type)

