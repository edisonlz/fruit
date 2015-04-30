#coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType
from app.content.lib.model_util import ModelUtil
from sub_channel import IpadSubChannel, IphoneSubChannel, AndroidSubChannel
from base_video import BaseVideo
from base.youkuapi.playlist import PlaylistApi


class IpadSubChannelItem(BaseVideo):
    subchannel = models.ForeignKey(IpadSubChannel, related_name='subchannelItem', verbose_name='子频道视频')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
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
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details', 'game_list', 'game_download', \
               'game_details', 'live_broadcast', 'video_with_game_list', 'video_with_game_details', 'game_gift', 'user'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('ipad'), types)

    def check_copyright(self, video_info, device_type='pad'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'pad')


class IphoneSubChannelVideo(BaseVideo):
    subchannel = models.ForeignKey(IphoneSubChannel, related_name='subchannelVideo', verbose_name='子频道视频')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
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
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details', \
               'game_download', 'game_gift', 'user', 'live_broadcast'
               # 'game_list', 'game_details', \

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('iphone'), types)

    def check_copyright(self, video_info, device_type='mobile'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'mobile')


class AndroidSubChannelVideo(BaseVideo):
    subchannel = models.ForeignKey(AndroidSubChannel, related_name='subchannelVideo', verbose_name='子频道视频')
    video_list_id = models.IntegerField(verbose_name='VIDEO LIST ID', default=0)

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
            'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list',\
               'video_with_game_download', 'user', 'video_list', 'live_broadcast'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('android'), types)

    def check_copyright(self, video_info, device_type='mobile'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'mobile')

    def add_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.save()

    def update_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.save()

    def details_for_interface(self,image_type):
        video_information = {
            'content_id' : self.video_id,
            'content_type' : str(self.video_type),
            'title' : self.title,
            'image' : getattr(self,image_type),
            'intro' : self.intro,
            #:playlist_videoid : self.playlist_videoid,
            'url' : self.url,
            'pv' : self.first_episode_video_pv,
            'second_title' : self.subtitle,
            'paid' : self.paid
        }
        video_information['playlist_videoid'] = ''
        if self.video_type == 3:
            info = PlaylistApi.get_playlist_info(self.video_id)
            first_episode_video_id = info.get('id') or self.first_episode_video_id or ''
            video_information['playlist_videoid'] = first_episode_video_id
        return video_information
