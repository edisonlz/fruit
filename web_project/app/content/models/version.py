#coding=utf-8
from django.db import models
class VersionControl(models.Model):
    platform = models.IntegerField(verbose_name='平台', default=0, db_index=True)
    version = models.CharField(max_length=20, verbose_name='版本号', default='')

    class Meta:
        verbose_name = u"平台版本控制"
        verbose_name_plural = verbose_name
        app_label = "content"


class VersionFeature(models.Model):
    BOX_TYPE_FEATURES = (
        {'id': 1, 'name': 'normal', 'desc': u'普通模块'},
        {'id': 2, 'name': 'slider', 'desc': u'轮播图模块'},
        {'id': 3, 'name': 'under_slider', 'desc': u'今日精选模块'},
        {'id': 4, 'name': 'game', 'desc': u'游戏模块'},
    )
    VIDEO_TYPE_FEATURES = (
        {'id': 1, 'name': 'video', 'desc': u'视频'},
        {'id': 2, 'name': 'show', 'desc': 'show'},
        {'id': 3, 'name': 'playlist', 'desc': 'playlist'},
        {'id': 4, 'name': 'url', 'desc': 'url'},
        {'id': 5, 'name': 'video_list', 'desc': u'专题'},  #android only
        {'id': 6, 'name': 'paid_video', 'desc': u'付费视频'},  #android only, useless
        {'id': 7, 'name': 'game_list', 'desc': u'(游戏)列表'},
        {'id': 8, 'name': 'game_download', 'desc': u'(游戏)下载'},
        {'id': 9, 'name': 'game_details', 'desc': u'(游戏)详情'},
        {'id': 10, 'name': 'live_broadcast', 'desc': u'直播'},
        {'id': 11, 'name': 'video_with_game_list', 'desc': u'视频+游戏列表'},  #reversed
        {'id': 12, 'name': 'video_with_game_download', 'desc': u'视频+游戏下载'},  #reversed
        {'id': 13, 'name': 'video_with_game_details', 'desc': u'视频+游戏详情'},  #reversed
        {'id': 14, 'name': 'game_gift', 'desc': u'(游戏)礼包'},
        {'id': 15, 'name': 'game_album', 'desc': u'(游戏)专辑'},  #reversed
        {'id': 16, 'name': 'game_activity', 'desc': u'(游戏)活动'},  #reversed
        {'id': 17, 'name': 'user', 'desc': u'用户'},  #iphone only
    )
    # e.g.
    # platform  version_begin   version_end     feature     value
    # iphone    3.2             4.2             video_type  url
    # iphone    3.5             4.2             video_type  game_details
    # iphone    3.1.2           4.2             box_type    game
    platform = models.IntegerField(verbose_name='平台', default=0, db_index=True)
    version_begin = models.CharField(max_length=20, verbose_name='起始版本号', default='')  # 空表示任意低于终止的版本都有效
    version_end = models.CharField(max_length=20, verbose_name='终止版本号', default='')  # 空表示任意大于起始的版本都有效
    feature = models.CharField(max_length=200, verbose_name='特征项', default='')
    value = models.CharField(max_length=200, verbose_name='取值', default='')

    class Meta:
        verbose_name = u"版本类型控制"
        verbose_name_plural = verbose_name
        app_label = "content"

    # TODO: fix these data belows:
    init_data = [
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'show'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'playlist'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'url'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_list'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_deails'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'live_broadcast'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video_with_game_details'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_gift'},
        {'platform': 'iphone', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'user'},

        {'platform': 'ipad', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video'},
        {'platform': 'ipad', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'show'},
        {'platform': 'ipad', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'playlist'},
        {'platform': 'ipad', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'url'},
        {'platform': 'ipad', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'live_broadcast'},

        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'show'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'playlist'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'url'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video_list'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_list'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_download'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_deails'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'live_broadcast'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'video_with_game_details'},
        {'platform': 'android', 'version_begin': '3.0', 'version_end': '', 'feature': 'video_type', 'value': 'game_gift'},
    ]

    @classmethod
    def supported_box_types(cls, platform, ver=''):
        return cls.supported_features('main_page_box_type', platform, ver)

    @classmethod
    def supported_video_types(cls, platform, ver=''):
        return cls.supported_features('main_page_video_type', platform, ver)

    @classmethod
    def supported_features(cls, feature, platform, ver=''):
        types = cls.objects.filter(feature=feature, platform=platform, version_begin__gte=ver)
        type_collection = []
        for type in types:
            if not(type.version_end and type.version_end < ver):
                type_collection.append(type.value)
        return  type_collection

    @classmethod
    def get_all_box_type_features(cls):
        return cls.BOX_TYPE_FEATURES

    @classmethod
    def get_all_video_type_feature(cls):
        return cls.VIDEO_TYPE_FEATURES
