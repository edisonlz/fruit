# coding=utf-8
from view.api_doc import handler_define, api_define, Param
from api.view.base import BaseHandler, CachedPlusHandler
from app.content.models import *
from django.db.models import Q, Max
from datetime import datetime
import time


class IphoneBoxContentBase(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    CLIENT_TYPE_PAD = 'pad'
    CLIENT_TYPE_PHONE = 'phone'

    def api_box_with_slider(self, params):
        boxes = HomeBox.objects.filter(platform=Platform.to_i("iphone"), is_delete=0, state=1).order_by('-position')
        if params['ver'] < '4.1':
            # del game module type from boxes
            boxes = boxes.exclude(box_type=BoxType.to_i('game'))
        result = [self.details_of_box(box=box, params=params) for box in boxes]
        return result

    def details_of_box(self, box, params):
        limit = box.video_count_for_pad if params['client_type'] == self.CLIENT_TYPE_PAD \
            else box.video_count_for_phone
        box_contents = {
            'title': box.title,
            'box_id': self.get_box_id_for_api(box),
            'is_youku_channel': box.is_youku_channel,
            'cid': '',
            'iphone_max_count': box.video_count_for_phone,
            'contents': self.get_box_contents_for_api(box, params, limit),
        }
        title_tag_info = self.get_tag_details(box.id, jump_info=True)
        if title_tag_info['type'] == 'jump_to_channel':
            cid = title_tag_info['cid']
            box_contents.update({'cid':cid})
        if params['ver'] >= '4.1':
            box_contents.update(
                {'image': box.image, 'image_link': box.image_link,
                 'jump_info': title_tag_info,
                 'tags': self.get_tag_details(box.id, tag_info=True)})
        return box_contents

    @staticmethod
    def get_box_contents_for_api(box, params, limit):
        videos = IphoneHomePublishedVideo.objects.filter(box_id=box.id, state=1, is_delete=0).order_by('-position')
        if not params.get('include_url', ''):
            videos = videos.exclude(video_type=VideoType.to_i('url'))
        if not params.get('include_mon_pay_video', ''):
            videos = videos.filter(Q(pay_type=BaseVideo.pay_type.mon) | Q(paid=0))
        if not params.get('include_personal_space', ''):
            videos = videos.exclude(video_type=VideoType.to_i('user'))
        if (not params['ver']) or (params['ver'] < '4.1'):
            videos = videos.exclude(video_type__in=[7, 9])
        if not params.get('include_live_broadcast', ''):
            videos = videos.exclude(video_type=VideoType.to_i('live_broadcast'))

        result = [IphoneBoxContentBase.details_of_video(video, box, params) for video in videos[:limit]]
        return {'results': result}

    @staticmethod
    def get_tag_details(box_id, jump_info=False, tag_info=False):
        box_tags = IphoneHomeBoxTag.objects.filter(is_delete=0, box_id=box_id)
        if jump_info:
            box_tag = box_tags.filter(tag_type='title').first()
            return IphoneBoxContentBase.get_tag_info(box_tag)
        elif tag_info:
            filter_tags = box_tags.filter(tag_type='normal')[:3]
            tag_info_list = [IphoneBoxContentBase.get_tag_info(tag) for tag in filter_tags]
            return tag_info_list


    @staticmethod
    def get_tag_info(box_tag):
        # print 'into get tag info'
        jump_type = TagType.to_s(box_tag.jump_type)
        tag_info = {'type': jump_type, 'title': box_tag.title, }
        if jump_type == 'no_jump':
            tag_info.pop('title')
        if jump_type == 'jump_to_hotword':
            tag_info['hotword'] = box_tag.hot_word
        if jump_type == 'jump_to_channel':
            tag_info['cid'] = str(box_tag.cid) if box_tag.cid > 0 else ''
        if jump_type == 'jump_to_sub_channel':
            sub_channel = IphoneSubChannel.objects.filter(id=box_tag.sub_channel_id).first()
            channel = IphoneChannel.objects.filter(id=sub_channel.channel_id).first()
            tag_info['cid'] = channel.cid or ''
            tag_info['sub_channel_id'] = sub_channel.id or 0
        if tag_info == 'jump_to_game':
            game_app = IosGame.objects.get(id=box_tag.game_id)
            tag_info['game_id'] = game_app.original_game_id
            tag_info['game_itunesid'] = game_app['itunesid']
            tag_info['game_url'] = game_app['url']

        return tag_info

    @staticmethod
    def details_of_video(video, box, params):
        content = {
            'content_id': video.video_id,
            'title': video.title,
            'content_type': VideoType.to_s(video.video_type),
            'img': video.h_image,
            'intro': video.intro,
            'url': video.url,
            'second_title': video.subtitle
        }
        if box.box_type == BoxType.to_i('slider'):
            content['image_2'] = video.s_image
        #not handle box_id is 112 and 113
        content_type = VideoType.to_s(video.video_type)
        if content_type == 'user':
            content['content_id'] = video.video_id
        if content_type == 'playlist':
            if params.get('include_playlist', ''):
                content['first_episode_video_id'] = video.first_episode_video_id
                content['first_episode_pv'] = video.first_episode_video_pv
            else:
                content['content_id'] = video.first_episode_video_id
                content['content_type'] = 'video'
        if video.is_mon_pay_video():
            content['is_mon_pay_video'] = 1

        if content_type == 'live_broadcast':
            content['live_broadcast_url'] = video.live_broadcast_url or ''
            content['live_broadcast_bg_image_3_5'] = video.live_broadcast_bg_image_3_5 or ''
            content['live_broadcast_bg_image_4'] = video.live_broadcast_bg_image_4 or ''
            content['live_broadcast_bg_image_4_7'] = video.live_broadcast_bg_image_4_7 or ''
            content['live_broadcast_bg_image_5_5'] = video.live_broadcast_bg_image_5_5 or ''
        if params['ver'] >= '4.1':
            if IphoneBoxContentBase.need_pgc_uid(video.attached_game_type, content_type):
                content['pgc_uid'] = video.pgc_uid
            if video.game_page_id:
                content['game_page_id'] = video.game_page_id

            game_without_video_flag = \
                IphoneBoxContentBase.type_of_game_without_video(video.attached_game_type, content_type)
            if game_without_video_flag or video.attached_game_type:
                content['game_information'] = IphoneBoxContentBase.get_game_info(video)
                content['game_relation'] = 'attached' if video.attached_game_type else 'standalone'
            if game_without_video_flag:
                # use v_image as game_image
                content['img'] = video.h_image
        return content

    @staticmethod
    def get_game_info(video):
        try:
            game_app = IosGame.objects.get(id=video.game_id)
        except IosGame.DoesNotExist:
            return {}
        else:
            actual_game_type = video.attached_game_type if video.attached_game_type else video.video_type
            game_type_dict = {
                'game_list': 'show_list',
                'game_download': 'download_game',
                'game_details': 'show_details',
            }
            game_type = None
            for k, v in game_type_dict:
                if k == actual_game_type:
                    game_type = v
            if game_type is None:
                game_type = 'unknown'
            return {
                'game_type': game_type,
                'game_id': game_app.original_game_id,
                'game_appname': game_app.appname,
                'game_version': game_app.version,
                'game_itunesid': game_app.itunesid,
                'game_logo': game_app.logo,
                'game_scroller': game_app.scroller,
                'game_score': game_app.score,
                'game_url': game_app.url,
                'game_desc': game_app.desc,
                'game_upload_time': game_app.upload_time,
                'game_size': game_app.size,
                'game_charge': game_app.charge,
                'game_redirect_type': game_app.redirect_type,
                'game_recommend_type': game_app.recommend_type,
                'game_redirect_url': game_app.redirect_url,
            }

    @staticmethod
    def type_of_game_without_video(attached_game_type, content_type):
        if (not attached_game_type) and content_type in ['game_list', 'game_download', 'game_details']:
            return True
        else:
            return False

    @staticmethod
    def need_pgc_uid(attached_game_type, content_type):
        if (not attached_game_type) and content_type in ['video', 'show', 'playlist']:
            return True
        else:
            return False

    @staticmethod
    def get_box_id_for_api(box):
        box_type = BoxType.to_s(box.box_type)
        #一些类型抽屉的box_id字段要写死 用于API判断抽屉类型
        if box_type in HomeBox.STATIC_BOX_ID.keys():
            return HomeBox.STATIC_BOX_ID[box_type]
        else:
            return box.id


@handler_define
class IphoneBoxContent(IphoneBoxContentBase):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.3'),
        }

    @api_define("iPhone box", r'/interface/ios_v3/box_contents_with_slider_playlist_and_url', [
        Param('ver', False, str, '3.3', '3.3', u'版本号'),
        Param('client_type', 'phone', str, 'phone', 'phone')
    ], description='iPhone3.3+ 首页内容')
    def get(self):
        ver = self.get_argument('ver', '3.3')
        # playlist will be treat as video if include_playlist == False
        params = {
            'ver': ver,
            'client_type': self.get_argument('client_type', 'phone'),
            'include_mon_pay_video': True if ver >= '3.4' else False,
            'include_personal_space': True if ver >= '3.8' else False,
            'include_url': True if ver >= '4.1' else False,
            'include_live_broadcast': True if ver >= '4.3' else False,
            'include_playlist': True if ver >= '3.3' else False,
        }
        result = self.api_box_with_slider(params)
        self.write({'results': result})


