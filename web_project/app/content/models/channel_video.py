#coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType
from app.content.lib.model_util import ModelUtil
from channel import AndroidChannel,IphoneChannel,IpadChannel
from base_video import BaseVideo

class AndroidChannelVideo(BaseVideo):
    channel = models.ForeignKey(AndroidChannel, related_name='channelVideo', verbose_name='频道视频')
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
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details', 'game_details',\
               'game_list', 'video_with_game_download', 'user', 'live_broadcast', 'game_download', 'game_gift'

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

    def update_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.save()

    def content_hash(self, contents):
        results = []
        for content in contents:
            #这个条件分支用不上了
            # if content.class == CmsAndroidContent && content.paid_video_id.present?
            #     paid_video = CmsPaidVideo.find(content.paid_video_id)
            #     result = {
            #     :content_id=> paid_video.video_type == 'show' ? paid_video.show_id : paid_video.video_id,
            #     :content_type => paid_video.video_type == 'show' ? '2' : '1',
            #     :title => paid_video.title,
            #     :image => paid_video.image_1,
            #     :is_paid_video => 1,
            #     :paid => 1
            # }else
            result = {
                'content_id': content.video_id,
                'content_type': content.video_type,
                'title': content.title,
                'image': content.h_image,
                'pv': content.pv,
                'paid': content.paid
            }

            results.append(result)
        return results



class IphoneChannelVideo(BaseVideo):
    channel = models.ForeignKey(IphoneChannel, related_name='channelVideo', verbose_name='频道视频')
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
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details', 'game_details',\
               'game_list', 'video_with_game_download', 'user', 'video_list', 'live_broadcast','game_download', 'game_gift'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('iphone'), types)

    def check_copyright(self, video_info, device_type='mobile'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'mobile')

class IpadChannelVideo(BaseVideo):
    channel = models.ForeignKey(IpadChannel, related_name='channelVideo', verbose_name='频道视频')
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
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details', 'game_details',\
               'game_list', 'video_with_game_download', 'user', 'video_list', 'live_broadcast','game_download', 'game_gift'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('ipad'), types)

    def check_copyright(self, video_info, device_type='mobile'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'mobile')
