#coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType
from app.content.models import AndroidVideoListModule
from base_video import BaseVideo
from app.content.lib.model_util import ModelUtil


class AndroidVideoListVideo(BaseVideo):
    '''
    视频列表里面的视频
    '''
    module = models.ForeignKey(AndroidVideoListModule, verbose_name='模块 ID')
    pv = models.IntegerField(verbose_name='PV', default=0) #这里ruby版是编辑手填的

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'url',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ('show','playlist')

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('android'), types)

    def check_copyright(self, video_info, device_type='mobile'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'mobile')