@handler_define
class IphoneBoxContentsWithSlider(IphoneBoxContentBase):
    def get_cache_key(self):
        return {
            'client_type': self.get_argument('client_type', 'phone'),
            'ver': self.get_argument('ver', '3.3')
        }

    @api_define("iPhone BoxContentsWithSlider", '/interface/ios_v3/box_contents_with_slider', [
        Param('client_type', True, str, 'phone', 'phone', description=u'客户端类型'),
        Param('ver', True, str, '3.2', '3.2', description=u'版本号'),
    ], description='iPhone3.2 首页内容')
    def get(self):
        client_type = self.get_argument('client_type', 'phone')
        ver = self.get_argument('ver', '3.2')
        default_video_count = 5 if client_type == 'phone' else 9
        params = {'default_contents_limit_in_box': default_video_count, 'ver': ver,
                  'client_type': client_type, 'include_url': False}
        result = self.api_box_with_slider(params)
        self.write({'results': result})


@handler_define
class IphoneBoxContentsWithSliderAndUrl(IphoneBoxContentBase):
    def get_cache_key(self):
        return {
            'client_type': self.get_argument('client_type', 'phone'),
            'ver': self.get_argument('ver', '3.2.2')
        }

    @api_define("iPhone BoxContentsWithSlider", '/interface/ios_v3/box_contents_with_slider_and_url', [
        Param('client_type', True, str, 'phone', 'phone', description=u'客户端类型'),
        Param('ver', True, str, '3.2.2', '3.2.2', description=u'版本号'),
    ], description='iPhone3.2.2 首页内容')
    def get(self):
        client_type = self.get_argument('client_type', 'phone')
        ver = self.get_argument('ver', '3.2.2')
        default_video_count = 5 if client_type == 'phone' else 9
        params = {'default_contents_limit_in_box': default_video_count, 'ver': ver,
                  'client_type': client_type, 'include_url': True}
        result = self.api_box_with_slider(params)
        self.write({'results': result})


