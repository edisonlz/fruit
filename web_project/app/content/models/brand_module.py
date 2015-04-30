#coding=utf-8
from django.db import models
from platform import Status
from wi_cache.base import CachingManager
from wi_model_util.imodel import get_object_or_none


class BrandModule(models.Model):
    objects = CachingManager()

    title = models.CharField(max_length=255, default=u'标题')
    link_to_url = models.CharField(max_length=255, verbose_name='URL', default='')
    state_for_android = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True,
                                            max_length=2)
    state_for_iphone = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True,
                                           max_length=2)
    state_for_ipad = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True,
                                         max_length=2)
    subchannel_id_of_android = models.IntegerField(verbose_name='子频道id', default=0)
    subchannel_id_of_iphone = models.IntegerField(verbose_name='子频道id', default=0)
    subchannel_id_of_ipad = models.IntegerField(verbose_name='子频道id', default=0)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')


    class Meta:
        app_label = "content"


    @classmethod
    def sub_channel_has_brands_headline(cls, platform, sub_channel):
        where_sub_channel = {}
        where_sub_channel['subchannel_id_of_%s' % platform] = sub_channel.id
        the_modules = BrandModule.objects.filter(**where_sub_channel).order_by('-id')
        the_module = the_modules[0] if the_modules else None
        if not the_module:
            return False
        brand_info = sub_channel.location_information(the_module, platform)
        res_bool = brand_info['location_is_valid'] and (brand_info['sub_channel'].id == sub_channel.id)
        return res_bool


    def placement_position_for_view(self, platform, channel_class, sub_channel_class):
        state_column = "state_for_" + platform
        sub_channel_id_column = "subchannel_id_of_" + platform
        state = getattr(self, state_column)
        sub_channel_id = getattr(self, sub_channel_id_column)
        if state == 0:
            return '-'
        if sub_channel_id:
            sub_channel = get_object_or_none(sub_channel_class, pk=sub_channel_id)
            channel = get_object_or_none(channel_class, pk=sub_channel.channel_id)
            if sub_channel:
                return channel.title + "-" + sub_channel.title
        return "-"
