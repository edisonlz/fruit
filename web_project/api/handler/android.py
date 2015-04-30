#coding=utf-8
from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler, CachedPlusHandler

from app.content.models import *
import logging

from wi_model_util.imodel import get_object_or_none


def strip_attrs(obj, attrs):
    ret = {}
    for attr in attrs:
        try:
            val = getattr(obj, attr)
        except Exception, e:
            continue
        else:
            ret[attr] = val
    return ret


#TODO: this api is very slow
@handler_define
class AndroidHomePage(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '4.4'),
            'device_type': self.get_argument('device_type', 'phone'),
            'show_video_list': self.get_argument('show_video_list', '0'),
            'show_paid_video': self.get_argument('show_paid_video', '0'),
            'show_slider': self.get_argument('show_slider', '0'),
            'show_game_information': self.get_argument('show_game_information', '0'),
            'show_live_broadcast': self.get_argument('show_live_broadcast', '0'),
        }

    @api_define("Android Home", r"/interface/android_v3/contents", [
        Param('ver', False, str, '4.4', '4.4', u'版本号'),
        Param('device_type', False, str, 'phone', 'phone', u'设备类型'),
        #Param('pid', False, str, '', '', u'pid'),
        Param('show_video_list', False, str, '1', '', u'show_video_list'),
        Param('show_paid_video', False, str, '1', '', u'show_paid_video'),
        Param('show_slider', False, str, '1', '', u'show_slider'),
        Param('show_game_information', False, str, '1', '', u'show_game_information'),
        Param('show_live_broadcast', False, str, '1', '', u'show_live_broadcast'),
    ], description="Android的首页视频(4.4+,4.4-)")
    @api_define("Android Home", r"/interface/android_v3/contents.json", [
        Param('ver', False, str, '4.4', '4.4', u'版本号'),
        Param('device_type', False, str, 'phone', 'phone', u'设备类型'),
        #Param('pid', False, str, '', '', u'pid'),
        Param('show_video_list', False, str, '1', '', u'show_video_list'),
        Param('show_paid_video', False, str, '1', '', u'show_paid_video'),
        Param('show_slider', False, str, '1', '', u'show_slider'),
        Param('show_game_information', False, str, '1', '', u'show_game_information'),
        Param('show_live_broadcast', False, str, '1', '', u'show_live_broadcast'),
    ], description="Android的首页视频(4.4+,4.4-)")
    def get(self):

        ver = self.get_argument('ver', '3.0')
        device_type = self.get_argument('device_type', 'phone')
        params = {'ver': ver, 'device_type': device_type}

        if ver >= '4.4':
            result = self.index_page_contents_for_v4_4(params)
            return self.write(result)

        # for ver < '4.4':
        is_show_video_list = (self.get_argument('show_video_list', '0') == '1')
        is_show_paid_video = (self.get_argument('show_paid_video', '0') == '1')
        is_show_slider = (self.get_argument('show_slider', '0') == '1')
        is_show_game_information = (self.get_argument('show_game_information', '0') == '1')
        is_show_live_broadcast = (self.get_argument('show_live_broadcast', '0') == '1')

        pid = self.get_argument('pid', '')
        for_phone = (device_type == 'phone')

        json = AndroidHomePublishedVideo().api_columns({
            'show_video_list': is_show_video_list,
            'show_paid_video': is_show_paid_video,
            'for_phone': for_phone,
            'show_slider': is_show_slider,
            'show_game_information': is_show_game_information,
            'show_live_broadcast': is_show_live_broadcast,
            'ver': ver
        })
        json['thumbnail'] = ''

        return self.write(json)

    @classmethod
    def index_page_contents_for_v4_4(cls, params):

        columns = HomeBox.objects.filter(platform=1, state=1, is_delete=0).exclude(
            box_type=BoxType.to_i('under_slider')).order_by('-position')
        result = []

        for column in columns:
            if column.box_type == BoxType.to_i('slider'):
                res = cls.slider_details_for_interface(column, params)
            else:
                limit = cls.video_count_in_layout(column, params)
                contents = AndroidHomePublishedVideo.objects.filter(box_id=column.id, state=1, is_delete=0).order_by(
                    '-position')[:limit]
                tags = []
                videos = []
                normal_tags = cls.tags_for_more_link(column)
                for tag in normal_tags:
                    tags.append(tag.details_for_interface())
                for content in contents:
                    videos.append(content.details_for_interface(params))
                res = {
                    'column_id': column.box_id_for_android_api,
                    'is_youku_channel': column.is_youku_channel,
                    'title': column.title,
                    'image': column.image,
                    'image_link': column.image_link,
                    'cid': '',
                    'jump_info': cls.jump_info_for_interface(column),
                    'tags': tags,
                    'layout': cls.get_layout(column),
                    'card_type': cls.card_type_for_interface(column),
                    'videos': videos,
                }
                title_tag_info = cls.jump_info_for_interface(column)
                if title_tag_info['type'] == 'jump_to_channel':
                    cid = title_tag_info['cid']
                    res.update({'cid': cid})
            result.append(res)
        return result

    @classmethod
    def slider_details_for_interface(cls, column, params):
        slider_contents = AndroidHomePublishedVideo.objects.filter(box_id=column.id, state=1, is_delete=0).order_by(
            '-position')[:5]
        under_slider_column = get_object_or_none(HomeBox, platform=1, state=1, is_delete=0,
                                                 box_type=BoxType.to_i('under_slider'))
        if under_slider_column:
            under_slider_contents = AndroidHomePublishedVideo.objects.filter(box_id=under_slider_column.id, state=1,
                                                                             is_delete=0).order_by('-position')[:4]
        else:
            under_slider_contents = []

        column_contents = {'column_id': column.box_id_for_android_api,
                           'is_youku_channel': column.is_youku_channel,
                           'title': column.title,
                           'cid': '',
                           'card_type': cls.card_type_for_interface(column),
                           'slider': [slider_content.details_for_interface(params) for slider_content in
                                      slider_contents],
                           'under_slider': [under_slider_content.details_for_interface(params) for under_slider_content
                                            in under_slider_contents]
        }
        title_tag_info = cls.jump_info_for_interface(column)
        if title_tag_info['type'] == 'jump_to_channel':
            cid = title_tag_info['cid']
            column_contents.update({'cid': cid})
        return column_contents


    @classmethod
    def video_count_in_layout(cls, column, params):
        if not column.platform == Platform.to_i('android'):
            return -1
        if column.video_count_for_phone == 2 and column.video_count_for_pad == 4:
            if params['device_type'] == 'pad':
                return 4
            else:
                return 2
        elif column.video_count_for_phone == 4 and column.video_count_for_pad == 4:
            return 4
        elif column.video_count_for_phone == 8 and column.video_count_for_pad == 8:
            return 8
        else:
            return 4

    @classmethod
    def card_type_for_interface(cls, column):
        if column.box_type == BoxType.to_i('slider'):
            return 1
        elif column.video_count_for_phone == 4 and column.video_count_for_pad == 4:
            return 2
        elif column.video_count_for_phone == 8 and column.video_count_for_pad == 8:
            return 3
        else:
            return 4

    @classmethod
    def jump_info_for_interface(cls, column):
        tag = cls.tag_for_column_title(column) or AndroidHomeBoxTag(tag_type='title', jump_type=TagType.to_i('no_jump'),
                                                                    title=column.title)
        return tag.details_for_interface()

    @classmethod
    def tag_for_column_title(cls, column):
        try:
            box_tag = AndroidHomeBoxTag.objects.get(is_delete=False, box_id=column.id, tag_type='title')
        except Exception, e:
            box_tag = None

        return box_tag

    @classmethod
    def tags_for_more_link(cls, column):
        try:
            box_tags = AndroidHomeBoxTag.objects.filter(is_delete=False, box_id=column.id, tag_type='normal')[:3]
        except Exception, e:
            box_tags = []

        return box_tags

    @classmethod
    def get_layout(cls, column):
        """
        v4.4+ android首页通过视频个数来确定layout
        """
        if column.video_count_for_phone == 4 and column.video_count_for_pad == 4:
            return '4+0'
        elif column.video_count_for_phone == 4 and column.video_count_for_pad == 8:
            return '4+4'
        elif column.video_count_for_phone == 2 and column.video_count_for_pad == 4:
            return '2+2'
        else:
            return '2+2'

    @classmethod
    def get_box_id_for_api(cls, box):
        box_type = BoxType.to_s(box.box_type)
        #一些类型抽屉的box_id字段要写死 用于API判断抽屉类型
        if box_type in HomeBox.STATIC_BOX_ID.keys():
            return HomeBox.STATIC_BOX_ID[box_type]
        else:
            return box.id