@handler_define
class IPhoneChannels_3_2(BaseHandler):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.3'),
        }

    @api_define("iPhone channels 3.2", r'/interface/ios_v3/channels_with_choiceness_state_and_icons', [
        Param('ver', False, str, '3.2', '3.2', u'版本号'),
        Param('updated_at', True, int, description=u'最近更新时间'),
    ], description='iPhone3.2 频道')
    def get(self):
        ver = self.get_argument('ver', '3.2')
        time_flag = self.get_argument('updated_at', '')
        last_updated_time = IphoneChannel.objects.filter(is_delete=0, state=1, state_iphone_3_2=1) \
                                .aggregate(Max('updated_at'))['updated_at__max'] or datetime.now()
        latest = int(time.mktime(last_updated_time.timetuple()))
        if not time_flag:
            self.write({'results': []})
        elif time_flag == latest:
            self.write({'results': []})
        else:
            channels = IphoneChannel.objects.filter(is_delete=False, state=1).order_by('-position')
            result_list = []
            for channel in channels:
                choiceness_type_sub_channel = channel.choiceness_type_sub_channel
                all_type_sub_channel = channel.all_type_sub_channel
                channel_info = {
                    'title': channel.title,
                    'cid': channel.cid if ver >= '3.2' else channel.channel_id,
                    'image_state': choiceness_type_sub_channel.image_type - 1 if choiceness_type_sub_channel else 0,
                    'title_color': channel.color,
                    'icon': channel.icon or '',
                    'icon_fifty_two': channel.icon_52 or '',
                }
                if ver >= '3.2':
                    channel_info['choiceness_state'] = choiceness_type_sub_channel.state if choiceness_type_sub_channel else 0
                    channel_info['icon_for_normal_state'] = channel.icon_3_2
                    channel_info['icon_for_selected_state'] = channel.icon_3_2_selected
                    channel_info['image_state_of_all_videos'] = all_type_sub_channel.image_type -1 if all_type_sub_channel else 0
                    channel_info['all_videos_state'] = channel.switch_all
                result_list.append(channel_info)

            results = {
                'updated_at': latest,
                'results': result_list
            }
            self.write(results)


