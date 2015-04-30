#coding=utf-8
from django.db import models
from app.content.models import AndroidGame, IosGame
from channel import AndroidChannel, IphoneChannel
from sub_channel import AndroidSubChannel, IphoneSubChannel
from platform import Platform, Status, TagType
from wi_cache.base import CachingManager
from app.content.models import *
from app.content.models.channel import IpadChannel
from app.content.models.sub_channel import IpadSubChannel
from wi_model_util.imodel import get_object_or_none


class HomeBoxTag(models.Model):
    objects = CachingManager()
    box_id = models.IntegerField(verbose_name=u'模块ID', null=True, blank=True, db_index=True)
    tag_type = models.CharField(max_length=100, default='')
    title = models.CharField(max_length=100, default=u'标题')
    # tag的跳转类型：no_jump/jump_to_hotword/jump_to_channel/jump_to_sub_channel/jump_to_game/jump_to_game_list
    jump_type = models.IntegerField(default=0, null=True, blank=True, db_index=True)
    cid = models.IntegerField(verbose_name=u'频道ID', default=0)  #跳转到频道时的cid
    sub_channel_id = models.CharField(max_length=20, verbose_name=u'子频道ID', default='0')  #跳转到子频道时的子频道id
    hot_word = models.CharField(max_length=100, verbose_name=u'热词', default='')
    game_id = models.CharField(max_length=10, verbose_name=u'游戏Id', default='')
    state = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=u'更新时间', auto_now=True)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)

    @property
    def jump_type_int(self):
        return int(self.jump_type)

    class Meta:
        abstract = True
        app_label = "content"


class AndroidHomeBoxTag(HomeBoxTag):
    @classmethod
    def tag_types(cls):
        return Platform.tag_types(Platform.to_i('android'))

    @property
    def jump_type_to_s(self):

        jump_type_id = int(self.jump_type)
        tag_type_info = AndroidHomeBoxTag.tag_types()
        tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
        jump_type_base = tag_type_hash.get(int(self.jump_type))
        #基础跳转说明
        jump_type_name = TagType.to_s(jump_type_id)
        if jump_type_name == "jump_to_channel":
            #new added--hx
            jump_channels = AndroidChannel.objects.filter(cid=self.cid, is_delete=False)
            if jump_channels:
                jump_channel_title = jump_channels[0].title
                #jump_type_detail = " (cid: %s)"% self.cid
                jump_type_detail = " (%s)" % jump_channel_title
            else:
                jump_type_detail = ''
        elif jump_type_name == "jump_to_sub_channel":
            sub_channel = AndroidSubChannel.objects.get(pk=int(self.sub_channel_id))
            channel = sub_channel.channel
            jump_type_detail = "(%s - %s)" % (channel.title, sub_channel.title)
        elif jump_type_name == "jump_to_hotword":
            jump_type_detail = self.hot_word
        elif jump_type_name == "jump_to_game":
            game_application = AndroidGame.objects.get(pk=int(self.game_id))
            print(game_application)
            jump_type_detail = "(game_id: %s)" % game_application.original_game_id
        else:
            jump_type_detail = ""
        #细节跳转说明
        return jump_type_base + jump_type_detail

    # for api
    def details_for_interface(self):
        tag_info = {
            'type': TagType.to_s(self.jump_type),
            'title': self.title,
        }
        tag_jump_type = TagType.to_s(self.jump_type)
        if self.tag_type == 'title' and tag_jump_type == 'no_jump':
            del tag_info['title']

        if tag_jump_type == 'jump_to_hotword':
            tag_info['hotword'] = self.hot_word

        if tag_jump_type == 'jump_to_channel':
            tag_info['cid'] = str(self.cid) if self.cid > 0 else ''

        if tag_jump_type == 'jump_to_sub_channel':
            sub_channel = AndroidSubChannel.objects.get(pk=self.sub_channel_id)
            tag_info['cid'] = ''
            tag_info['sub_channel_id'] = 0
            if sub_channel:
                tag_info['sub_channel_id'] = sub_channel.id or 0
                channel = sub_channel.channel
                if channel:
                    tag_info['cid'] = str(channel.cid) if (channel.cid and channel.cid > 0) else ''

        if tag_jump_type == 'jump_to_game':
            game_application = AndroidGame.objects.get(pk=self.game_id)
            tag_info['game_id'] = 0
            if game_application:
                tag_info['game_id'] = game_application.original_game_id

        return tag_info


class IphoneHomeBoxTag(HomeBoxTag):
    @classmethod
    def tag_types(cls):
        return Platform.tag_types(Platform.to_i('iphone'))

    @property
    def jump_type_to_s(self):
        jump_type_id = int(self.jump_type)
        tag_type_info = IphoneHomeBoxTag.tag_types()
        tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
        jump_type_base = tag_type_hash.get(int(self.jump_type))
        #基础跳转说明
        jump_type_name = TagType.to_s(jump_type_id)
        if jump_type_name == "jump_to_channel":
            #new added--hx
            jump_channels = IphoneChannel.objects.filter(cid=self.cid, is_delete=False)
            if jump_channels:
                jump_channel_title = jump_channels[0].title
                #jump_type_detail = " (cid: %s)"% self.cid
                jump_type_detail = " (%s)" % jump_channel_title
            else:
                jump_type_detail = ''
                #jump_type_detail = " (cid: %s)"% self.cid
        elif jump_type_name == "jump_to_sub_channel":
            sub_channel = IphoneSubChannel.objects.get(pk=int(self.sub_channel_id))
            channel = sub_channel.channel
            jump_type_detail = "(%s - %s)" % (channel.title, sub_channel.title)
        elif jump_type_name == "jump_to_hotword":
            jump_type_detail = self.hot_word
        elif jump_type_name == "jump_to_game":
            game_application = IosGame.objects.get(pk=int(self.game_id))
            jump_type_detail = "(game_id: %s)" % game_application.original_game_id
        else:
            jump_type_detail = ""
        #细节跳转说明
        return jump_type_base + jump_type_detail


class IpadHomeBoxTag(HomeBoxTag):
    @classmethod
    def tag_types(cls):
        return Platform.tag_types(Platform.to_i('ipad'))

    @property
    def jump_type_to_s(self):
        jump_type_id = int(self.jump_type)
        tag_type_info = IpadHomeBoxTag.tag_types()
        tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
        jump_type_base = tag_type_hash.get(int(self.jump_type))
        #基础跳转说明
        jump_type_name = TagType.to_s(jump_type_id)
        if jump_type_name == "jump_to_channel":
            #new added--hx
            jump_channels = IpadChannel.objects.filter(cid=self.cid, is_delete=False)
            if jump_channels:
                jump_channel_title = jump_channels[0].title
                #jump_type_detail = " (cid: %s)"% self.cid
                jump_type_detail = " (%s)" % jump_channel_title
            else:
                jump_type_detail = ''
                #jump_type_detail = " (cid: %s)"% self.cid
        elif jump_type_name == "jump_to_sub_channel":
            sub_channel = IpadSubChannel.objects.get(pk=int(self.sub_channel_id))
            channel = sub_channel.channel
            jump_type_detail = "(%s - %s)" % (channel.title, sub_channel.title)
        elif jump_type_name == "jump_to_hotword":
            jump_type_detail = self.hot_word
        elif jump_type_name == "jump_to_game":
            game_application = IosGame.objects.get(pk=int(self.game_id))
            jump_type_detail = "(game_id: %s)" % game_application.original_game_id
        else:
            jump_type_detail = ""
        #细节跳转说明
        return jump_type_base + jump_type_detail