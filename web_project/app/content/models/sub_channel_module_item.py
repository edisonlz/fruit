# coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType
from sub_channel_module import IpadSubChannelModule, IphoneSubChannelModule, IphoneSubChannelModuleV4, \
    AndroidSubChannelModule
from base_video import BaseVideo
from app.content.models import HomeBox, VideoListModule, AndroidGame, IosGame
from base.youkuapi.video import VideoApi
from base.youkuapi.show import ShowApi
from base.youkuapi.playlist import PlaylistApi
from base.youkuapi.parse_item import parse_item_id_and_type
from app.content.lib.model_util import ModelUtil
from wi_model_util.imodel import get_object_or_none


class IpadSubChannelModuleItem(BaseVideo):
    module = models.ForeignKey(IpadSubChannelModule, related_name='moduleItem', verbose_name=u'模块视频')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            # 'game_list', 'game_download', 'game_details',
            # 'live_broadcast',
            # 'video_with_game_list',
            # 'video_with_game_download',
            # 'video_with_game_details',
            # 'game_gift',  #'game_album', 'game_activity',
            # 'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('ipad'), types)

    def check_copyright(self, video_info, device_type='pad'):
        return ModelUtil.check_copyright(self.video_type, video_info, 'pad')


class IphoneSubChannelModuleV4Item(BaseVideo):
    module = models.ForeignKey(IphoneSubChannelModuleV4, related_name='moduleItem', verbose_name='v4.x模块视频')
    game_image = models.CharField(max_length=255, verbose_name='游戏图片', default='')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
            # 'live_broadcast',
            'video_with_game_list',
            # 'video_with_game_download',
            'video_with_game_details',
            # 'game_gift',  #'game_album', 'game_activity',
            # 'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list', 'game_download'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('iphone'), types)


class IphoneSubChannelModuleVideo(BaseVideo):
    module = models.ForeignKey(IphoneSubChannelModule, related_name='moduleVideo', verbose_name=u'模块视频')

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list',
            # 'game_download',
            'game_details',
            # 'live_broadcast',
            # 'video_with_game_list',
            # 'video_with_game_download',
            # 'video_with_game_details',
            # 'game_gift',  #'game_album', 'game_activity',
            # 'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list', 'video_with_game_details',\
               # 'game_download', 'game_details','game_list'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('iphone'), types)