@handler_define
class IPhoneChannels_3(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'cid': self.get_argument('cid', ''),
            'version': self.get_argument('version', '3.0'),
        }

    @api_define("iPhone channels 3.0,3.1", r'/interface/ios_v3/channels', [
        Param('ver', False, str, '3.2', '3.2', u'版本号'),
    ], description='iPhone频道3.0, 3.1')
    @api_define("iPhone channels 3.0,3.1", r'/interface/ios_v3/channels.json', [
        Param('ver', False, str, '3.2', '3.2', u'版本号'),
    ], description='iPhone频道3.0, 3.1')
    def get(self):
        version = self.get_argument('version', '')
        params = {'version': version}
        channels = IphoneChannel.objects.filter(is_delete=0, state=1, show_type=1).order_by('-position')
        res_dic = {}
        res_dic['results'] = [self.channel_hash(channel, params) for channel in channels]
        return self.write(res_dic)

    @staticmethod
    def channel_hash(channel, params):
        all_type_sub_channel = channel.all_type_sub_channel
        choiceness_type_sub_channel = channel.choiceness_type_sub_channel
        hash = {'title': channel.title, 'cid': channel.cid if params['version'] >= 3.2 else channel.id,
                'image_state': channel.image_type or '', 'title_color': channel.color, 'icon': channel.icon or '',
                'icon_fifty_two': channel.icon_52 or ''}
        if params['version'] >= '3.2':
            hash['choiceness_state'] = choiceness_type_sub_channel.state if choiceness_type_sub_channel else 0,
            hash['icon_for_normal_state'] = channel.icon_3_2
            hash['icon_for_selected_state'] = channel.icon_3_2_selected
            hash['image_state_of_all_videos'] = all_type_sub_channel.image_type -1 if all_type_sub_channel else 0
            hash['all_videos_state'] = all_type_sub_channel.state if all_type_sub_channel else 0
        return hash


