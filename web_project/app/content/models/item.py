#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from django.db.models import Max
from sorl.thumbnail.fields import ImageWithThumbnailsField
import uuid
from home_module import Box
from common import BaseModel

class ItemCategory(BaseModel):

    title = models.CharField(max_length=100, default=u'标题')
    
    class Meta:
        app_label = "content"


class PromoteType(object):
    DISCOUNT = 0
    ONE2ONE = 1
    TYPE_HASH = {
        DISCOUNT: u'折扣',
        ONE2ONE: u'买一送一'
    }
    TYPES = [
        (DISCOUNT, u'折扣'),
        (ONE2ONE, u'买一送一'),
    ]

    @classmethod
    def to_s(cls,itype):
        return TYPE_HASH.get(itype)


class ItemPromote(BaseModel):

    title = models.CharField(max_length=100, default=u'标题')
    promote_rate  = models.FloatField(verbose_name="促销利率")
    promote_type = models.IntegerField(verbose_name="促销类型",choices=PromoteType.TYPES,default=PromoteType.DISCOUNT)


    class Meta:
    	verbose_name = u"促销类型"
        verbose_name_plural = verbose_name
        app_label = "content"

    def save(self,*args,**kwargs):
    	if PromoteType.DISCOUNT == self.promote_type:
    		self.promote_rate = 1
    	super(ItemPromote,self).save(self,*args,**kwargs)
    



class Item(models.Model):

    title = models.CharField(max_length=100, default=u'标题')

    categroy = models.ForeignKey(ItemCategory,verbose_name=u'分类')
    promote = models.ForeignKey(ItemPromote,verbose_name=u'促销',null=True,blank=True)

    price = models.FloatField(verbose_name=u'价格')
    stock_price = models.FloatField(verbose_name=u'进货价格')


	#usage:
	# info['screenshots'] = game.get_screen_shots(obj,web=web)
    # images/app/screen/  ln to outside of project
    show_image = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"展示图")


    adv_image = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"广告图")


    head_image = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"轮播图")


    screen_shot_1 = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"详情图1")

    screen_shot_2 = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"详情图2" )

    screen_shot_3 = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"详情图3" )

    screen_shot_4 = ImageWithThumbnailsField(
        upload_to=lambda ss, name: "images/app/screen/%s.%s" % (uuid.uuid4(), name.split('.')[-1]), blank=False,
        null=False,
        thumbnail={'size': (480, 320), 'extension': 'jpg'},
        extra_thumbnails={
            'phone': {'size': (480, 320), 'extension': 'jpg'}
        }, verbose_name=u"详情图4" )


    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)


    def get_sale_price(self):

    	if self.promote:
    		return (self.promote.promote_type,self.promote.promote_rate * self.price)


# class BoxItem(models.Model):

#     box = models.ForeignKey(Box)
#     item = models.ForeignKey(Item)

#     class Meta:
#         verbose_name = u"盒子水果"
#         verbose_name_plural = verbose_name
#         app_label = "content"


