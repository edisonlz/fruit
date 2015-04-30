#coding=utf-8
from django.db import models
from base_video import BaseVideo
from platform import Status
from app.content.models import BrandModule
from wi_cache.base import CachingManager
from app.content.models import Platform, VideoType, AndroidGame
from app.content.lib.model_util import ModelUtil

class BrandVideo(BaseVideo):

    objects = CachingManager()

    state_for_android = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    state_for_iphone = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    state_for_ipad = models.IntegerField(verbose_name=u"状态(开/关)", choices=Status.STATUS, default=0, db_index=True, max_length=2)
    brand_module = models.ForeignKey(BrandModule, verbose_name='品牌模块ID')


    @classmethod
    def video_type_supports(cls):
        #支持的类型
        return (
            'video',
            'url',
            'user',
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

    #overrided from base_video
    def add_game_download_type_fields(self, params):

        game_class = AndroidGame
        new_game = game_class.create_or_update(params)
        self.game_id = new_game.id
        self.title = params.get("title", '')
        self.h_image = params.get("h_image", '')
        # DO NOT SAVE HERE
        # self.save()

    #overrided from base_video
    def update_game_download_type_fields(self, params):

        game_class = AndroidGame
        game = game_class.create_or_update(params)
        self.game_id = game.id
        self.title = params.get("title", "")
        self.h_image = params.get("h_image", "")
        self.save()

    def add_position(self, box_pk):
        video_sets = self.__class__.objects.defer('position').filter(brand_module_id=box_pk)
        if not video_sets:
            current_box_max_position = 0
        else:
            current_box_max_position = video_sets.order_by("-position")[0].position + 1
        self.position = current_box_max_position


