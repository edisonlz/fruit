#!/usr/bin/env python
# -*- coding: utf-8 -*-
from base.youkuapi.playlist import PlaylistApi
from base.youkuapi.show import ShowApi
from base.youkuapi.video import VideoApi
from app.content.models.platform import VideoType


def youku_video_info_from_web(video_id, video_type):
    if video_type == VideoType.to_i('playlist'):
        return PlaylistApi.get_playlist_info(video_id)
    elif video_type == VideoType.to_i('video'):
        return VideoApi.get_video_info(video_id)
    elif video_type == VideoType.to_i('show'):
        return ShowApi.get_show_info(video_id)
    else:
        return {}


def get_video_type(video_id):
    import re

    pat = re.compile(r'^\d+$')
    if video_id.startswith('X'):
        return 'video'
    elif video_id.startswith('z'):
        return 'show'
    elif pat.match(video_id):
        return 'playlist'
    else:
        return 'unknown'


if __name__ == '__main__':
    print get_video_type('090ec930b26611e3a705')