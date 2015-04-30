# coding=utf-8
from app.content.models import *
from view.api_doc import handler_define, api_define, Param
from api.view.base import BaseHandler, CachedPlusHandler
from api.handler.winphone_data import all_sub_channels, all_channels


class WinphoneIndexPageBase(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def box_contents(self, box, ver):
        if Platform.to_s(box.box_type) == 'slider' and ver < '3.3':
            slider_videos = IphoneBoxVideo.objects.filter(box=box, state=1).order_by('-position').first()
            choiceness_box = HomeBox.objects.filter(platform=Platform.to_i('iphone'), state=1, is_delete=False,
                                                    box_type=BoxType.to_i('under_slider'))
            if choiceness_box:
                choiceness_videos = IphoneBoxVideo.objects.filter(box=choiceness_box, state=1, is_delete=False). \
                                        order_by('-position')[:choiceness_box.video_count_for_phone]
                videos = slider_videos + choiceness_videos
            else:
                videos = slider_videos
        else:
            videos = IphoneBoxVideo.objects.filter(box=box, state=1, is_delete=False). \
                         order_by('-position')[:box.video_count_for_phone]
        return {'results': [self.convert_video(video, ver) for video in videos]}

    @staticmethod
    def convert_video(video, ver):
        video_info = {
            'content_id': video.video_id,
            'title': video.title,
            'content_type': VideoType.to_s(video.video_type),
            'img': video.h_image,
            'intro': video.intro,
            'url': video.url
        }
        if VideoType.to_s(video.video_type) == 'playlist':
            video_info['first_episode_video_id'] = video.first_episode_video_id
        return video_info

    def boxes_information(self, ver):
        boxes = HomeBox.objects.filter(platform=Platform.to_i('iphone'), state=1, is_delete=False).order_by('-position')
        if ver < '3.3':
            boxes = boxes.exclude(box_type=BoxType.to_i('under_slider'))

        results = []
        for box in boxes:
            tmp = {
                'title': box.title,
                'cid': box.cid,
                'contents': self.box_contents(box, ver),
            }
            if ver >= '3.3':
                tmp['is_slider'] = 1 if BoxType.to_s(box.box_type) == 'slider' else 0
            results.append(tmp)
        return results


@handler_define
class WinphoneIndexPage(WinphoneIndexPageBase):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '1.0')
        }

    @api_define("Winphone Index", r'/interface/windows_phone/index_page', [
        Param('ver', False, str, '1.0', '1.0', '版本号'),
    ], description='WinPhone首页接口')
    @api_define("Winpad Index", r'/interface/windows_pad/index_page', [
        Param('ver', False, str, '1.0', '1.0', '版本号'),
    ], description='WinPad首页接口')
    # 实际上win pad接口是没有ver参数的，不过这里可以预留
    def get(self):
        ver = self.get_argument('ver', '1.0')
        results = self.boxes_information(ver)
        self.write({'results': results})


@handler_define
class Wp8IndexPage(WinphoneIndexPageBase):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.3')
        }

    @api_define("Winphone8.1 Index", r'/interface/wp8/index_page', [
        Param('ver', False, str, '3.3', '3.3', '版本号'),
    ], description='WinPhone8.1首页接口')
    def get(self):
        ver = self.get_argument('ver', '3.3')
        results = self.boxes_information(ver)
        self.write({'results': results})


@handler_define
class WinphoneChannelPage(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'channel_id': self.get_argument('channel_id', '96'),
            'ver': self.get_argument('ver', '1.0')
        }

    @api_define("Winphone Channel Page", r'/interface/windows_phone/channels_page', [
        Param('channel_id', True, int, '96', '96', '频道ID'),
        Param('ver', True, str, '1.0', '1.0', '版本号'),
    ], description='WinPhone频道页')
    # 这个接口实际上没有ver这个参数，不过可以先预留
    def get(self):
        ret = dict()
        cid = self.get_argument('channel_id')
        channel = IphoneChannel.objects.filter(cid=cid, state=1, is_delete=False).first()
        if channel:
            if channel.choiceness_type_sub_channel:
                modules = channel.choiceness_type_sub_channel.module.filter(module_type=0, state=1, is_delete=False). \
                    order_by('-position')
                modules_and_videos = [self.get_module_info(module) for module in modules]
                ret['modules_and_videos'] = modules_and_videos
            ret['rank'] = []

        self.write(ret)

    def get_module_info(self, module):
        valide_video_types = [Platform.to_i(type) for type in ['video', 'show', 'playlist', 'url']]
        videos = module.moduleVideo.filter(state=1, is_delete=False, video_type__in=valide_video_types).order_by(
            '-position')[:50]
        return {
            'title': module.title,
            'module_id': module.id,
            'videos': [self.get_video_info(video) for video in videos]
        }

    @staticmethod
    def get_video_info(video):
        video_type = VideoType.to_s(video.video_type)
        ret = {
            'video_id': video.video_id,
            'title': video.title,
            'intro': video.intro,
            'video_type': video_type,
            'width_img': video.h_image,
            'height_img': video.v_image
        }
        if video_type == 'playlist':
            ret['first_episode_video_id'] = video.first_episode_video_id
        return ret


@handler_define
class WinphoneSubchannelPage(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'channel_id': self.get_argument('channel_id', '96'),
            'ver': self.get_argument('ver', '3.3')
        }

    @api_define("WinPhone SubChannel Page", r'/interface/windows_phone/sub_channels', [
        Param('channel_id', True, int, '96', '96', '频道ID'),
        Param('ver', True, str, '3.3', '3.3', '版本号'),
    ], description='WinPhone子频道页')
    # 这个接口实际上没有ver这个参数，不过可以先预留
    def get(self):
        ret = {}
        cid = int(self.get_argument('channel_id'))
        sub_channels = []
        for sub_channel in all_sub_channels:
            if sub_channel['cid'] == cid and sub_channel['state'] == 1:
                sub_channels.append({
                    'title': sub_channel['title'],
                    'filter_keys': sub_channel['filter'],
                    'image_type': sub_channel['image_type']
                })
        if sub_channels:
            ret['cid'] = cid
            ret['sub_channels'] = sub_channels
            ret['comment'] = ""
            for channel in all_channels:
                if channel['cid'] == cid:
                    ret['channel_title'] = channel['title']

        self.write(ret)