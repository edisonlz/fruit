#coding=utf-8
from django.db import models
from app.content.models import Platform, VideoType, SubChannelType, AndroidGame
from app.content.lib.model_util import ModelUtil
from base_video import BaseVideo
from base.youkuapi.playlist import PlaylistApi
from django.db.models import Q


class FixedPositionVideo(BaseVideo):
    channel_id = models.IntegerField(verbose_name='所属频道ID', default=0)
    subchannel_id = models.IntegerField(verbose_name='所属子频道ID', default=0)
    module_id = models.IntegerField(verbose_name='所属子频道抽屉ID', default=0)
    fixed_position = models.IntegerField(verbose_name='固定位置', default=0)
    subchannel_type = models.IntegerField(verbose_name='所属子频道类型', default=0)

    class Meta:
        abstract = True
        app_label = "content"

    @classmethod
    def position_fixed_videos_replace_processor(cls, target_videos, fixed_videos):
        target_videos_list = list(target_videos)
        original_videos_count = len(target_videos_list)
        for fixed_video in fixed_videos:
            if fixed_video.fixed_position <= original_videos_count:
                target_videos_list.insert(fixed_video.fixed_position - 1, fixed_video)
        return target_videos_list[:original_videos_count]

    @classmethod
    def get_fixed_videos(cls, fixed_video_class, options):
        if options['subchannel_type'] == SubChannelType.to_i('editable_box'):
            return fixed_video_class.objects.filter(module_id=options['module_id'], is_delete=0,
                                                    state=1).order_by('fixed_position')
        elif options['subchannel_type'] == SubChannelType.to_i('editable_video_list'):
            return fixed_video_class.objects.filter(subchannel_id=options['subchannel_id'], is_delete=0,
                                                    state=1).order_by('fixed_position')
        return None


