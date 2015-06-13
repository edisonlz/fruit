#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from django.db.models import Max
from common import Status
from common import BaseModel
from address import ShoppingAddress,City

import logging
import traceback
from django.conf import settings
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
    shop = models.ForeignKey(ShoppingAddress)

    objects = CachingManager()

    class Meta:
        verbose_name = u"首页盒子"
        verbose_name_plural = verbose_name
        app_label = "content"

    @property
    def box_type_str(self):
        return BoxType.to_s(int(self.box_type))


    @classmethod
    def getBoxes(cls,shop=None):

        if not shop:
            city = City.objects.get(name="全局")
            shop = ShoppingAddress.objects.get(city=city,name="全局")
        else:
            shop = ShoppingAddress.objects.get(pk=shop)

        items = cls.objects.filter(shop=shop)

        return items

    @property
    def items(self):
        return BoxItem.objects.filter(box=self)


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



    @property
    def picture(self):

        picture_dict={
            0:"self.item.adv_image",#head_image
            1:"self.item.show_image",#show_image
            2:"self.item.adv_image",#adv_image
        }
        url = eval(picture_dict.get(self.box.box_type))
        if not url:
            url = eval("self.item.show_image")

        public_url = "http://{}{}".format(settings.APPHOST,url)
        print public_url

        return public_url


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



