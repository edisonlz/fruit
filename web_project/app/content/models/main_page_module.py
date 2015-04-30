#coding=utf-8
from django.db import models
from platform import Status, BoxType, Platform, TagType
from main_page_module_tag import IphoneHomeBoxTag, AndroidHomeBoxTag, IpadHomeBoxTag
from wi_cache.base import CachingManager
from django.db.models import Max
from app.content.models import VideoType


class BaseHomeBox(models.Model):
    Generic = 1
    Android = 2
    Ipad = 3
    Iphone = 4

    MODULETYPE = {
        Generic: "all",
        Android: "android",
        Ipad: "ipad",
        Iphone: "iphone",
    }
    PLATFORM_PATTERN = {v: k for k, v in MODULETYPE.items()}

    objects = CachingManager()
    box_id = models.IntegerField(verbose_name=u'模块ID', null=True, blank=True)
    title = models.CharField(max_length=100, default=u'标题')
    position = models.IntegerField(verbose_name=u'位置', default=0, db_index=True)
    cid = models.IntegerField(verbose_name=u'频道ID', default=0)
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    video_count_for_phone = models.IntegerField(verbose_name=u"手机模块视频个数", default=4)
    video_count_for_pad = models.IntegerField(verbose_name=u"手机模块视频个数", default=0)
    platform = models.IntegerField(verbose_name=u"平台类型", default=1, db_index=True)
    box_type = models.IntegerField(verbose_name=u"模块类型", default=1, db_index=True)
    image = models.CharField(max_length=255, default='', verbose_name=u'标题图片')
    image_link = models.CharField(max_length=255, default='', verbose_name=u'标题图片跳转')
    is_youku_channel = models.IntegerField(verbose_name=u'是否主站频道', default=0)
    for_membership = models.IntegerField(verbose_name=u'Ipad是否为会员专享', default=0)
    is_phone_use_multiply_units = models.IntegerField(verbose_name=u'Android多用单元', default=0)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    attached_common_id = models.IntegerField(default=0, verbose_name=u'关联公共模块')
    #def platformization(self):
    class Meta:
        # verbose_name = u"新首页模块"
        # verbose_name_plural = verbose_name
        abstract = True
        app_label = "content"

    @property
    def box_type_to_s(self):
        box_type = BoxType.to_s(int(self.box_type))
        return box_type

    def tag_type_info(self,tag_type='tag'):
        if self.platform == Platform.to_i("iphone"):
            tag_type_info = IphoneHomeBoxTag.tag_types()
            if tag_type == 'tag':
                tag_type_info = [item for item in tag_type_info if item['name'] != 'no_jump']
        elif self.platform == Platform.to_i("android"):
            tag_type_info = AndroidHomeBoxTag.tag_types()
            if tag_type == 'title':
                tag_type_info = [item for item in tag_type_info if item['name'] in TagType.ANDROID_TITLE_TAG_TYPES]
                return tag_type_info
            elif tag_type == 'tag':
                tag_type_info = [item for item in tag_type_info if item['name'] != 'no_jump']
        else:
            tag_type_info = IpadHomeBoxTag.tag_types()
            if tag_type == 'tag':
                tag_type_info = [item for item in tag_type_info if item['name'] != 'no_jump']
        if BoxType.to_s(self.box_type) != 'game' or tag_type == 'title':
            tag_type_info = [item for item in tag_type_info if not item['name'] in TagType.GAME_BOX_UNIQ_TAGS]
        return tag_type_info

    def platform_to_s(self):
        platform = Platform.to_s(int(self.platform))
        return platform

    #params
    #{ image_link': 'http://www.youku.com',
    #  box_id': '', video_count_for_phone': 4,
    #  cid': "1", title': 'test', box_type': 1,
    #  video_count_for_pad': 4,
    #  normal_img': 'http://r1.ykimg.com/0510000054B5E0646714C0612908F08E'}
    def update_value(self, params):
        box_id = params.get("box_id", '0')
        if len(box_id) > 0:
            self.box_id = int(box_id)
        self.image = params.get('normal_img', '')
        self.title = params.get('title', '')
        self.attached_common_id = params.get('attached_common_box_id') or 0
        self.image_link = params.get('image_link', '')
        self.video_count_for_pad = params.get('video_count_for_pad') or 4
        self.video_count_for_phone = params.get('video_count_for_phone') or 4
        if params.get("box_type"):
            self.box_type = params.get("box_type")
        if not self.id:
            max_position = HomeBox.objects.filter(platform=self.platform).aggregate(Max('position'))[
                               'position__max'] or 0
            self.position = max_position + 1
        self.cid = params.get('cid') or '0'
        self.is_youku_channel = 1
        self.save()
        return self

    def create_default_title_tag(self):
        if self.platform == Platform.to_i("android"):
            default_title_tag = AndroidHomeBoxTag()
        elif self.platform == Platform.to_i("ipad"):
            default_title_tag = IpadHomeBoxTag()
        else:
            default_title_tag = IphoneHomeBoxTag()
        default_title_tag.box_id = self.id
        default_title_tag.tag_type = "title"
        default_title_tag.title = self.title
        default_title_tag.jump_type = 1
        default_title_tag.state = 1
        box_type = BoxType.to_s(self.box_type)
        if box_type in HomeBox.IPAD_SPECIAL_BOXES.keys() and self.platform == Platform.to_i("ipad"):
            default_title_tag.cid = HomeBox.IPAD_SPECIAL_BOXES[box_type]['cid']
            default_title_tag.jump_type = TagType.to_i('jump_to_channel')
        default_title_tag.save()

    def update_default_title_tag(self):

        if self.platform == Platform.to_i("android"):
            default_title_tag = AndroidHomeBoxTag.objects.filter(is_delete=False, box_id=self.id, tag_type='title')[0]
        elif self.platform == Platform.to_i("ipad"):
            default_title_tag = IpadHomeBoxTag.objects.filter(is_delete=False, box_id=self.id, tag_type='title')[0]
        else:
            default_title_tag = IphoneHomeBoxTag.objects.filter(is_delete=False, box_id=self.id, tag_type='title')[0]

        default_title_tag.title = self.title
        default_title_tag.save()

    def is_show_tag(self):
        return self.box_type_to_s in ['normal','game']