class AndroidFixedPositionVideo(FixedPositionVideo):
    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return (
            'video', 'show', 'playlist', 'url',
            # 'video_list',
            # 'paid_video',
            'game_list', 'game_download', 'game_details',
            # 'live_broadcast',
            'video_with_game_list', 'video_with_game_download', 'video_with_game_details',
            'game_gift',  #'game_album', 'game_activity',

        )

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return 'show', 'playlist', 'video_with_game_list', \
                'video_with_game_download', 'user',  'live_broadcast','video_list'

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks,types)
        return VideoType.platformization(Platform.to_i('android'), types)

    @classmethod
    def get_fixed_videos(cls, fixed_video_class, options):
        # fixed_videos = FixedPositionVideo.get_fixed_videos(fixed_video_class, options)
        fixed_videos = super(AndroidFixedPositionVideo, cls).get_fixed_videos(fixed_video_class, options)

        if not options['ver'] >= '4.1.3':
            fixed_videos = fixed_videos.filter(attached_game_type='').exclude(video_type__in=(7, 8, 9))
        if not options['ver'] >= '4.3':
            fixed_videos = fixed_videos.exclude(video_type__in=(14, 15, 16))
        return fixed_videos

    @classmethod
    def position_fixed_videos_replace_processor(cls, target_videos, fixed_videos):
        target_videos_list = list(target_videos)
        original_videos_count = len(target_videos_list)
        for fixed_video in fixed_videos:
            if fixed_video.fixed_position <= original_videos_count:
                target_video = target_videos_list[fixed_video.fixed_position - 1]
                fixed_video.image_for_client = getattr(target_video, 'image_for_client', '')
                target_videos_list.insert(fixed_video.fixed_position - 1, fixed_video)
        return target_videos_list[:original_videos_count]

    @classmethod
    def replace_position_fixed_videos(cls, target_videos, options={}):
        fixed_videos = cls.get_fixed_videos(AndroidFixedPositionVideo, options)
        if not fixed_videos:
            return target_videos
        return cls.position_fixed_videos_replace_processor(target_videos, fixed_videos)

    def add_url_type_fields(self, params):
        self.url = params.get("url", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        # DO NOT SAVE HERE
        # self.save()

    def add_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.game_id = 0
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        # DO NOT SAVE HERE
        # self.save()

    def add_game_gift_type_fields(self, params):
        self.game_page_id = params.get("game_page_id", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
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
            self.game_download_button_name = params.get('game_download_button_name', '')
            self.game_details_button_name = params.get('game_details_button_name', '')

    #should override in subclass if different to this
    def add_game_download_type_fields(self, params):
        new_game = AndroidGame.create_or_update(params)
        self.game_id = new_game.id
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        # DO NOT SAVE HERE
        # self.save()

    def update_game_download_type_fields(self, params):
        game = AndroidGame.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()

    def add_video_with_game_details_type_fields(self, params):
        self.add_video_type_fields(params)
        self.attached_game_type = 'game_details'
        mock_video_fields = True if self.attached_game_type else False
        self.add_game_details_type_fields(params, mock_video_fields=mock_video_fields)
        # self.save()

    def update_url_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()

    def update_video_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()

    def update_game_list_type_fields(self, params):
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()

    def update_game_details_type_fields(self, params):
        game = AndroidGame.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()

    def update_game_gift_type_fields(self, params):
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.game_download_button_name = params.get('game_download_button_name', '')
        self.game_details_button_name = params.get('game_details_button_name', '')
        self.save()


    @property
    def image_for_client(self):
        return getattr(self,"_image_for_client")

    @image_for_client.setter
    def image_for_client(self,value):
        self._image_for_client = value

    @property
    def client_image_for_interface(self):
        return self.image_for_client or ''

    @property
    def details_for_interface(self):
        video_information = {
            'content_id': self.video_id,
            'content_type': str(self.video_type),
            'title': self.title,
            'image': self.client_image_for_interface,
            'intro': self.intro,
            #:playlist_videoid : self.playlist_videoid,
            'url': self.url,
            'pv': self.first_episode_video_pv,
            'second_title': self.subtitle,
            'paid': self.paid
        }
        video_information['playlist_videoid'] = ''
        if self.video_type == 3:
            video_information['playlist_videoid'] = self.first_episode_video_id

        if self.attached_game_type or self.video_type in [7, 8, 9, 14, 15, 16]:
            if self.attached_game_type or self.video_type in [7, 8, 9]:
                video_information['game_relation'] = (self.attached_game_type and "attached") or "standalone"  #括号可省
                video_information['game_information'] = self.game_information_hash
            elif self.video_type in [14, 15, 16]:
                video_information['game_page_id'] = self.game_page_id or ''
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
        elif self.video_type in [7, 8, 9]:
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
        game_application = AndroidGame.objects.get(pk=self.game_id)
        if game_application:
            game_id = game_application.original_game_id
            game_type = self.game_type_for_interface
            return {
                'game_type': game_type,
                'game_id': game_id,
                'game_name': game_application.name,
                'game_description': game_application.description,
                'game_package_name': game_application.package_name,
                'game_logo': game_application.logo,
                'game_version_code': game_application.version_code,
                'game_version_name': game_application.version_name,
                'game_url': game_application.url,
                'game_type_name': game_application.category_name,
                'game_class_name': game_application.category_name,
                'game_score': (game_application.score or '0')
                #:comment => 'game_type_name 跟 game_class_name 是一样的，
                #都是java class name, 对于android 3.6 以及以上有效.
                #对于android 3.5.x 版本，还是要靠上面的content_type来识别如何处理。而且3.5.x不会使用 本节点中的game_type内容。 '
            }
        else:
            return {}


class IphoneFixedPositionVideo(FixedPositionVideo):
    @classmethod
    def get_fixed_videos(cls, fixed_video_class, options):
        # fixed_videos = FixedPositionVideo.get_fixed_videos(fixed_video_class, options)
        fixed_videos = super(IphoneFixedPositionVideo, cls).get_fixed_videos(fixed_video_class, options)

        if options.get('include_mon_pay_video', ''):
            fixed_videos = fixed_videos.filter(Q(paid=0) | Q(paid=1, pay_type=BaseVideo.pay_type.mon))
        else:
            fixed_videos = fixed_videos.filter(paid=0)
        return fixed_videos

    @classmethod
    def replace_position_fixed_videos(cls, target_videos, options={}):
        fixed_videos = cls.get_fixed_videos(IphoneFixedPositionVideo, options)
        if not fixed_videos:
            return target_videos
        return cls.position_fixed_videos_replace_processor(target_videos, fixed_videos)


class IpadFixedPositionVideo(FixedPositionVideo):
    @classmethod
    def replace_position_fixed_videos(cls, target_videos, options={}):
        fixed_videos = cls.get_fixed_videos(IpadFixedPositionVideo, options)
        if not fixed_videos:
            return target_videos
        return cls.position_fixed_videos_replace_processor(target_videos, fixed_videos)

    def add_url_type_fields(self, params):
        self.url = params.get("url", '')
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        # DO NOT SAVE HERE
        # self.save()

    def update_url_type_fields(self, params):
        self.url = params.get("url", "")
        self.title = params.get("title", "")
        self.subtitle = params.get("subtitle", "")
        self.intro = params.get("intro", "")
        self.h_image = params.get("h_image", "")
        self.v_image = params.get("v_image", '')
        self.s_image = params.get("s_image", '')
        self.save()