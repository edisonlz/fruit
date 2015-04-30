#coding:utf-8
from django.db import models
from sub_channel import IpadChannel
from platform import Status
from wi_cache.base import CachingManager


class JinPage(models.Model):

    # objects = CachingManager()
    #
    # title = models.CharField(max_length=255, verbose_name='标题')
    # type = models.IntegerField(verbose_name='类型', choices=TYPES, default=1)
    # image = models.IntegerField(verbose_name='图片类型',choices=IMAGE_TYPES, default=1)
    # nums = models.IntegerField(verbose_name='个数', max_length=3)
    # channel = models.ForeignKey(IpadChannel, related_name='subchannel', verbose_name='频道')
    # position = models.IntegerField(verbose_name='位置', default=0)
    # state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=1,
    #                             max_length=2)
    #
    # class Meta:
    #     verbose_name = u"IOS精选页"
    #     verbose_name_plural = verbose_name
    #     app_label = "content"

    objects = CachingManager()

    title = models.CharField(max_length=100, verbose_name='标题')
    nums = models.IntegerField(verbose_name='视频个数', max_length=3)
    channel = models.ForeignKey(IpadChannel, related_name='jin_module', verbose_name='精选页')
    position = models.IntegerField(verbose_name='位置', default=0)
    cid = models.IntegerField(verbose_name='频道ID', null=True, blank=True)
    state = models.IntegerField(verbose_name="状态(开/关)", choices=Status.STATUS, default=1,
                                max_length=2)

    class Meta:
        verbose_name = u"IOS精选页"
        verbose_name_plural = verbose_name
        app_label = "content"