@handler_define
class AndroidChannelManage(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '4.4'),
            'channel_id': self.get_argument('channel_id', '0'),
        }

    @api_define("Android Channel", r"/interface/android_v3/channel_contents", [
        Param('channel_id', False, str, '', '', u'频道id'),
        Param('ver', False, str, '', '', u'版本号'),
        Param('pid', False, str, '', '', u'pid'),
    ], description="Android频道内容接口(频道管理中专题精编的类型为video_list的内容接口)")
    @api_define("Android Channel", r"/interface/android_v3/channel_contents.json", [
        Param('channel_id', False, str, '', '', u'频道id'),
        Param('ver', False, str, '', '', u'版本号'),
        Param('pid', False, str, '', '', u'pid'),
    ], description="Android频道内容接口(频道管理中专题精编的类型为video_list的内容接口)")
    def get(self):
        channel_id = int(self.get_argument('channel_id', 0))
        ver = self.get_argument('ver', '')
        not_show_paid_video = True if (not ver) or ver < '3.4' else False
        channel = get_object_or_none(AndroidChannel, is_delete=0, state=1, id=channel_id,
                                     content_type=AndroidChannel.CONTENT_TYPE_OF_TOPIC)
        if not channel:
            return self.write({'results': []})
        channel_video = get_object_or_none(AndroidChannelVideo, is_delete=0, state=1, channel_id=channel.id)
        if not channel_video:
            return self.write({'results': []})
        contents = AndroidVideoListVideo.objects.filter(is_delete=0, state=1, module_id=channel_video.video_list_id)
        if not_show_paid_video:
            contents = contents.filter(paid=0)
        contents = contents.order_by('-position').order_by('id')

        json = self.content_hash(contents)
        return self.write({"results": json})

    def content_hash(self, contents):
        results = []
        for content in contents:
            result = {
                'content_id': content.video_id,
                'content_type': str(content.video_type),
                'title': content.title,
                'image': content.h_image,
                'pv': content.pv,
                'paid': content.paid
            }
            if content.video_type == VideoType.to_i('url'):
                result['url'] = content.url

            results.append(result)
        return results


