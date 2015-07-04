# coding=utf-8
import functools
from django.db import models


class User(models.Model):

    username = models.CharField(verbose_name=u'用户名', max_length=30, unique=True,
        help_text='Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters')


    phone = models.CharField(verbose_name="phone", max_length=16)
    email = models.EmailField(verbose_name=u'电子邮件', blank=True)
    is_active = models.BooleanField(verbose_name=u'是否激活', default=True)
    date_joined = models.DateTimeField(verbose_name=u'注册时间', auto_now_add=True)


    class Meta:
        app_label = 'user'