@handler_define
class IphoneSubChannelList(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'cid': self.get_argument('cid', ''),
            'ver': self.get_argument('ver', '3.0'),
        }

    @api_define("iPhone box", r'/interface/ios_v3/sub_channels', [
        Param('ver', False, str, '3.0', '3.0', description=u'版本号'),
        Param('cid', True, str, description=u'频道的ID')
    ],
                description='iPhone3.2.2+ 子频道列表')
    def get(self):
        cid = self.get_argument('cid')
        ver = self.get_argument('ver', '3.0')
        if not cid:
            return self.write({})

        #TODO check performance
        channel = IphoneChannel.objects. \
            filter(content_type=IphoneChannel.CONTENT_TYPE_OF_ORIGIN, cid=cid, is_delete=0). \
            filter(Q(state=1) | Q(state_iphone_3_2=1)).order_by('-position').first()
        if not channel:
            return self.write({})
        sub_channels = channel.subchannel.filter(state=1, is_delete=0).order_by('-position')
        #TODO check performance
        if ver < '3.4' and cid == '96':
            sub_channels = sub_channels.exclude(title__contains=u'会员')

        result_list = []
        for subchannel in sub_channels:
            result_list.append(self.collect_subchannel_info(subchannel, ver))
        self.write({'results': result_list})

    @staticmethod
    def collect_subchannel_info(sub_channel, ver):
        result = dict(title=sub_channel.title,
                      sub_channel_type=sub_channel.get_type,
                      sub_channel_id=sub_channel.id,
                      image_state=sub_channel.get_image_state)
        if sub_channel.get_type == 'filter':
            result['filter'] = sub_channel.filter_collection
        if ver >= '4.0':
            result['module_with_units'] = 1 if sub_channel.is_choiceness == 1 and sub_channel.module_with_units == 1 \
                else 0

        return result


