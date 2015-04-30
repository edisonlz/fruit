#coding=utf-8
from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler, CachedPlusHandler

from app.content.models import *
import logging

from wi_model_util.imodel import get_object_or_none

@handler_define
class BrandWebsite(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'platform': self.get_argument('platform', ''),
            'device_type': self.get_argument('device_type', ''),
            'sub_channel_id': self.get_argument('sub_channel_id', ''),
        }

    @api_define("Brand website", r"/interface/marketing/brands", [
        Param('platform', True, str, '', 'android', u'平台(android/iphone/ipad)'),
        Param('device_type', True, str, '', 'phone', u'设备'),
        Param('sub_channel_id', True, str, '', '22', u'子频道id'),
    ], description="品牌官网头频道抽屉")

    def get(self):
        params_initial = self.request.arguments
        result = {}
        if params_initial.has_key('platform') and params_initial.has_key('device_type') and params_initial.has_key('sub_channel_id'):
            params={'platform': params_initial['platform'][0], 'device_type': params_initial['device_type'][0], 'sub_channel_id':params_initial['sub_channel_id'][0]}
            platform = self.inside_platform(params)
            if not platform:
                return self.write(result)
            sub_channel_id = int(params['sub_channel_id'])
            where_state = {}
            where_state['state_for_%s'%platform] = 1
            where_sub_channel_id = {}
            where_sub_channel_id['subchannel_id_of_%s'%platform] = sub_channel_id
            brand_modules = BrandModule.objects.filter(**where_state).filter(**where_sub_channel_id).order_by('-id')
            #brand_modules = BrandModule.objects.filter(**where_state)
            #brand_modules.filter(**where_sub_channel_id).order_by('-id')
            if not brand_modules:
                return self.write(result)
            else:
                brand_module = brand_modules[0]
                videos = BrandVideo.objects.filter(brand_module_id = brand_module.id ,**where_state)
                if not params['platform'] == 'android':
                    videos = videos.exclude(video_type=VideoType.to_i('game_list'))
                    videos = videos.exclude(video_type=VideoType.to_i('game_download'))
                    videos = videos.exclude(video_type=VideoType.to_i('game_details'))
                #videos = videos.order_by('-position')
                result = {
                    'title':brand_module.title,
                    'link_to_url':brand_module.link_to_url,
                    'sub_channel_id_for_link': '',
                    'brands': [self.details_for_interface(video) for video in videos]
                }
                return self.write(result)
        else:
            return self.write(result)


    @staticmethod
    def details_for_interface(video):
        information = {
            'title': video.title,
            'sub_title': video.subtitle,
            'image': video.h_image,
            'content_type': BrandWebsite.content_type_for_interface(video),
            'content_id': video.video_id
        }
        if video.video_type == VideoType.to_i('playlist'):
            information['first_episode_video_id'] = video.first_episode_video_id or ''
        if video.video_type == VideoType.to_i('url'):
            information['url'] = video.url
        if video.video_type in [VideoType.to_i('game_list'), VideoType.to_i('game_download'), VideoType.to_i('game_details')]:
            information['game_information'] = BrandWebsite.game_information_hash(video)

        return information

    @staticmethod
    def game_information_hash(video):
        game_application = get_object_or_none(AndroidGame, pk=video.game_id)
        if not game_application:
            return {}
        game_id = game_application.original_game_id
        game_type = 'unknown'
        if video.video_type == VideoType.to_i('game_list'):
            game_type = 'show_list'
        elif video.video_type == VideoType.to_i('game_download'):
            game_type = 'download_game'
        elif video.video_type == VideoType.to_i('game_details'):
            game_type = 'show_details'

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
            'game_class_name': game_application.category_name
        }


    @staticmethod
    def content_type_for_interface(video):
        if video.video_type == VideoType.to_i('video'):
            return 'video'
        elif video.video_type == VideoType.to_i('show'):
            return 'show'
        elif video.video_type == VideoType.to_i('playlist'):
            return 'playlist'
        elif video.video_type == VideoType.to_i('url'):
            return 'url'
        elif video.video_type in [VideoType.to_i('game_list'), VideoType.to_i('game_download'), VideoType.to_i('game_details')]:
            return 'game'
        elif video.video_type == VideoType.to_i('user'):
            return 'user'

    @staticmethod
    def inside_platform(params):
        if params['platform'] =='android':
            return 'android'
        elif params['platform'] == 'ios':
            if params['device_type'] == 'phone':
                return 'iphone'
            elif params['device_type'] == 'pad':
                return 'ipad'
        else:
            return ''
