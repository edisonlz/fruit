# coding=utf-8
import functools
from django.db import models
from django.contrib.auth.models import AbstractUser
from app.content.models.main_page_module import HomeBox
from app.content.models.main_page_common_video import HomeCommonBox
from app.content.models import IphoneChannel, IpadChannel, AndroidChannel, BrandModule


class User(AbstractUser):
    ROLE_CHOICES = (
        (0, "管理员"),
        (1, "普通用户"),
        (2, "总编"),
    )

    NORMAL = 1
    EDITOR = 2
    SUPERUSER = 0

    role = models.IntegerField(verbose_name=u'用户角色', choices=ROLE_CHOICES, default=1)

    class Meta:
        app_label = 'user'

    @property
    def role_name(self):
        role_dic = dict(self.ROLE_CHOICES)
        return role_dic.get(self.role, "无")

    @property
    def is_manager(self):
        return self.is_super or self.is_super_editor

    @property
    def is_super(self):
        return self.role == self.SUPERUSER

    @property
    def is_super_editor(self):
        return self.role == self.EDITOR

    @property
    def is_normal_user(self):
        return self.role == self.NORMAL


class UserBoxPerm(models.Model):
    SOURCE_CHOICE = (
        (0, u"首页平台"),
        (1, u"首页推荐池"),
        (2, u"iphone频道"),
        (3, u"ipad频道"),
        (4, u"android频道"),
        (5, u"品牌官网"),
    )
    alpha_block = {
        'main_page_device': 0,
        'main_page_recommend': 1,
        'iphone_channel': 2,
        'ipad_channel': 3,
        'android_channel': 4,
        'brand': 5,
    }
    src_cls_dict = {
        0: HomeBox,
        1: HomeCommonBox,
        2: IphoneChannel,
        3: IpadChannel,
        4: AndroidChannel,
        5: BrandModule,
    }
    user = models.ForeignKey(User)
    drawer_id = models.IntegerField(blank=False)  # 平台抽屉ID，推荐池盒子ID，频道ID
    source = models.IntegerField(choices=SOURCE_CHOICE, default=0)

    class Meta:
        app_label = 'user'

    @classmethod
    def get_src_id(cls, src_name):
        """
        通过 字符标识 获取 数字标识
        """
        try:
            name = str(src_name)
            return cls.alpha_block[name]
        except KeyError:
            return None

    @classmethod
    def has_perm(cls, box_id, user, src=0):
        if user.is_normal_user:
            return cls.objects.filter(drawer_id=box_id, user=user, source=src).count() > 0
        return True

    @classmethod
    def get_src_cls(cls, src=0):
        if isinstance(src, (str, unicode)):
            src = cls.get_src_id(src)
        try:
            return cls.src_cls_dict[src]
        except KeyError:
            return cls.src_cls_dict[0]

    @classmethod
    def get_src_name_from_platform(cls, platform='iphone'):
        contrast = {
            'iphone': 2,
            'ipad': 3,
            'android': 4
        }
        try:
            return contrast[platform]
        except KeyError:
            return -1
