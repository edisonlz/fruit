#coding=utf-8
from django.db import models
from wi_cache.base import CachingManager
from app.content.models import BaseVideo, BaseHomeBox, VideoType, Platform
from app.content.lib.model_util import ModelUtil
from app.content.models.main_page_video import AndroidBoxVideo, IpadBoxVideo, IphoneBoxVideo, WinPhoneBoxVideo
from app.content.models.main_page_module import HomeBox
from django.db.models import Max
from redis_model.queue import Client


class HomeCommonBox(BaseHomeBox):
    platform_dict = {1: AndroidBoxVideo, 2: IpadBoxVideo, 3: IphoneBoxVideo, 4: WinPhoneBoxVideo}
    MaxVideoCountInBox = 100
    MaxPositionInBox = 1000000
    queue_client = Client()

    def sync_box_videos(self, video_ids):
        """
        @desc:同步公共视频
        @params: video_ids(sync video list)
        """

        #1.获取绑定公共模块的盒子
        override_boxes = HomeBox.objects.filter(is_delete=False, attached_common_id=self.id)

        for override_box in override_boxes:
            sync_videos = HomeCommonVideo.objects.filter(id__in=video_ids).order_by('-position')

            #2.反射获对于的类
            # TODO: 这里应该有处理各个平台的逻辑吧,同一个box里的内容可以被同步到不同平台
            sync_video_class = HomeCommonBox.platform_dict[override_box.platform]
            current_videos_max_position = sync_video_class.get_max_box_position(override_box)
            new_max_position = current_videos_max_position + 1

            #3.更新视频和视频顺序
            for index, sync_video in enumerate(reversed(sync_videos)):
                sync_video.sync_video(override_box, new_max_position + index)

            #4.清理历史数据
            HomeCommonBox.queue_client.dispatch("cache.do_clean_box", {
                # TODO: 这里的box_id不对吧？
                "box_id": override_box.id,
                "box_class": HomeBox.__name__,
                "video_class": sync_video_class.__name__,
                "max_position_for_each_box": HomeBox.MaxPositionInBox,
                "max_video_count_for_each_box": HomeBox.MaxVideoCountInBox, })

        return {'status': 'success'}


    


class HomeCommonVideo(BaseVideo):
    box = models.ForeignKey(HomeCommonBox, verbose_name='模块 ID')

    @classmethod
    def existed_sync_video(cls, box, box_video):
        publish_video_class = HomeCommonBox.platform_dict[box.platform]
        video_type = VideoType.to_s(box_video.video_type)
        return publish_video_class.get_exist_home_video(video_type, publish_video_class, box, box_video)



    def sync_video(self, box, new_position):
        """
        将公用模块视频同步到指定抽屉的指定位置
        """
        video_class = HomeCommonBox.platform_dict[box.platform]
        existed_video = HomeCommonVideo.existed_sync_video(box, self)
        if existed_video:
            sync_video = existed_video
            sync_video.position = new_position
        else:
            sync_video = video_class()
            sync_video.position = new_position
            sync_video.box_id = box.id

        sync_video = self.sync_video_details(target_video=sync_video)
        sync_video.save()

    def sync_video_details(self, target_video):
        target_video.title = self.title
        target_video.intro = self.intro
        target_video.subtitle = self.subtitle
        target_video.v_image = self.v_image
        target_video.h_image = self.h_image
        target_video.s_image = self.h_image
        #因为推荐池视频里轮播图与普通图都存在h_image字段
        #同步时需调整。
        target_video.video_id = self.video_id
        target_video.video_type = self.video_type
        target_video.paid = self.paid
        target_video.pay_type = self.pay_type
        target_video.has_copyright = self.has_copyright
        target_video.url = self.url
        target_video.first_episode_video_id = self.first_episode_video_id
        target_video.first_episode_video_pv = self.first_episode_video_pv
        target_video.image_size = self.image_size
        target_video.game_id = self.game_id
        target_video.attached_game_type = self.attached_game_type
        target_video.game_page_id = self.game_page_id
        target_video.pgc_uid = self.pgc_uid
        return target_video


    @classmethod
    def video_type_supports(cls):
        #实际支持的类型
        return ( 'video', 'show', 'playlist', 'url', 'live_broadcast')

    @classmethod
    def video_type_mocks(cls):
        #页面上不显示的类型
        return ('show', 'playlist', )

    @classmethod
    def video_types(cls, mock=False):
        types = list(cls.video_type_supports())
        if mock:
            mocks = cls.video_type_mocks()
            types = filter(lambda x: x not in mocks, types)
        return VideoType.platformization(Platform.to_i('ipad'), types)
    
    def check_video_type(self, mock=False):
        return HomeCommonVideo.video_types(mock).has_key(self.video_type)