class SubChannelDetails(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def details_for_interface(self, subchannel, ver):
        params = dict(include_playlist=True if ver >= '3.3' else False,
                      include_mon_pay_video=True if ver >= '3.4' else False,
                      ver=ver)
        result = {}
        if subchannel.type == 1:  # editable_box
            result = self.details_of_editable_box_sub_channel(subchannel, params)
        elif subchannel.type == 2:  #editable_video_list
            result = self.details_of_editable_video_list_sub_channel(subchannel, params)

        return result

    def details_of_editable_box_sub_channel(self, subchannel, params):
        #TODO: replace magic-number
        slider_module_collection = subchannel.module.filter(module_type=1, state=1)[:1]
        slider_module = slider_module_collection.get() if slider_module_collection else None
        slider_details = self.details_of_module(slider_module, params)
        #TODO check performance
        normal_modules = subchannel.module.filter(state=1).exclude(module_type=1).order_by('-position')
        modules_details = [self.details_of_module(mod, params) for mod in normal_modules]
        result = {
            'image_state': subchannel.get_image_state,
            'sub_channel_type': subchannel.get_type,
            'slider_module': slider_details,
            'modules': modules_details,
        }

        if params['ver'] >= '3.7':
            #TODO: complete this
            has_brands_headline = BrandModule.sub_channel_has_brands_headline('iphone', subchannel)
            result['has_brands_headline'] = 1 if has_brands_headline else 0
        if params['ver'] >= '4.0':
            result['module_with_units'] = 0
        return result

    def details_of_module(self, mod, params):
        if not mod:
            return {}

        params['video_limit'] = mod.iphone_video_count or 6
        videos = self.get_videos_form_box(box=mod, params=params)
        details_of_videos = [self.details_of_video(mod, video, params) for video in videos]

        return {'title': mod.title, 'module_id': mod.id, 'results': details_of_videos}

    def details_of_editable_video_list_sub_channel(self, subchannel, params):
        params['video_limit'] = subchannel.video_count or 20
        videos = self.get_videos_form_box(box=subchannel, params=params)
        mod = None
        details_of_videos = [self.details_of_video(mod, video, params) for video in videos]
        return {
            'image_state': subchannel.get_image_state,
            'sub_channel_type': subchannel.get_type,
            'results': details_of_videos
        }

    @staticmethod
    def get_videos_form_box(box, params):
        video_limit = params['video_limit']
        if 'module' in box.__class__.__name__.lower():
            videos = IphoneSubChannelModuleVideo.objects.filter(module_id=box.id, state=1)
            params['subchannel_type'] = SubChannelType.to_i('editable_box')
            params['module_id'] = box.id
        else:
            videos = IphoneSubChannelVideo.objects.filter(subchannel_id=box.id, state=1)
            params['subchannel_type'] = SubChannelType.to_i('editable_video_list')
            params['subchannel_id'] = box.id
        if params.get('include_mon_pay_video', ''):
            videos = videos.filter(Q(paid=0) | Q(paid=1, pay_type=BaseVideo.pay_type.mon))
        else:
            videos = videos.filter(paid=0)
        videos = videos.order_by('-position')[:video_limit]
        videos = IphoneFixedPositionVideo.replace_position_fixed_videos(videos, params)
        return videos

    @staticmethod
    def details_of_video(mod, video, params):
        result = {
            'video_id': video.video_id,
            'title': video.title,
            'intro': video.intro,
            'video_type': VideoType.to_s(video.video_type),
            'url': video.url
        }
        if video.video_type == VideoType.to_i('playlist'):
            result['video_id'] = video.first_episode_video_id
            if params.get('include_playlist', ''):
                result['playlist_id'] = video.video_id
            else:
                result['playlist_type'] = 'video'

        if video.is_mon_pay_video():
            result['is_mon_pay_video'] = 1

        if (not mod) or mod.module_type == 0:  # for list-type-sub_channel OR normal module
            result['width_img'] = video.h_image
            result['height_img'] = video.v_image
            result['paid'] = video.paid
        elif mod.module_type == 1:  # for slider module
            result['image_2'] = video.s_image
        return result


@handler_define
class IphoneSubChannelDetails_3_2_2(SubChannelDetails):
    def get_cache_key(self):
        return {
            'sub_channel_id': self.get_argument('sub_channel_id', '1'),
        }

    @api_define("iPhone box", r'/interface/ios_v3/sub_channel_details', [
        Param('sub_channel_id', True, str, description=u'子频道id')
    ],
                description='iPhone3.3+ 子频道内容详情')
    def get(self):
        ver = '3.2.2'
        sub_channel_id = self.get_argument('sub_channel_id')
        subchannel = IphoneSubChannel.objects.filter(id=sub_channel_id, is_delete=0, state=1).order_by('-position') \
            .first()
        if not subchannel:
            return self.write({})
        self.write(self.details_for_interface(subchannel, ver))


@handler_define
class IphoneSubChannelDetails_3_3(SubChannelDetails):
    def get_cache_key(self):
        return {
            'sub_channel_id': self.get_argument('sub_channel_id', '1'),
            'ver': self.get_argument('ver', '3.3'),
        }

    @api_define("iPhone box", r'/interface/ios_v3/sub_channel_details_with_playlist', [
        Param('sub_channel_id', True, str, description=u'子频道id'),
        Param('ver', False, str, '3.3', description=u'版本号'),
    ],
                description='iPhone3.3+ 子频道内容详情')
    def get(self):
        ver = self.get_argument('ver', '3.3')
        sub_channel_id = self.get_argument('sub_channel_id')
        subchannel = IphoneSubChannel.objects.filter(id=sub_channel_id, is_delete=0, state=1).order_by('-position') \
            .first()
        if not subchannel:
            return self.write({})
        self.write(self.details_for_interface(subchannel, ver))


@handler_define
class IphoneChannelVideos(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'channel_id': self.get_argument('channel_id', '1'),
            'ver': self.get_argument('ver', '3.3')
        }

    @api_define("iPhone ChannelVideos", r'/interface/ios_v3/channel_videos', [
        Param('channel_id', True, int, '1', '1', description=u'cid'),
        Param('ver', False, str, '3.0', '3.0', description=u'版本号')
    ], description='iPhone频道视频')
    @api_define("iPhone ChannelVideos", r'/interface/ios_v3/channel_videos.json', [
        Param('channel_id', True, int, '1', '1', description=u'cid'),
        Param('ver', False, str, '3.0', '3.0', description=u'版本号')
    ], description='iPhone频道视频')
    def get(self):
        cid = self.get_argument('channel_id', '1')
        channel = get_object_or_none(IphoneChannel, cid=cid, state=1, is_delete=False)
        if not channel:
            return self.write({})
        sub_channel = get_object_or_none(IphoneSubChannel, channel=channel, is_choiceness=1, state=1, is_delete=False)
        if not sub_channel:
            return self.write({})
        modules = IphoneSubChannelModule.objects.filter(subchannel=sub_channel, state=1, is_delete=False). \
            exclude(title__contains='会员')
        modules_info = [self.details_of_module(module) for module in modules]
        self.write({'modules': modules_info})

    def details_of_module(self, module):
        result = {'title': module.title, 'module_id': module.id}
        video_limit = module.iphone_video_count or 20
        videos = IphoneSubChannelModuleVideo.objects.filter(module=module, state=1, is_delete=False,
                                                            attached_game_type=''). \
                     filter(Q(paid=0) | ~Q(pay_type=BaseVideo.pay_type.mon)). \
                     exclude(video_type__in=(
            VideoType.to_i('url'),
            VideoType.to_i('game_list'),
            VideoType.to_i('game_download'),
            VideoType.to_i('game_details'))
        ).order_by('-position')[:video_limit]  # 游戏相关
        videos = IphoneFixedPositionVideo.replace_position_fixed_videos(videos,
                    {'subchannel_type': SubChannelType.to_i('editable_box'),
                     'module_id': module.id,
                     'include_mon_pay_video': False,
                     })
        result['results'] = [self.convert_video(video) for video in videos]
        return result

    def convert_video(self, video):
        tmp = {}
        video_type = VideoType.to_s(video.video_type)
        tmp['video_id'] = video.id
        tmp['title'] = video.title
        tmp['intro'] = video.intro
        tmp['video_type'] = VideoType.to_s(video.video_type)
        tmp['width_img'] = video.h_image
        tmp['height_img'] = video.v_image
        tmp['url'] = video.url
        if video_type == 'playlist':
            tmp['video_id'] = video.first_episode_video_id
            tmp['video_type'] = 'video'
        if video.is_mon_pay_video():
            tmp['is_mon_pay_video'] = 1
        if 'game' in VideoType.to_s(video.video_type):
            tmp['game_image'] = video.h_image
            tmp['game_information'] = self.get_game_info(video.game_id)
        return tmp

    def get_game_info(self, game_id):
        game_info = {}
        game = IosGame.objects.get(pk=game_id)
        if game:
            game_info['game_type'] = game.categories
            game_info['game_id'] = game_id
            game_info['game_appname'] = game.appname
            game_info['game_version'] = game.version
            game_info['game_itunesid'] = game.itunesid
            game_info['game_logo'] = game.logo
            game_info['game_scroller'] = game.scroller
            game_info['game_score'] = game.score
            game_info['game_url'] = game.url
            game_info['game_desc'] = game.desc
            game_info['game_upload_time'] = game.upload_time
            game_info['game_size'] = game.size
            if self.get_argument('ver', '3.3') >= '4.3.1':
                game_info['game_charge'] = game.charge
                game_info['game_redirect_type'] = game.redirect_type
                game_info['game_recommend_type'] = game.recommend_type
                game_info['game_redirect_url'] = game.redirect_url
        return game_info



@handler_define
class IphoneVipGoodsPageBack(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    # def get_cache_key(self):
    #     return {
    #     }

    @api_define("ios vip goods page back img", r'/interface/ios_v3/vip_center_regulator', [
    ], description='ios(iphone3.4+)会员商品页背景图')
    @api_define("ios vip goods page back img", r'/interface/ios_v3/vip_center_regulator.json', [
    ], description='ios(iphone3.4+)会员商品页背景图')
    def get(self):
        regulators = IosVipGoodsPageBack.objects.filter(is_delete=0, state=1, device_type='iphone')
        if regulators:
            regulator = regulators[0]
            result = {
                        'vip_img': regulator.vip_img,
                        'vip_img_hd': regulator.vip_img_hd,
                      }
        else:
            result = {
                'vip_img': '',
                'vip_img_hd': '',
                }
        return self.write(result)


