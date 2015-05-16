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




class BoxItem(models.Model):

    from item import Item

    box = models.ForeignKey(Box)
    item = models.ForeignKey(Item)
    position = models.IntegerField(verbose_name=u'位置', default=0, db_index=True)
    is_delete = models.IntegerField(verbose_name=u"状态",default=0)

    class Meta:
        verbose_name = u"盒子水果"
        verbose_name_plural = verbose_name
        app_label = "content"


    @classmethod
    def deleteItem(cls,boxid,itemid):

        from item import Item

        try:
            print "boxid:{}\titem:{}".format(boxid,itemid)
            box = Box.objects.get(pk=boxid)
            item = Item.objects.get(pk=itemid)

            boxitem = cls.objects.get(box=box,item=item)
            boxitem.is_delete=1
            boxitem.position=0
            boxitem.save()
            return True
        except:
            logging.error(traceback.format_exc())
            return False

    @classmethod
    def getBoxItemNum(cls,box):

        items = cls.objects.filter(box=box,is_delete=0).order_by("-position")
        if items:
            return items[0].position
        else:
            return 0

    @classmethod
    def addItem(cls,boxid,itemid):

        from item import Item

        try:
            print "boxid:{}\titem:{}".format(boxid,itemid)
            box = Box.objects.get(pk=boxid)
            item = Item.objects.get(pk=itemid)

            position = cls.getBoxItemNum(box)
            boxitems = cls.objects.get_or_create(box=box,item=item)
            boxitem=boxitems[0]
            boxitem.position=position+1
            boxitem.is_delete=0
            boxitem.save()

            return True
        except:
            logging.error(traceback.format_exc())
            return False


    @classmethod
    def updatePosition(cls,box_id,item_ids):

        try:
            # import pdb
            # pdb.set_trace()
            position = 1
            for item_id in item_ids:
                boxitem = cls.objects.get(box_id = box_id,item_id=item_id)
                boxitem.position = position
                position += 1
                boxitem.save()

            return True
        except:
            logging.error(traceback.format_exc())
            return False


