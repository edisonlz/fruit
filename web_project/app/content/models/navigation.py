#coding=utf-8

from django.db import models
from platform import Platform, Status, Imgtype, Channeltype
from wi_cache.base import CachingManager


class AndroidChannelNavigation(models.Model):
    objects = CachingManager()

    NAV_TYPE_OF_ORIGIN = 1  # '优酷频道',原生频道
    NAV_TYPE_OF_TOPIC = 2  # '专题精编',焦点聚焦
    NAV_TYPE_OF_PERSONAL = 3  # '个人频道',个人专属
    NAV_TYPES = { 1: u'优酷频道', 2: u'专题精编', 3: u'个人频道', }

    # 导航这里用nav_type来唯一标识：每个nav_type只有一条记录（限制页面上的新增、删除权限）
    title = models.CharField(max_length=100, default=u'', verbose_name='标题')
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    icon = models.CharField(max_length=255, default=u'', verbose_name='图片')
    nav_type = models.IntegerField(verbose_name=u"导航类型", default=1, db_index=True, max_length=2)
    position = models.IntegerField(verbose_name=u'位置', default=0, db_index=True)
    is_delete = models.BooleanField(verbose_name=u'删除导航', default=False, db_index=True)

    class Meta:
        app_label = "content"

