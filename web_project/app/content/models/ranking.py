# coding: utf8
from django.db import models
from platform import Platform, Status
from wi_cache.base import CachingManager
from django.core.exceptions import FieldError
from django.db.models import Max


def set_position(instance, model, query_dict=None):
    if query_dict:
        try:
            position = model.objects.filter(**query_dict).aggregate(Max('position'))['position__max']
        except (FieldError, TypeError):
            position = 0
    else:
        position = model.objects.all().aggregate(Max('position'))['position__max']
    if position is None:
        position = 0
    setattr(instance, 'position', position+1)


class Ranking(models.Model):
    VER_DIFF = (
        (0, 'iphone high ver'),
        (1, 'iphone low ver'),
    )

    objects = CachingManager()

    title = models.CharField(max_length=100, default=u'', verbose_name=u'名称')
    cid = models.IntegerField(max_length=20, verbose_name=u'频道ID', null=True)
    position = models.IntegerField(verbose_name=u'位置', default=0)
    platform = models.IntegerField(verbose_name=u'平台', default=Platform.ANDROID)
    ver_diff = models.IntegerField(verbose_name=u'版本区分', default=0)
    state = models.IntegerField(verbose_name=u'状态（开／关）', choices=Status.STATUS, default=0)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        verbose_name = u"排行榜"
        verbose_name_plural = verbose_name
        app_label = "content"

    @classmethod
    def ver_diff_value_set(cls):
        return [k for k, v in cls.VER_DIFF]

    def save(self, *args, **kwargs):
        set_position(self, Ranking)
        return super(Ranking, self).save(*args, **kwargs)