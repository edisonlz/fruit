#coding=utf-8

from django.db import models
from app.content.models import BaseVideo

########################################以下为频道页视频发布########################################

##################################################
#######－－－－－－－频道下视频发布－－－－－－－－－－－－－
##################################################

class AndroidPubChannelV(BaseVideo):
    channel_id = models.IntegerField(verbose_name=u"频道id", default=0, max_length=2)
    #video_list_module_id是关联到video_list_module的
    video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)

class IphonePubChannelV(BaseVideo):
    channel_id = models.IntegerField(verbose_name=u"频道id", default=0, max_length=2)

class IpadPubChannelV(BaseVideo):
    channel_id = models.IntegerField(verbose_name=u"频道id", default=0, max_length=2)

class AndroidPubChannelVL(BaseVideo):  # VL = VideoList
    pv = models.IntegerField(verbose_name=u'PV', default=0) #这里ruby版是编辑手填的
    video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)


##################################################
#######－－－－－－－子频道下视频发布－－－－－－－－－－－－
##################################################

class AndroidPubSubChannelV(BaseVideo):
     sub_channel_id = models.IntegerField(verbose_name=u"子频道id", default=0, max_length=2)
     video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)

class IphonePubSubChannelV(BaseVideo):
    sub_channel_id = models.IntegerField(verbose_name=u"子频道id", default=0, max_length=2)

class IpadPubSubChannelV(BaseVideo):
    sub_channel_id = models.IntegerField(verbose_name=u"子频道id", default=0, max_length=2)

class AndroidPubSubChannelVL(BaseVideo):
    pv = models.IntegerField(verbose_name='PV', default=0) #这里ruby版是编辑手填的
    video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)




##################################################
#######－－－－－－－子频道模块下视频发布－－－－－－－－－－－
##################################################

class AndroidPubSubChannelMV(BaseVideo):  # MV = ModuleVideo
    game_download_button_name = models.CharField(max_length=100, verbose_name=u'下载按钮名', default='')
    game_details_button_name = models.CharField(max_length=100, verbose_name=u'详情按钮名', default='')
    sub_channel_module_id = models.IntegerField(verbose_name=u'子频道模块ID', default=0)
    video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)

class IphonePubSubChannelMV(BaseVideo):
    sub_channel_module_id = models.IntegerField(verbose_name=u'子频道模块ID', default=0)

class IpadPubSubChannelMV(BaseVideo):
    sub_channel_module_id = models.IntegerField(verbose_name=u'子频道模块ID', default=0)

class IphonePubSubChannelMVV4(BaseVideo):
    game_image = models.CharField(max_length=255, verbose_name=u'游戏图片', default='')
    sub_channel_module_id = models.IntegerField(verbose_name=u'子频道模块ID', default=0)

class AndroidPubSubChannelMVL(BaseVideo):
    pv = models.IntegerField(verbose_name=u'PV', default=0) #这里ruby版是编辑手填的
    video_list_id = models.IntegerField(verbose_name=u'VIDEO LIST ID', default=0)


########################################以下为频道页模块发布########################################
