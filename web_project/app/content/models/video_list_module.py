# coding=utf-8
from django.db import models
from platform import Status
from wi_cache.base import CachingManager


class VideoListModule(models.Model):
    '''
    a. 如果支持视频列表，这里是视频列表对应的（隐藏的父级层次）父节点
    b. 让一个（非视频列表里的）视频成为video_list类型视频：
       1. video.video_type = VideoType.to_i('video_list')
       2. video.video_list_id = VideoListModule.instance.id
    '''
    objects = CachingManager()
    title = models.CharField(max_length=100, verbose_name='标题', default='')
    position = models.IntegerField(verbose_name='位置', default=0)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0,
                                max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=u'更新时间')
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        abstract = True
        app_label = "content"


class AndroidVideoListModule(VideoListModule):
    pass
