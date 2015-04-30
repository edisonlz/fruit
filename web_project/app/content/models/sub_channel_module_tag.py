# coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from app.content.models import AndroidSubChannelModule, Status

JUMP_TYPE = [
    ('game_page', u'游戏')
]

LINK_TO_TYPE = [
    ('home_page', u'首页'),
    ('rank_page', u'分类'),
    ('category_page', u'排行榜'),
    ('extend_page', u'运营页'),
]

LINK_TO_TYPE_DICT = {i[0]: i[1] for i in LINK_TO_TYPE}


class AndroidSubChannelModuleTag(models.Model):
    objects = CachingManager()
    module = models.ForeignKey(AndroidSubChannelModule, related_name='tag', verbose_name=u'子频道模块')
    jump_type = models.CharField(max_length=255, verbose_name=u'跳转类型', choices=JUMP_TYPE)
    link_to = models.CharField(max_length=255, verbose_name=u'跳转方式', choices=LINK_TO_TYPE)
    title = models.CharField(max_length=255, verbose_name=u'标题')
    position = models.IntegerField(verbose_name='位置', default=0)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, max_length=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        verbose_name = u"安卓子频道模块Tag"
        verbose_name_plural = verbose_name
        app_label = "content"

    @classmethod
    def game_entrances_for_interface(cls, sub_channel_id, cid):
        """
        吐出子频道内第一个抽屉的tags
        """
        if cid == 99:
            return []
        ret = []
        modules = AndroidSubChannelModule.objects.filter(subchannel_id=sub_channel_id, is_delete=False,
                                                        state=1).order_by('-position')
        if modules:
            tags = modules[0].tag.filter(is_delete=False).order_by('-position')
            ret = [{'title': tag.title, 'link_to': tag.link_to} for tag in tags]

        return ret