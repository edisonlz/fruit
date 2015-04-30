#coding=utf-8

from django.db import models

class IosVipGoodsPageBack(models.Model):
    STATUS = ((0, u'关闭'),
              (1, u'开启'), )

    vip_img = models.CharField(max_length=255, verbose_name='小图', default='')
    vip_img_hd = models.CharField(max_length=255, verbose_name='大图', default='')
    state = models.IntegerField(verbose_name='状态（开／关）', choices=STATUS, default=0)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)
    position = models.IntegerField(verbose_name='位置', default=0)
    device_type = models.CharField(max_length=100, verbose_name=u'设备类型(phone/pad)', default='')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        app_label = "content"

    def add_position(self,):
        video_sets = self.__class__.objects.defer('position')
        if not video_sets:
            current_box_max_position = 0
        else:
            current_box_max_position = video_sets.order_by("-position")[0].position + 1
        self.position = current_box_max_position


