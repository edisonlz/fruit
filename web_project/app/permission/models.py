#encoding=utf-8
from django.contrib.auth.models import Permission, Group
from django.db import models
from django.conf import settings
from app.content.urls import CUSTOMIZED_URL_TRANS_DICT
import urllib
from app.user.models import User


# Create your models here.


class Perm(models.Model):
    code = models.CharField(u'权限码', max_length=128, db_index=True, unique=True, null=True)

    name = models.CharField(u"英文权限名称", max_length=64)

    action = models.CharField(u"Action Name", max_length=64)

    url_regex = models.CharField(u"Url Pattern", max_length=128)

    platform = models.CharField(u"url所属平台", max_length=64, default='')

    area = models.CharField(u"url所属区域", max_length=64, default='')

    family = models.CharField(u"url所属位置", max_length=128, default='')

    operation = models.CharField(u"url的操作类型", max_length=64, default='')

    class Meta:
        verbose_name = u'系统权限'
        verbose_name_plural = verbose_name
    @classmethod
    def ch_url_name(cls, en_name):
        ch_name_info = [CUSTOMIZED_URL_TRANS_DICT.get(fragment, fragment) for fragment in en_name.split(' ')]
        return ' '.join(ch_name_info)
    @classmethod
    def ch_url_params(cls, en_params):
        return urllib.unquote(en_params).encode('utf-8')

    def __unicode__(self):
        return u"%s" % unicode(self.name)


class UserPerms(models.Model):
    perm = models.ForeignKey(Perm)
    perm.db_index = True
    user = models.ForeignKey(User)
    user.db_index = True

    class Meta:
        verbose_name = u'用户系统权限'
        verbose_name_plural = verbose_name

    @classmethod
    def change_perm(cls, uid, to_delete_perms, to_add_perms):
        #delelte perms
        cls.objects.filter(user_id=uid, perm_id__in=to_delete_perms).delete()
        #add perms
        for perm_id in to_add_perms:
            cls.objects.create(perm_id=perm_id, user_id=uid)


class UserGroupPerms(models.Model):
    perm = models.ForeignKey(Perm)
    perm.db_index = True
    group = models.ForeignKey(Group)
    group.db_index = True

    class Meta:
        verbose_name = u'用户组系统权限'
        verbose_name_plural = verbose_name

    @classmethod
    def change_perm(cls, gid, to_delete_perms, to_add_perms):
        #delelte perms
        cls.objects.filter(group_id=gid, perm_id__in=to_delete_perms).delete()
        #add perms
        for perm_id in to_add_perms:
            cls.objects.create(perm_id=perm_id, group_id=gid)