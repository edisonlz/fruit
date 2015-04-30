#coding=utf-8
from django.db import models
from base_video import BaseVideo, AndroidGame
from platform import VideoType
from wi_cache.base import CachingManager


class SearchBackgroundVideo(BaseVideo):
    objects = CachingManager()
    live_broadcast_url = models.CharField(max_length=255, verbose_name='直播url', default='')
    device_type = models.CharField(max_length=100, verbose_name=u'设备类型(phone/pad)', default='')
    video_list_id = models.IntegerField(verbose_name='VIDEO LIST ID', default=0)

    class Meta:
        app_label = "content"


    @classmethod
    def video_type_supports(cls):
        #支持的类型
        return (
            'video',
            'url',
            'live_broadcast',
            'video_list',
            'game_list',
            'game_download',
            'game_details',
        )

    @classmethod
    def video_types(cls):
        types = list(cls.video_type_supports())
        print "types:============", types
        res = []
        for type in types:
            for key in VideoType.KEYS:
                if key.get("name") == type:
                    res.append(key)

        return res


    def update_video_list_type_fields(self, params):
        self.video_list_id = int(params.get("video_list_id", 0))
        self.title = params.get("title")
        self.sub_title = params.get("sub_title")
        self.info = params.get("info", "")
        self.info = params.get("info", "")
        self.pgc_uid = params.get("pgc_uid")
        self.h_image = params.get("h_image")
        self.save()


    def add_game_download_type_fields(self, params):
        if params['platform'] == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')

        new_game = game_class.create_or_update(params)
        self.game_id = new_game.id
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        self.v_image = params.get("v_image", '')
        self.s_image = params.get('s_image', '')
        # DO NOT SAVE HERE
        # self.save()
        #TODO: add other video_relatived info


    def update_game_download_type_fields(self, params):
        if params['platform'] == 'android':
            game_class = AndroidGame
        else:
            raise Exception('platform not support game_download')

        game = game_class.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.save()


    def add_position(self,):
        video_sets = self.__class__.objects.defer('position')
        if not video_sets:
            current_box_max_position = 0
        else:
            current_box_max_position = video_sets.order_by("-position")[0].position + 1
        self.position = current_box_max_position



