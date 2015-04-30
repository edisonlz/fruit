#coding=utf-8
from django.db import models
from sub_channel import IpadChannel
from platform import Status
from app.user.models import User
# class UserPathModel(models.Model):
#     commit_datetime = models.DateTimeField(auto_now_add=True)
#     uri = models.CharField(max_length=255)
#     level = models.IntegerField(default=0)
#     action = models.IntegerField(default=0)
#     params = models.TextField()
#     method = models.CharField(max_length=10)
#     user = models.ForeignKey(User,verbose_name=u"用户")
#
#     class Meta:
#         verbose_name = u"用户行为模型"
#         verbose_name_plural = verbose_name
#         app_label = "content"

class UserActionLog(models.Model):
    commit_datetime = models.DateTimeField(auto_now_add=True)
    path = models.CharField(max_length=255)
    params = models.TextField()
    method = models.CharField(max_length=10)
    # object_name = models.CharField(max_length=255,default='')
    # user_action = models.IntegerField(max_length=10,default=0)
    platform = models.CharField(verbose_name=u"平台", default='', max_length=64, db_index=True)
    area = models.CharField(verbose_name=u"区域", default='', max_length=64, db_index=True)
    family = models.CharField(verbose_name=u"位置", default='', max_length=128, db_index=True)
    operation = models.CharField(verbose_name=u"操作", default='', max_length=64, db_index=True)
    user = models.ForeignKey(User, verbose_name=u"用户")
    # level = models.IntegerField(max_length=10,default=0)

    class Meta:
        verbose_name = u"用户行为记录"
        verbose_name_plural = verbose_name
        app_label = "content"
