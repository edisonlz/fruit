#coding=utf-8

from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler,CachedPlusHandler

from wi_cache import function_cache

@handler_define
class VideoService(BaseHandler):
    @api_define("VideoInfo", r'/service', [
        Param('vid', True, str, "XNTEzODEzNzky", "XNTEzODEzNzky", u'video id'),
        ], description="获取视频信息")
    def get(self):
        info = self.get_video(self.arg("vid"))
        self.write(info)


    @function_cache(cache_keys="vid",
                    prefix='video_service:',
                    expire_time=60 * 2)
    def get_video(self,vid):
        from base.youkuapi.video import VideoApi
        return VideoApi.get_video_info(vid)

        