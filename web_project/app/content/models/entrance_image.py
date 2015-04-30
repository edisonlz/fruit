# coding=utf-8
from django.db import models
from platform import Status


class EntranceImage(models.Model):
    TERMINAL = (
        (1, 'Android Phone'),
        (2, 'Android Pad'),
        (3, 'iPhone'),
        (4, 'iPad'),
    )

    image = models.CharField(max_length=255, verbose_name='图片', default='')
    image_4s = models.CharField(max_length=255, verbose_name='iPhone4s图片', default='')
    image_5s = models.CharField(max_length=255, verbose_name='iPhone5s图片', default='')
    image_6 = models.CharField(max_length=255, verbose_name='iPhone6图片', default='')
    image_6plus = models.CharField(max_length=255, verbose_name='iPhone6plus图片', default='')
    terminal_type = models.IntegerField(verbose_name='客户端类型', default=0, choices=TERMINAL)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=1, db_index=True,
                                max_length=2)
    # is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)
    effect_at = models.DateTimeField(verbose_name='生效时间')
    expired_at = models.DateTimeField(verbose_name='过期时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间', db_index=True)

    class Meta:
        verbose_name = u"客户端启动页"
        verbose_name_plural = verbose_name
        app_label = "content"

    @classmethod
    def terminal_int_type_set(cls):
        return [k for k, v in cls.TERMINAL]

    @classmethod
    def get_terminal_str(cls, terminal_type):
        for k, v in cls.TERMINAL:
            if k == terminal_type:
                return v