@handler_define
class Navigation(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {}

    @api_define("Android Channel", r"/interface/android_v3/channel_navigations", [
    ], description="Android频道导航接口")
    @api_define("Android Channel", r"/interface/android_v3/channel_navigations.json", [
    ], description="Android频道导航接口")
    def get(self):
        nav_set = AndroidChannelNavigation.objects.filter(is_delete=0, state=1).order_by('-position')
        nav_infos = [self.details_of_nav(nav) for nav in nav_set]
        self.write({'results': nav_infos})

    @staticmethod
    def details_of_nav(nav):
        return {'title': nav.title, 'navigation_id': nav.id}


@handler_define
class AndroidSubChannels(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'cid': self.get_argument('cid', '3.5'),
        }

    @api_define("Android SubChannels", r'/interface/android_v3/sub_channels.json', [
        Param('cid', True, int, '1', '1', u'cid'),
    ], description="子频道列表 Android3.5+")
    @api_define("Android SubChannels", r'/interface/android_v3/sub_channels', [
        Param('cid', True, int, '1', '1', u'cid'),
    ], description="子频道列表 Android3.5+")
    def get(self):
        cid = self.get_argument('cid', 1)
        channel = AndroidChannel.objects. \
            filter(content_type=AndroidChannel.CONTENT_TYPE_OF_ORIGIN, cid=cid).first()
        if not channel:
            return self.write({'results': {}})
        sub_channels = AndroidSubChannel.objects. \
            filter(channel_id=channel.id, state=1, is_delete=False).order_by('position')
        results = [sub_channel.interface_information for sub_channel in sub_channels]
        self.write({'results': results})


@handler_define
class AndroidSubChannelDetails(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'sub_channel_id': self.get_argument('sub_channel_id', '1'),
            'ver': self.get_argument('ver', '3.0'),
        }

    @api_define("Android SubChannel Details", r'/interface/android_v3/sub_channel_details.json', [
        Param('sub_channel_id', True, int, 0, 0, u'sub_channel_id'),
        Param('ver', True, str, '3.0', '3.0', u'ver'),
        Param('show_game_information', True, int, 0, 0, u'show_game_information')  #会插入固定位置视频
    ], description="子频道列表详情 Android3.5+")
    @api_define("Android SubChannel Details", r'/interface/android_v3/sub_channel_details', [
        Param('sub_channel_id', True, int, 0, 0, u'sub_channel_id'),
        Param('ver', True, str, '3.0', '3.0', u'ver'),
        Param('show_game_information', True, int, 0, 0, u'show_game_information')  #会插入固定位置视频
    ], description="子频道列表详情 Android3.5+")
    def get(self):
        sub_channel_id = self.get_argument('sub_channel_id', '')
        ver = self.get_argument('ver', '3.0')
        is_show_game = self.get_argument('show_game_information', 0) == '1'
        if len(sub_channel_id) < 1:
            return self.write({})

        sub_channel = get_object_or_none(AndroidSubChannel, pk=sub_channel_id)

        if not sub_channel:
            return self.write({})

        result = sub_channel.details_for_interface({'ver': ver, 'is_show_game': is_show_game})
        self.write(result)


@handler_define
class AndroidChannels(CachedPlusHandler):
    def get_varnish_expire(self):
        return 2

    def get_cache_expire(self):
        return 2

    def get_cache_key(self):
        return {
            'type': self.get_argument('type', '0'),
            'ver': self.get_argument('ver', '3.0'),
        }

    @api_define("Android Channels", r'/interface/android_v3/channels.json', [
        Param('type', False, int, 0, 0, u'频道类型'),
        Param('ver', False, str, '3.0', '3.0', u'版本号'),
    ], description="安卓频道接口")
    def get(self):
        type = int(self.get_argument('type', 0))
        type = 1 if type == 0 else 2  # 老接口中type字段－0优酷频道，1专题精编，新系统库－1优酷频道，2专题精编
        channels = AndroidChannel.objects.filter(content_type=type, state=1, is_delete=False).order_by('-position')
        results = [self.channel_info(channel) for channel in channels]
        self.write({'results': results})

    def channel_info(self, channel):
        channel_id = self.channel_id_for_api(channel)
        content_type = self.content_type_for_api(channel)

        return {
            'channel_id': channel.cid,
            'title': channel.title,
            'color': channel.color,
            'icon': channel.icon_bg,
            'like_icon': channel.icon,
            'daci_content': '',  # TODO 新系统没有这个字段，待定
            'content_type': content_type,
            'playlist_first_video_id': self.playlist_first_video_id(channel, channel_id, content_type),
        }

    def playlist_first_video_id(self, channel, channel_id, content_type):
        ret = ""
        if content_type == VideoType.to_i('video_list'):
            try:
                playlist_first_video = AndroidVideoListVideo.objects.filter(module_id=channel_id, state=1,
                                                                            is_delete=False).order_by('position')[0]
                ret = playlist_first_video.video_id
            except Exception, e:
                print e
                logging.error(e)
                return ret

        return ret

    @staticmethod
    def content_type_for_api(channel):
        default_content_type = 1
        if channel.show_type == AndroidChannel.SHOW_TYPE_OF_VIDEO:
            try:
                first_video = AndroidChannelVideo.objects.get(channel_id=channel.id, state=1, is_delete=False)
            except AndroidChannelVideo.DoesNotExist:
                return default_content_type
            return first_video.video_type
        else:
            return default_content_type

    @staticmethod
    def channel_id_for_api(channel):
        ret = channel.id
        if channel.show_type == AndroidChannel.SHOW_TYPE_OF_VIDEO:
            try:
                first_video = AndroidChannelVideo.objects.get(channel_id=channel.id, state=1, is_delete=False)
            except AndroidChannelVideo.DoesNotExist, e:
                print e
                logging.error(e)
                return ret
            if first_video.video_type == VideoType.to_i('video_list'):
                ret = first_video.video_list_id
        return ret



@handler_define
class AndroidSearchBackImg(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    # def get_cache_key(self):
    #     return {
    #     }

    @api_define("android search back img", r'/interface/android_v3/search_background_videos', [
    ], description='android4.2+搜索背景图')
    @api_define("android search back img", r'/interface/android_v3/search_background_videos.json', [
    ], description='android4.2+搜索背景图')
    def get(self):
        videos_for_phone = SearchBackgroundVideo.objects.filter(is_delete=0, state=1, device_type='phone')
        videos_for_pad = SearchBackgroundVideo.objects.filter(is_delete=0, state=1, device_type='pad')
        print "videos_for_phone:-videos_for_pad:-", videos_for_phone, videos_for_pad
        if not videos_for_phone and not videos_for_pad:
            result = {}
            return self.write(result)

        if videos_for_phone and videos_for_pad:
            video_for_phone = videos_for_phone[0]
            video_for_pad = videos_for_pad[0]
        elif videos_for_phone:
            video_for_phone = videos_for_phone[0]
            video_for_pad = None
        elif videos_for_pad:
            video_for_phone = None
            video_for_pad = videos_for_pad[0]
        result = map(AndroidSearchBackImg.video_details_for_interface, [video_for_phone, video_for_pad])
        return self.write(result)

    @staticmethod
    def video_details_for_interface(video):
        if video.video_list_id > 0:
            return AndroidSearchBackImg.video_list_for_interface(video)
        res = {
            'device_type': video.device_type,
            'content_id': video.video_id,
            'content_type': str(video.video_type),
            'title': video.title,
            'image': video.h_image,
            'intro': video.intro,
            'url': video.url,
            'paid': video.paid,
            'playlist_videoid': ''
        }

        if VideoType.to_s(video.video_type) == 'playlist':
            res['playlist_videoid'] = video.first_episode_video_id

        if VideoType.to_s(video.video_type) in ['game_list', 'game_download', 'game_details']:
            game_app_id = video.game_id
            res['game_info'] = AndroidHomePublishedVideo().game_information_hash(game_app_id)
            res['second_title'] = video.subtitle

        return res

    @staticmethod
    def video_list_for_interface(video):
            return {
                'content_type': str(video.video_type),
                'content_id': video.video_list_id,
                'title': video.title,
                'image': video.h_image,
                'intro': video.intro,
                'playlist_videoid': '',
                'url': '',
                'second_title': video.subtitle
            }