class HomeBox(BaseHomeBox):
    MaxVideoCountInBox = 200
    MaxPositionInBox = 1000000
    STATIC_BOX_ID = {
        'slider': 99,
        'under_slider': 100,
        'game': 820,
        'recommend': 114,
        'first_banner': 112,
        'second_banner': 113
    }
    IPAD_SPECIAL_BOXES = {
        'recommend':{'id':114,'cid':2000},
        'subscribe':{'id':0,'cid':2004}
    }

    @classmethod
    def check_and_change_cid(cls,tag):
        if tag.tag_type == 'title':
            box = cls.objects.get(pk=tag.box_id,is_delete=0)
            if box:
                box.cid = int(tag.cid)
                box.save()



    def is_game_box(self):
        return self.box_type == BoxType.to_i('game')
    def is_slider_box(self):
        return self.box_type == BoxType.to_i('slider')
    def is_no_video_box(self):
        return self.box_type == BoxType.to_i('recommend') or self.box_type == BoxType.to_i('subscribe')

    def publish_video_count(self):
        if Platform.to_s(self.platform) == 'ipad':
            return self.video_count_for_pad
        elif Platform.to_s(self.platform) == 'iphone':
            return self.video_count_for_phone
        else:
            result = self.video_count_for_phone
            if self.video_count_for_pad > self.video_count_for_phone:
                result = self.video_count_for_pad
            return result
        
    @property
    def box_id_for_android_api(self):
        box_type = BoxType.to_s(self.box_type)
        #一些类型抽屉的box_id字段要写死 用于API判断抽屉类型
        if box_type in HomeBox.STATIC_BOX_ID.keys():
            return HomeBox.STATIC_BOX_ID[box_type]
        else:
            return self.id

