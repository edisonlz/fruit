# coding=utf-8
from django.db import models
from platform import Platform, Status, Imgtype, Channeltype
from wi_cache.base import CachingManager


class CidDetail(models.Model):
    objects = CachingManager()
    title = models.CharField(max_length=100, default=u'名称')
    cid = models.IntegerField(max_length=20,verbose_name=u'频道ID', null=True, blank=True)
    is_youku_channel = models.IntegerField(verbose_name=u'是否主站频道', default=0)
    #generic fields
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)
    class Meta:
        verbose_name = u"主站频道信息"
        verbose_name_plural = verbose_name
        app_label = "content"

