#coding=utf-8
from django.db import models
#from app.content.models.main_page_module import HomeBox
class Platform(object):
    KEYS = {"android": 1, "ipad": 2, "iphone": 3, "win_phone": 4}
    ANDROID = 1
    IPAD = 2
    IPHONE = 3
    WIN_PHONE = 4

    @classmethod
    def all(cls):
        return cls.KEYS

    @classmethod
    def names(cls):
        return cls.KEYS.keys()

    @classmethod
    def ids(cls):
        return cls.KEYS.values()

    #TODO: drop this method, and go to VideoModel.video_types
    # @classmethod
    # def video_types(cls, platform_key, location='main_page', mock=False, names=()):
    #     '''
    #     params.platform_key: 1 ~ 4
    #     params.location: 首页/频道页
    #     params.mock: 是否屏蔽掉页面上不显示的类型
    #     return: 相应平台(首页/频道页)的所有(实际/页面)支持的视频类型
    #     '''
    #     return VideoType.platformization(platform_key, location, mock, names)

    @classmethod
    def box_types(cls, platform_key):
        return BoxType.platformization(platform_key)

    @classmethod
    def tag_types(cls, platform_key):
        return TagType.platformization(platform_key)

    @classmethod
    def to_i(cls, platform_name):
        return cls.KEYS.get(platform_name)

    @classmethod
    def to_s(cls, platform_key):
        for k, v in cls.KEYS.items():
            if v == platform_key:
                return k
        return ''

    #TODO: deprecate code bellows:
    @classmethod
    def get_platform(cls, path):
        ps = path.split("/")
        if ps and len(ps) > 2:
            return cls.KEYS.get(ps[2])


class Status(object):
    StatusOpen = 1
    StatusClose = 0
    STATUS_HASH = {
        StatusClose: u'关闭',
        StatusOpen: u'开启'
    }
    STATUS = [
        (StatusClose, u'关闭'),
        (StatusOpen, u'开启'),
    ]



class VideoType(object):
    KEYS = (
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
    #android support all the video types
    ANDROID_DEFAULT = []
    for key in KEYS:
        ANDROID_DEFAULT.append(key['name'])
    ANDROID_DEFAULT = tuple(ANDROID_DEFAULT)
    IPAD_DEFAULT = (
        'video',
        'url',
        'playlist',
        'show',
        'game_list',
        'game_details',
        'game_gift',
        'live_broadcast',
        'user'
    )
    WIN_PHONE_DEFAULT = IPAD_DEFAULT
    IPHONE_DEFAULT = (
        'video',
        'show',
        'playlist',
        'url',
        'game_list',
        'game_details',
        'live_broadcast',
        'video_with_game_list',  #reversed
        'video_with_game_download',  #reversed
        'video_with_game_details',  #reversed
        'game_gift',
        'game_album',  #reversed
        'game_activity',  #reversed
        'user',  #reversed
    )
    @classmethod
    # def platformization(cls, platform_type, location='main_page', mock=False, names=(), mocks=()):
    def platformization(cls, platform_type, names=()):
        '''
        :param int platform_type: 1/2/3/4
        return dict of video_types of video_type_names, default by platform_type(int)
        '''
        result = []
        if not names:
            names = cls.default_names(platform_type)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value)
        return result

    @classmethod
    # def names(cls, platform_key, location='main_page', mock=False, mocks=()):
    def default_names(cls, platform_key):
        if platform_key == Platform.to_i('android'):
            return cls.ANDROID_DEFAULT
        if platform_key == Platform.to_i('ipad'):
            return cls.IPAD_DEFAULT
        if platform_key == Platform.to_i('iphone'):
            return cls.IPHONE_DEFAULT
        if platform_key == Platform.to_i('win_phone'):
            return cls.WIN_PHONE_DEFAULT
        else:
            #TODO: define ErrorPlatformException
            raise Exception

    @classmethod
    # def ids(cls, platform_key, location='main_page', mock=False):
    def ids(cls, platform_key, names=()):
        result = []
        if not names:
            names = cls.default_names(platform_key)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value['id'])
        return result

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for type in cls.KEYS:
            if type_id == type['id']:
                d_type = type
                break
        return d_type

    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for type in cls.KEYS:
            if type_name == type['name']:
                d_type = type
                break
        return d_type

    @classmethod
    def to_s(cls, type_id):
        d_type = cls.id_to_dict(type_id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0

    @classmethod
    def to_desc(cls, type_id):
        d_type = cls.id_to_dict(type_id)
        if d_type:
            return d_type['desc']
        else:
            return ''


class BoxType(object):
    #KEYS = {'normal': 1, 'slider': 2, 'under_slider': 3, 'game': 4}
    KEYS = (
        {'id': 1, 'name': 'normal', 'desc': u'普通模块'},
        {'id': 2, 'name': 'slider', 'desc': u'轮播图模块'},
        {'id': 3, 'name': 'under_slider', 'desc': u'今日精选模块'},
        {'id': 4, 'name': 'game', 'desc': u'游戏模块'},
        {'id': 5, 'name': 'recommend', 'desc': u'为我推荐模块'},
        {'id': 6, 'name': 'subscribe', 'desc': u'订阅更新模块'}
    )
    ANDROID = []
    for key in KEYS:
        ANDROID.append(key['name'])
    ANDROID = tuple(ANDROID)
    # ANDROID = KEYS
    IPAD = ANDROID
    IPHONE = ANDROID
    WIN_PHONE = ANDROID

    @classmethod
    def all(cls):
        return cls.KEYS

    @classmethod
    def to_s(cls, type_id):
        id = int(type_id) if type_id else 0
        d_type = cls.id_to_dict(id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0

    @classmethod
    def platformization(cls, platform_type, location='main_page'):
        '''
        return dict of box_types by platform_type(int)
        '''
        result = []
        names = cls.names(platform_type)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value)
        return result

    @classmethod
    def names(cls, platform_key):
        if platform_key == Platform.to_i('android'):
            return cls.ANDROID
        if platform_key == Platform.to_i('ipad'):
            return cls.IPAD
        if platform_key == Platform.to_i('iphone'):
            return cls.IPHONE
        if platform_key == Platform.to_i('win_phone'):
            return cls.WIN_PHONE

    @classmethod
    def ids(cls, platform_key):
        result = []
        names = cls.names(platform_key)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value['id'])
        return result

    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for type in cls.KEYS:
            if type_name == type['name']:
                d_type = type
                break
        return d_type

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for type in cls.KEYS:
            if type_id == type['id']:
                d_type = type
                break
        return d_type