class AndroidSubChannelModuleVideo(BaseVideo):
    module = models.ForeignKey(AndroidSubChannelModule, related_name='moduleVideo', verbose_name=u'模块视频')
    video_list_id = models.IntegerField(verbose_name='VIDEO LIST ID', default=0)
    game_download_button_name = models.CharField(max_length=100, verbose_name=u'下载按钮名', default='')
    game_details_button_name = models.CharField(max_length=100, verbose_name=u'详情按钮名', default='')

    def add_url_type_fields(self, params):
        self.url = params.get("url", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        # DO NOT SAVE HERE
        # self.save()

    def add_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.game_id = 0
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        # DO NOT SAVE HERE
        # self.save()

    def add_game_gift_type_fields(self, params):
        self.game_page_id = params.get("game_page_id", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        # DO NOT SAVE HERE
        # self.save()

    #should override in subclass if different to this
    def add_game_details_type_fields(self, params, mock_video_fields=False):
        new_game = AndroidGame.create_or_update(params)
        self.game_id = new_game.id
        if not mock_video_fields:
            self.title = params.get("title", '')
            self.h_image = params.get("h_image", '')
            self.v_image = params.get("v_image", '')
            self.s_image = params.get("s_image", '')
            self.game_download_button_name = params.get('game_download_button_name','')
            self.game_details_button_name = params.get('game_details_button_name','')

    #should override in subclass if different to this
    def add_game_download_type_fields(self, params):
        new_game = AndroidGame.create_or_update(params)
        self.game_id = new_game.id
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        # DO NOT SAVE HERE
        # self.save()

    def update_game_download_type_fields(self, params):
        game = AndroidGame.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def add_video_with_game_details_type_fields(self, params):
        self.add_video_type_fields(params)
        self.attached_game_type = 'game_details'
        self.add_game_details_type_fields(params)
        # self.save()

    def update_url_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def update_video_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def update_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def add_game_details_type_fields(self, params):
        game = AndroidGame.create_or_update(params)
        self.game_id = game.id
        if not self.attached_game_type:  # 判断游戏详情类型，避免视频＋游戏类型覆盖视频的title和h_image
            self.title = params.get('title')
            self.h_image = params.get('h_image')
            self.v_image = params.get("v_image", '')
            self.s_image = params.get("s_image", '')
            self.game_download_button_name = params.get('game_download_button_name','')
            self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def update_game_details_type_fields(self, params):
        game = AndroidGame.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    def update_game_gift_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name','')
        self.game_details_button_name = params.get('game_details_button_name','')
        self.save()

    @property
    def image_for_client(self):
        return getattr(self,"_image_for_client")

    @image_for_client.setter
    def image_for_client(self,value):
        self._image_for_client = value

    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url','video_list',
            # 'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
            # 'live_broadcast',
            'video_with_game_list', 'video_with_game_download', 'video_with_game_details',
            'game_gift',  #'game_album', 'game_activity',
            'user',
        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list', \
               'game_list', 'video_with_game_download', 'user',  'live_broadcast','video_list'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks,types)
        return VideoType.platformization(Platform.to_i('android'), types)

    def add_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.save()

    def update_video_list_type_fields(self, params):
        self.title = params.get('title', "")
        self.video_list_id = params.get('video_list_id')
        self.box_id = params.get("box_id")
        self.video_type = VideoType.to_i("video_list")
        self.save()
    @property
    def client_image_for_interface(self):
        return self.image_for_client or ''

    @property
    def details_for_interface(self):
        video_information = {
            'content_id' : self.video_id,
            'content_type' : str(self.video_type),
            'title' : self.title,
            'image' : self.client_image_for_interface,
            'intro' : self.intro,
            #:playlist_videoid : self.playlist_videoid,
            'url' : self.url,
            'pv' : self.first_episode_video_pv,
            'second_title' : self.subtitle,
            'paid' : self.paid
        }
        video_information['playlist_videoid'] = ''
        if self.video_type == 3:
            video_information['playlist_videoid'] = self.first_episode_video_id

        if self.video_type in [7,8,9,11,12,13,14,15,16]:
            if self.video_type in [7,8,9,11,12,13]:
                video_information['game_relation'] = (self.attached_game_type and "attached") or "standalone" #括号可省
                video_information['game_information'] = self.game_information_hash
                if self.module.module_type == 1:
                    #轮播图类型模块
                    video_information['game_download_button_name'] = self.game_download_button_name or ''
                    video_information['game_details_button_name'] = self.game_details_button_name or ''
            elif self.video_type in[14,15,16]:
                video_information['game_page_id'] = self.game_page_id or ''
            if self.module.module_type == 3:
                #video_in_game_banner_module
                video_information['game_vertical_image'] = self.v_image or ''
                video_information['game_horizontal_image'] = self.h_image or ''
        return video_information

    @property
    def game_type_for_interface(self):
    #这里传出的值与首页接口保持一致
        if self.attached_game_type:
            if self.attached_game_type and len(self.attached_game_type) > 0:
                if self.attached_game_type == 'game_list':
                    return 'show_list'
                elif self.attached_game_type == 'game_download':
                    return 'download_game'
                elif self.attached_game_type == 'game_details':
                    return 'show_details'
                else:
                    return 'unknown'
        elif self.video_type in [7,8,9]:
            if self.video_type == 7:
                return 'show_list'
            elif self.video_type == 8:
                return 'download_game'
            elif self.video_type == 9:
                return 'show_details'
        else:
            return 'unknown'

    @property
    def game_information_hash(self):
        game_application = get_object_or_none(AndroidGame, pk=self.game_id)
        if not game_application:
            return {}
        if game_application:
            game_id = game_application.original_game_id
            game_type = self.game_type_for_interface
            return {
              'game_type' : game_type,
              'game_id' : game_id,
              'game_name' : game_application.name,
              'game_description' : game_application.description,
              'game_package_name' : game_application.package_name,
              'game_logo' : game_application.logo,
              'game_version_code' : game_application.version_code,
              'game_version_name' : game_application.version_name,
              'game_url' : game_application.url,
              'game_type_name' : game_application.category_name,
              'game_class_name' : game_application.category_name,
              'game_score' : (game_application.score or '0')
              #:comment => 'game_type_name 跟 game_class_name 是一样的，
              #都是java class name, 对于android 3.6 以及以上有效.
              #对于android 3.5.x 版本，还是要靠上面的content_type来识别如何处理。而且3.5.x不会使用 本节点中的game_type内容。 '
            }
        else:
            return {}




