# coding=utf-8
from django.db import models
from platform import Platform, Status, Imgtype, Channeltype
from wi_cache.base import CachingManager


class Channel(models.Model):
    objects = CachingManager()

    CONTENT_TYPE_OF_ORIGIN = 1 # '优酷频道',
    CONTENT_TYPE_OF_TOPIC = 2 # '专题精编'
    SHOW_TYPE_OF_CHANNEL = 1 # '普通频道',
    SHOW_TYPE_OF_VIDEO = 2 # '视频频道'
    CONTENT_TYPE = { 1 : '优酷频道', 2 : '专题精编' }
    SHOW_TYPE = { 1 : '普通频道', 2 : '视频频道' }

    title = models.CharField(max_length=100, default=u'名称')
    cid = models.IntegerField(verbose_name=u'频道ID', null=True, blank=True)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    position = models.IntegerField(verbose_name=u'位置', default=0, db_index=True)

    #generic fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间', db_index=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    class Meta:
        # verbose_name = u"iPad频道"
        # verbose_name_plural = verbose_name
        abstract = True
        app_label = "content"

    @property
    def is_game_channel(self):
        return self.cid == 99

    @property
    def is_film_channel(self):
        return self.cid == 96

    @property
    def choiceness_type_sub_channel(self):
        if 'android' in self.__class__.__name__.lower():
            return None
        sub_channel_set = self.subchannel.filter(is_choiceness=1, state=1, is_delete=False)
        if not sub_channel_set:
            return None
        return sub_channel_set[0]

    @property
    def all_type_sub_channel(self):
        sub_channel_set = self.subchannel.filter(type=3, is_show_filters=True, state=1, is_delete=False)
        if not sub_channel_set:
            return None
        return sub_channel_set[0]


class IpadChannel(Channel):
    # platform = models.IntegerField(verbose_name=u"平台类型", default=Platform.IPAD, db_index=True)
    switch_choiceness = models.IntegerField(verbose_name=u"精选开关", choices=Status.STATUS, default=0, max_length=2)
    switch_all = models.IntegerField(verbose_name=u"全部开关", choices=Status.STATUS, default=0, max_length=2)
    image_type_choiceness = models.IntegerField(verbose_name=u'精选图片', choices=Imgtype.IMG_TYPE, default=1, max_length=2) #'精选子频道'横竖图开关
    image_type_all = models.IntegerField(verbose_name=u'全部图片', choices=Imgtype.IMG_TYPE, default=1, max_length=2) #'全部子频道'横竖图开关
    image_type_sale = models.IntegerField(verbose_name=u'营销图片', choices=Imgtype.IMG_TYPE, default=0, max_length=2) #'营销频道'横竖图开关
    #TODO: Rename image to icon
    # icon = models.CharField(max_length=255, verbose_name=u'正常图', null=True, blank=True)
    # #TODO: Rename icon_selected to icon_selected
    # icon_selected = models.CharField(max_length=255, verbose_name=u'选中图', null=True, blank=True)
    icon_small = models.CharField(max_length=255, verbose_name=u'正常图(小)', null=True, blank=True)
    icon_small_selected = models.CharField(max_length=255, verbose_name=u'选中图(小)', null=True, blank=True)
    icon_big = models.CharField(max_length=255, verbose_name=u'正常图(大)', null=True, blank=True)
    icon_big_selected = models.CharField(max_length=255, verbose_name=u'选中图(大)', null=True, blank=True)
    # 是否为营销频道
    for_sale = models.IntegerField(verbose_name=u"频道类型", choices=Channeltype.CHANNEL, default=0, max_length=2)
    content_type = models.IntegerField(verbose_name=u'内容分类',null=True,blank=True)
    show_type = models.IntegerField(verbose_name=u'播放分类',null=True,blank=True)

    @property
    def is_normal(self):
        return self.show_type == 1

    @property
    def image_size_of_slider_module(self):
        return '784x270' if '电影' in self.title else '640x270'

class IphoneChannel(Channel):
    COLOR_BOARD = ('#6bb9dd', '#e36767', '#f6cb7d', '#6ba374')
    channel_id = models.IntegerField(verbose_name=u"频道id", default=0, max_length=2)
    color = models.CharField(max_length=100, verbose_name=u'标题色值', null=True, blank=True)
    image_type = models.IntegerField(verbose_name=u'图片类型', choices=Imgtype.IMG_TYPE, default=1)#这个字段没有赋值的代码
    switch_choiceness = models.IntegerField(verbose_name=u"精选开关", choices=Status.STATUS, default=0, max_length=2)
    switch_all = models.IntegerField(verbose_name=u"全部开关", choices=Status.STATUS, default=0, max_length=2)
    image_type_choiceness = models.IntegerField(verbose_name=u'精选图片', choices=Imgtype.IMG_TYPE, default=1, max_length=2)
    image_type_all = models.IntegerField(verbose_name=u'全部图片', choices=Imgtype.IMG_TYPE, default=1, max_length=2) #'全部子频道'横竖图开关
    state_iphone_3_2 = models.IntegerField(verbose_name=u"v3.2+状态(开/关)", choices=Status.STATUS, default=1, db_index=True, max_length=2)# 对iphone 3.2+ 是开启还是关闭; 0：关闭，1：开启
    icon = models.CharField(max_length=255, verbose_name=u'icon', null=True, blank=True)
    icon_52 = models.CharField(max_length=255, verbose_name=u'icon52x52', null=True, blank=True) #52x52图片
    icon_3_2 = models.CharField(max_length=255, verbose_name=u'icon52x52', null=True, blank=True) #iphone 3.2+ 正常状态下的icon
    icon_3_2_selected = models.CharField(max_length=255, verbose_name=u'icon52x52', null=True, blank=True) ##iphone 3.2+ 选中状态下的icon
    content_type = models.IntegerField(verbose_name=u'内容分类',null=True,blank=True)
    show_type = models.IntegerField(verbose_name=u'播放分类',null=True,blank=True)
    #attached_video_id = models.IntegerField(verbose_name=u'直接关联视频',null=True,blank=True)

    @property
    def is_normal(self):
        return self.show_type == 1

class AndroidChannel(Channel):
    COLOR_BOARD = ('#6bb9dd', '#e36767', '#f6cb7d', '#6ba374')
    #TODO: check if need this field(channel_id)
    #使用cid
    channel_id = models.IntegerField(verbose_name=u"频道id", default=0, max_length=2)
    color = models.CharField(max_length=100, verbose_name=u'标题色值', null=True, blank=True)
    icon = models.CharField(max_length=255, verbose_name=u'图片(喜欢)', null=True, blank=True, default='blue')
    icon_bg = models.CharField(max_length=255, verbose_name=u'背景图', null=True, blank=True) #button_bg
    content_type = models.IntegerField(verbose_name=u'内容分类',null=True,blank=True)
    show_type = models.IntegerField(verbose_name=u'播放分类',null=True,blank=True)
    #daci_content = models.CharField(max_length=255, verbose_name=u'大词', null=True, blank=True) TODO 大词是否需要？
    #attached_video_id = models.IntegerField(verbose_name=u'直接关联视频',null=True,blank=True)
    #TODO: add other fields(refrence cms_android_channels' schema)

    @property
    def is_normal(self):
        return self.show_type == 1