class TagType(object):
    KEYS = (
        {'id': 1, 'name': 'no_jump', 'desc': u'无跳转'},
        {'id': 2, 'name': 'jump_to_channel', 'desc': u'跳转到频道'},
        {'id': 3, 'name': 'jump_to_sub_channel', 'desc': u'跳转到子频道'},
        {'id': 4, 'name': 'jump_to_hotword', 'desc': u'跳转到热词'},
        {'id': 5, 'name': 'jump_to_game_list', 'desc': u'跳转到游戏列表'},
        {'id': 6, 'name': 'jump_to_game', 'desc': u'跳转到游戏详情'},
    )
    GAME_BOX_UNIQ_TAGS = ['jump_to_game_list','jump_to_game']
    ANDROID_TITLE_TAG_TYPES = ['no_jump','jump_to_sub_channel']
    # ANDROID_BOX_BLOCK_TAGS = ['jump_to_game_list','jump_to_game','jump_to_channel','jump_to_hotword',]
    def platformization(cls, platform_type, box_type=1):
        pass


    ANDROID = []
    for key in KEYS:
        ANDROID.append(key['name'])
    IPHONE = ANDROID[:]
    IPHONE.remove('jump_to_hotword')
    ANDROID = tuple(ANDROID)
    IPHONE = tuple(IPHONE)
    # ANDROID = KEYS
    IPAD = ANDROID
    WIN_PHONE = ()

    @classmethod
    def all(cls):
        return cls.KEYS

    @classmethod
    def to_s(cls, type_id):
        d_type = cls.id_to_dict(type_id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0

    @classmethod
    def platformization(cls, platform_type, location='main_page'):
        '''
        return dict of box_types by platform_type(int)
        '''
        result = []
        names = cls.names(platform_type)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value)
        return result

    @classmethod
    def names(cls, platform_key):
        if platform_key == Platform.to_i('android'):
            return cls.ANDROID
        if platform_key == Platform.to_i('ipad'):
            return cls.IPAD
        if platform_key == Platform.to_i('iphone'):
            return cls.IPHONE
        if platform_key == Platform.to_i('win_phone'):
            return cls.WIN_PHONE
        return ()

    @classmethod
    def ids(cls, platform_key):
        result = []
        names = cls.names(platform_key)
        for name in names:
            value = cls.name_to_dict(name)
            if value:
                result.append(value['id'])
        return result

    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for type in cls.KEYS:
            if type_name == type['name']:
                d_type = type
                break
        return d_type

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for type in cls.KEYS:
            if type_id == type['id']:
                d_type = type
                break
        return d_type

class Imgtype(object):
    ImgVertical = 2
    ImgHorizontal = 1
    IMG_TYPE = [
        (ImgHorizontal, u'横图'),
        (ImgVertical, u'竖图')
    ]
    KEYS = (
        {'id': 1, 'name': 'horizontal', 'desc': u'横图'},
        {'id': 2, 'name': 'vertical', 'desc': u'竖图'},
    )
    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for type in cls.KEYS:
            if type_name == type['name']:
                d_type = type
                break
        return d_type

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for type in cls.KEYS:
            if type_id == type['id']:
                d_type = type
                break
        return d_type
    @classmethod
    def to_s(cls, type_id):
        d_type = cls.id_to_dict(type_id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0



class Channeltype(object):
    SaleOpen = 1
    SaleClose = 0

    CHANNEL = [
        (SaleOpen, u'营销频道'),
        (SaleClose, u'非营销频道')
    ]

class SubChannelType(object):
    KEYS = (
        {'id': 1, 'name': 'editable_box', 'desc': u'抽屉'},
        {'id': 2, 'name': 'editable_video_list', 'desc': u'列表'},
        {'id': 3, 'name': 'filter', 'desc': u'筛选条件'},
    )
    @classmethod
    def name_to_dict(cls, type_name):
        d_type = {}
        for type in cls.KEYS:
            if type_name == type['name']:
                d_type = type
                break
        return d_type

    @classmethod
    def id_to_dict(cls, type_id):
        d_type = {}
        for type in cls.KEYS:
            if type_id == type['id']:
                d_type = type
                break
        return d_type
    @classmethod
    def to_s(cls, type_id):
        d_type = cls.id_to_dict(type_id)
        if d_type:
            return d_type['name']
        else:
            return ''

    @classmethod
    def to_i(cls, type_name):
        d_type = cls.name_to_dict(type_name)
        if d_type:
            return d_type['id']
        else:
            return 0

class SubChannelModuleType(SubChannelType):
    KEYS =  (
        {'id': 0, 'name': 'normal', 'desc': u'普通'},
        {'id': 1, 'name': 'headline', 'desc': u'轮播图'},
        {'id': 2, 'name': 'game', 'desc': u'游戏'},
        {'id': 3, 'name': 'game_banner', 'desc': u'游戏头图'},
    )