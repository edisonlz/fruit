#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from django.db.models import Max


class Status(object):
    StatusOpen = 1
    StatusClose = 0
    STATUS_HASH = {
        StatusClose: u'关闭',
        StatusOpen: u'开启'
    }
    STATUS = [
        (StatusClose, u'关闭'),
        (StatusOpen, u'开启'),
    ]

    @property
    def status_str(self):
        return self.STATUS_HASH.get(self.status)


class BaseModel(models.Model,Status):

    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=Status.StatusClose, db_index=True, max_length=2)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)


    class Meta:
        verbose_name = u"基类"
        verbose_name_plural = verbose_name
        app_label = "content"
        abstract = True
