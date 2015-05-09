#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from django.db.models import Max
from common import Status
from common import BaseModel
import logging
import traceback

class BoxType(object):
    NORMAL = 1
    HEADER_SHOW = 0
    ADV = 2
    
    TYPE_HASH = {
        NORMAL: u'普通盒子',
        HEADER_SHOW: u'轮播图',
        ADV : "整条广告",
    }

    TYPES = [
        (NORMAL, u'普通盒子'),
        (HEADER_SHOW, u'轮播图'),
        (ADV, u'整条广告'),
    ]

    @classmethod
    def to_s(cls,itype):
        return cls.TYPE_HASH.get(itype)


class Box(BaseModel):

    title = models.CharField(max_length=100, default=u'标题')
    position = models.IntegerField(verbose_name=u'位置', default=0, db_index=True)
    iner_count = models.IntegerField(verbose_name=u"内部容器个数", default=12)
    box_type = models.IntegerField(verbose_name=u"模块类型", choices=BoxType.TYPES,default=BoxType.NORMAL, db_index=True)


    objects = CachingManager()

    class Meta:
        verbose_name = u"首页盒子"
        verbose_name_plural = verbose_name
        app_label = "content"

    @property
    def box_type_str(self):
        return BoxType.to_s(int(self.box_type))


    def deletebox(self):
        self.is_delete=1
        self.save()


    @classmethod
    def delete_box(cls,boxid):

        try:
            box = cls.objects.get(pk=boxid)

            box.deletebox()

            return True

        except:

            logging.error(traceback.format_exc())
            return False











