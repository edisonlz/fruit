# coding=utf-8
from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler, CachedPlusHandler

from app.content.models import *
from django.db.models import Q


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


class IPadHome(CachedPlusHandler):
    box_type = None

    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def api_context(self, ver):
        ret = []
        # 轮播图盒子
        slider_box = self.get_slider_box()
        if slider_box:
            IPadHome.box_type = 'slider'
            ret.append(self.pack_box(slider_box, ver))

        IPadHome.box_type = None
        # 精选盒子
        selection_box = self.get_selection_box()
        if selection_box:
            ret.append(self.pack_box(selection_box, ver))
        # 其他盒子
        other_boxes = self.get_normal_boxes()
        for box in other_boxes:
            ret.append(self.pack_box(box, ver))
        return ret

    def pack_box(self, box, ver):
        contents = {}
        videos = IpadHomePublishedVideo.objects.filter(box_id=box.id, is_delete=False, state=1)
        #TODO: filter video_types
        # 3.2+, has mon_pay_video
        if ver < '3.2':
            videos = videos.filter(Q(paid=0) | ~Q(pay_type=BaseVideo.pay_type.mon))

        videos = videos.order_by('-position')[:box.video_count_for_pad]
        contents['results'] = self.convert_index_videos(videos, ver)
        packed_box = {'title': box.title,
                      'box_id': self.get_box_id_for_api(box),
                      'is_youku_channel': box.is_youku_channel,
                      'max_count': box.video_count_for_pad,
                      'cid': '',
                      'contents': contents}
        packed_box = self.tag_process(packed_box, box, ver)
        return packed_box

    def tag_process(self, packed_box, box, ver):
        return packed_box

    @staticmethod
    def convert_index_videos(videos, ver):
        return [IPadHome.convert_index_video(video, ver) for video in videos]

    @classmethod
    def convert_index_video(cls, video, ver):
        result = {
            'content_id': video.video_id,
            'content_type': VideoType.to_s(video.video_type),
            'title': video.title,
            'img': video.s_image if cls.box_type == 'slider' else video.h_image,
            'intro': video.intro,
            'second_title': video.subtitle,
            'url': video.url
        }
        # 3.2+, has mon_pay_video
        # 3.0.2+, has playlist
        if result['content_type'] == 'playlist':
            if ver >= '3.0.2':
                result['first_episode_video_id'] = video.first_episode_video_id
            else:
                result['content_id'] = video.first_episode_video_id
                result['content_type'] = 'video'
        elif result['content_type'] == 'live_broadcast':
            if ver < '3.9.2':
                result['content_id'] = ''
                result['content_type'] = 'url'
        elif result['content_type'] == 'url':
            pass
        if video.is_mon_pay_video():
            result['is_mon_pay_video'] = 1
        return result

    @staticmethod
    def get_box_id_for_api(box):
        box_type = BoxType.to_s(box.box_type)
        #一些类型抽屉的box_id字段要写死 用于API判断抽屉类型
        if box_type in HomeBox.STATIC_BOX_ID.keys():
            return HomeBox.STATIC_BOX_ID[box_type]
        else:
            return box.id
    @staticmethod
    def get_slider_box():
        # 轮播图盒子
        slider_box_set = HomeBox.objects.filter(platform=2, box_type=2, state=1, is_delete=False)[:1]
        if slider_box_set:
            return slider_box_set[0]
        return None

    @staticmethod
    def get_selection_box():
        # 精选盒子
        selection_box_set = HomeBox.objects.filter(platform=2, box_type=3, state=1, is_delete=False)[:1]
        if selection_box_set:
            return selection_box_set[0]
        return None

    @staticmethod
    def get_normal_boxes():
        # 其他盒子
        return HomeBox.objects.filter(platform=2, state=1, is_delete=False).exclude(box_type=2). \
            exclude(box_type=3).order_by('-position')

    @staticmethod
    def get_tag_details(box_id, jump_info=False, tag_info=False):
        box_tags = IpadHomeBoxTag.objects.filter(is_delete=0, box_id=box_id)
        if jump_info:
            box_tag = box_tags.filter(tag_type='title').first()
            return IPadHome.get_tag_info(box_tag)
        elif tag_info:
            filter_tags = box_tags.filter(tag_type='normal')[:4]
            tag_info_list = [IPadHome.get_tag_info(tag) for tag in filter_tags]
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
            sub_channel = IpadSubChannel.objects.filter(id=box_tag.sub_channel_id).first()
            channel = IpadChannel.objects.filter(id=sub_channel.channel_id).first()
            tag_info['cid'] = str(channel.cid) if (channel.cid and channel.cid > 0) else ''
            tag_info['sub_channel_id'] = sub_channel.id or 0
        if tag_info == 'jump_to_game':
            game_app = IosGame.objects.get(id=box_tag.game_id)
            tag_info['game_id'] = game_app.original_game_id
            tag_info['game_itunesid'] = game_app['itunesid']
            tag_info['game_url'] = game_app['url']

        return tag_info



@handler_define
class IPadHome_3_0(IPadHome):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.0'),
        }

    @api_define("iPad Home", r'/interface/ipad_v3/index_videos', [
        Param('ver', True, str, '3.0', '3.0', u'版本号'),
    ], description="IPAD3.0+ 首页")
    def get(self):
        ver = self.get_argument('ver', '3.0')
        self.write({'results': self.api_context(ver)})

    def tag_process(self, packed_box, box, ver):
        title_tag_info = self.get_tag_details(box.id, jump_info=True)
        #老版本接口
        # 为我推荐（cid:2000），订阅更新(cid:2004) 类型 抽屉 需要cid字段 直接取抽屉的title_tag的cid字段
        # 用于 API项目 判断抽屉的类型
        # 其余类型抽屉 如果 title_tag 类型为跳转到频道 则取 cid字段作为 跳转标识使用
        if BoxType.to_s(box.box_type) in HomeBox.IPAD_SPECIAL_BOXES.keys():
            cid = title_tag_info['cid']
            packed_box.update({'cid':cid})
        elif title_tag_info['type'] == 'jump_to_channel' and title_tag_info['cid'] != '':
            cid = title_tag_info['cid']
            packed_box.update({'cid':cid})
        return packed_box


@handler_define
class IPadHome_3_0_2(IPadHome):
    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.0.2'),
        }

    @api_define("iPad Home", r'/interface/ipad_v3/index_videos_with_playlist', [
        Param('ver', True, str, '3.0.2', '3.0.2', u'版本号'),
    ], description="IPAD3.0.2+ 首页")
    def get(self):
        ver = self.get_argument('ver', '3.0.2')
        self.write({'results': self.api_context(ver)})

    def tag_process(self, packed_box, box, ver):
        title_tag_info = self.get_tag_details(box.id, jump_info=True)
        #新版本ipad接口 为我推荐（cid:2000），订阅更新(cid:2004) 类型 抽屉 需要cid字段 直接取抽屉的title_tag的cid字段
        #用于 API项目 判断抽屉的类型
        if BoxType.to_s(box.box_type) in HomeBox.IPAD_SPECIAL_BOXES.keys():
            cid = title_tag_info['cid']
            packed_box.update({'cid':cid})
        if ver >= '3.9.5':
            packed_box.update(
                {'jump_info': title_tag_info,
                 'tags': self.get_tag_details(box.id, tag_info=True)})
        return packed_box


@handler_define
class IpadChannels(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'ver': self.get_argument('ver', '3.0'),
        }

    @api_define("iPad Channels", r'/interface/ipad_v3/channels', [
        Param('ver', True, str, '3.0', '3.0', u'版本号'),
    ], description="PAD3.X 频道列表")
    def get(self):
        ver = self.get_argument('ver', '3.0')
        channels = IpadChannel.objects.filter(state=1, is_delete=False).order_by('-position')
        results = [self.channel_info(channel, ver) for channel in channels]

        self.write({'channels_count': channels.count(), 'results': results})

    @staticmethod
    def channel_info(channel, ver):
        choiceness_type_sub_channel = channel.choiceness_type_sub_channel
        all_type_sub_channel = channel.all_type_sub_channel
        info = {
            'title': channel.title, 'channel_id': channel.cid,
            # 'choiceness_state': choiceness_type_sub_channel.state if choiceness_type_sub_channel else 0,
            'choiceness_state': 1,
            'image_state_for_choiceness': choiceness_type_sub_channel.image_type - 1 if choiceness_type_sub_channel
            else 0,  # 旧系统是[0,, 1] 新系统是[1, 2]
            'image_state_for_all': all_type_sub_channel.image_type - 1 if all_type_sub_channel else 0,
        }
        if ver >= '3.1':
            if channel.for_sale:
                info['choiceness_state'], info['all_videos_state'] = 0, 0
            else:
                info['all_videos_state'] = all_type_sub_channel.state if all_type_sub_channel else 0
            info['normal_icon'] = channel.icon_big
            info['selected_icon'] = channel.icon_big_selected
            info['marking_state'] = channel.for_sale
            info['image_state_for_marking'] = channel.image_type_sale
        else:
            info['big_normal_icon'] = channel.icon_big
            info['big_selected_icon'] = channel.icon_big_selected
            info['small_normal_icon'] = channel.icon_small
            info['small_selected_icon'] = channel.icon_small_selected
        return info


@handler_define
class IPadSubChannels(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60


    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'cid': self.get_argument('cid', '1'),
            'ver': self.get_argument('ver', '3.2'),
        }

    @api_define("iPad SubChannels", r'/interface/ipad_v3/sub_channels', [
        Param('cid', True, int, '1', '1', u'cid'),
        Param('ver', True, str, '3.2', '3.2', u'版本号'),
    ], description="PAD3.X 子频道列表")
    def get(self):
        cid = int(self.get_argument('cid', '1'))
        ver = self.get_argument('ver', '3.2')
        channel_set = IpadChannel.objects.filter(content_type=IpadChannel.CONTENT_TYPE_OF_ORIGIN,
                                                 cid=cid, state=1, is_delete=False).exclude(cid=1001)[:1]
        if channel_set:
            channel = channel_set.get()
        else:
            self.write({})
            return
        filter_params = {
            'channel_id': channel.id,
            'state': 1,
            'is_delete': False
        }
        if ver < '3.2' and cid == 96:
            filter_params.update({'for_membership': 0})
        sub_channels = IpadSubChannel.objects.filter(**filter_params).order_by('-position')
        results = [self.details_of_sub_channel(sub_channel) for sub_channel in sub_channels]

        self.write({'results': results})

    @staticmethod
    def details_of_sub_channel(sub_channel):
        result = {
            'title': sub_channel.title, 'sub_channel_type': sub_channel.get_type,
            'sub_channel_id': sub_channel.id, 'image_state': sub_channel.get_image_state,
        }
        if sub_channel.get_type == 'filter':
            result['filter'] = sub_channel.filter_collection
        return result


@handler_define
class IPadSubChannelDetails(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'sub_channel_id': self.get_argument('sub_channel_id', '1'),
            'ver': self.get_argument('ver', '3.2'),
        }

    @api_define("iPad SubChannelDetails", r'/interface/ipad_v3/sub_channel_details', [
        Param('sub_channel_id', True, int, '1', '1', u'sub_channel_id'),
        Param('ver', True, str, '3.0.2', '3.0.2', u'版本号'),
    ], description="PAD3.X 子频道详情")
    def get(self):
        sub_channel_id = self.get_argument('sub_channel_id', '1')
        ver = self.get_argument('ver', '3.0.2')
        sub_channel_set = IpadSubChannel.objects.filter(pk=sub_channel_id)[:1]
        if not sub_channel_set:
            return self.write({})
        sub_channel = sub_channel_set[0]
        params = {'ver': ver, 'sub_channel_id': sub_channel_id}
        self.write(self.details_of_sub_channel(sub_channel, params))

    def details_of_sub_channel(self, sub_channel, params):
        params['include_mon_pay_video'] = True if params.get('ver', '') >= '3.2' else False
        sub_channel_type = sub_channel.get_type
        if sub_channel_type == 'editable_box':
            return self.details_of_editable_box_sub_channel(sub_channel, params)
        elif sub_channel_type == 'editable_video_list':
            return self.details_of_editable_video_list_sub_channel(sub_channel, params)
        else:
            return {}

    def details_of_editable_video_list_sub_channel(self, sub_channel, params):
        default_video_limit = 5 if sub_channel.get_image_state == 'horizontal' else 4
        video_limit = sub_channel.video_count or default_video_limit
        videos = IpadSubChannelItem.objects.filter(subchannel_id=sub_channel.id, state=1)
        if params['include_mon_pay_video']:
            videos = videos.filter(Q(paid=0) | Q(paid=1, pay_type=BaseVideo.pay_type.mon))
        else:
            videos = videos.filter(paid=0)
        videos = videos.order_by('-position')[:video_limit]
        options = params.copy()
        options['subchannel_type'] = SubChannelType.to_i('editable_video_list')
        options['subchannel_id'] = sub_channel.id
        videos = IpadFixedPositionVideo.replace_position_fixed_videos(videos, options)
        mod = None
        videos_details = [self.details_of_video(mod, video) for video in videos]
        return {
            'image_state': sub_channel.get_image_state,
            'sub_channel_type': sub_channel.get_type,
            'results': videos_details,
        }

    def details_of_editable_box_sub_channel(self, sub_channel, params):
        result = {
            'image_state': sub_channel.get_image_state,
            'sub_channel_type': sub_channel.get_type,
            'slider_module': self.details_of_slider_module(sub_channel, params),
            'modules': self.details_of_normal_modules(sub_channel, params)
        }
        if params.get('ver', '') >= '3.3':
            has_brands_headline = BrandModule.sub_channel_has_brands_headline('ipad', sub_channel)
            result['has_brands_headline'] = 1 if has_brands_headline else 0
        return result

    def details_of_slider_module(self, sub_channel, params):
        slider_box_set = sub_channel.module.filter(module_type=1, state=1, is_delete=False)[:1]
        if not slider_box_set:
            return {}
        slider_box = slider_box_set[0]
        return self.details_of_module(sub_channel, slider_box, params)

    def details_of_normal_modules(self, sub_channel, params):
        sub_channel_modules = sub_channel.module.filter(is_delete=False, state=1). \
            exclude(module_type=1).order_by('-position')
        return [self.details_of_module(sub_channel, mod, params) for mod in sub_channel_modules]

    def details_of_module(self, sub_channel, mod, params):
        result = {
            'title': mod.title,
            'module_id': mod.id,
            'results': self.details_of_videos(sub_channel, mod, params)
        }
        if mod.module_type == 1:  # slider
            result['headline_image_size'] = sub_channel.channel.image_size_of_slider_module  # TODO
        return result

    def details_of_videos(self, sub_channel, mod, params):
        default_video_limit = 5 if sub_channel.get_image_state == 'horizontal' else 4
        video_limit = mod.video_count or default_video_limit
        videos = IpadSubChannelModuleItem.objects.filter(module_id=mod.id, state=1, is_delete=False)
        if params['include_mon_pay_video']:
            videos = videos.filter(Q(paid=0) | Q(paid=1, pay_type=BaseVideo.pay_type.mon))
        else:
            videos = videos.filter(paid=0)
        videos = videos.order_by('-position')[:video_limit]
        options = params.copy()
        options['subchannel_type'] = SubChannelType.to_i('editable_box')
        options['module_id'] = mod.id
        videos = IpadFixedPositionVideo.replace_position_fixed_videos(videos, options)
        return [self.details_of_video(mod, video) for video in videos]

    @staticmethod
    def details_of_video(mod, video):
        result = {
            'video_id': video.video_id,
            'title': video.title,
            'intro': video.intro,
            'video_type': VideoType.to_s(video.video_type),
            'second_title': video.subtitle,
            'url': video.url,
        }
        if result['video_type'] == 'playlist':
            result['video_id'] = video.first_episode_video_id
            result['playlist_id'] = video.video_id

        if mod and mod.module_type == 1:  # slider module
            result['image_2'] = video.s_image
        else:  # video-list-type-sub_channel & normal module
            result['width_img'] = video.h_image
            result['height_img'] = video.v_image
            result['paid'] = video.paid

        if video.is_mon_pay_video():
            result['is_mon_pay_video'] = 1
        return result


@handler_define
class IpadChannelVideos(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    def get_cache_key(self):
        return {
            'channel_id': self.get_argument('channel_id', '1'),
        }

    @api_define("iPad ChannelVideos", r'/interface/ipad_v3/channel_videos', [
        Param('channel_id', True, int, '1', '1', u'channel_id'),
    ], description="PAD3.X 频道视频")
    def get(self):
        ret = {}
        channel_id = self.get_argument('channel_id', '1')
        channel = get_object_or_none(IpadChannel, cid=channel_id, state=1, is_delete=False)
        if not channel:
            return self.write({})
        params = {
            'include_playlist': True if channel.for_sale else False,
            'include_url': True if channel.for_sale else False,
        }
        sub_channel = get_object_or_none(IpadSubChannel, is_choiceness=1, channel=channel)
        if not sub_channel:
            return self.write({})
        slider_module = get_object_or_none(IpadSubChannelModule, subchannel=sub_channel, module_type=1, state=1,
                                           is_delete=False)
        ret['headline_and_videos'] = self.details_of_slider_module(channel, slider_module, params)
        ret['modules_and_videos'] = self.details_of_normal_modules(sub_channel, params)
        self.write(ret)

    def details_of_normal_modules(self, sub_channel, params):
        modules = IpadSubChannelModule.objects.filter(subchannel=sub_channel, module_type=0, state=1, is_delete=False)
        #TODO: test-point: not add: ver < 3.2 不支持会员精选模块
        return [self.details_of_normal_module(mod, params) for mod in modules]

    def details_of_normal_module(self, mod, params):
        result = {'title': mod.title, 'module_id': mod.id}
        videos = IpadSubChannelModuleItem.objects.filter(module=mod, state=1, is_delete=False)
        options = params.copy()
        options['subchannel_type'] = SubChannelType.to_i('editable_box')
        options['module_id'] = mod.id
        videos = IpadFixedPositionVideo.replace_position_fixed_videos(videos, options)
        result['results'] = [self.details_of_video(mod, video, params) for video in videos]
        return result

    def details_of_slider_module(self, channel, mod, params):
        if not mod:
            return {}
        result = {'title': mod.title, 'module_id': mod.id, 'headline_image_size': channel.image_size_of_slider_module}
        slider_videos = IpadSubChannelModuleItem.objects.filter(module=mod, state=1, is_delete=False)
        if not params.get('include_url', False):
            slider_videos = slider_videos.exclude(video_type=VideoType.to_i('url'))
        slider_videos = slider_videos.order_by('-position')[:mod.video_count]
        options = params.copy()
        options['subchannel_type'] = SubChannelType.to_i('editable_box')
        options['module_id'] = mod.id
        slider_videos = IpadFixedPositionVideo.replace_position_fixed_videos(slider_videos, options)

        result['results'] = [self.details_of_video(mod, video, params) for video in slider_videos]
        return result

    def details_of_video(self, mod, video, params):
        result = {'video_id': video.id, 'video_type': video.video_type,
                  'title': video.title, 'intro': video.intro, 'second_title': video.subtitle, }
        if mod.module_type == 1:  # if is_slider
            result['headline_image'] = video.s_image
        else:
            result['width_img'] = video.h_image
            result['height_img'] = video.v_image

        if result['video_type'] == VideoType.to_i('playlist'):
            result['video_id'] = video.first_episode_video_id
            if params.get('include_playlist', False):
                result['playlist_id'] = video.video_id
            else:
                result['video_type'] = 'video'
        if result['video_type'] == VideoType.to_i('playlist'):
            result['url'] = video.url
        return result



@handler_define
class IpadVipGoodsPageBack(CachedPlusHandler):
    def get_varnish_expire(self):
        return 60

    def get_cache_expire(self):
        return 60 * 2

    # def get_cache_key(self):
    #     return {
    #     }

    @api_define("ios vip goods page back img", r'/interface/ios_v3/vip_center_regulator', [
    ], description='ios(ipad3.2+)会员商品页背景图')
    @api_define("ios vip goods page back img", r'/interface/ios_v3/vip_center_regulator.json', [
    ], description='ios(ipad3.2+)会员商品页背景图')
    def get(self):
        regulators = IosVipGoodsPageBack.objects.filter(is_delete=0, state=1, device_type='ipad')
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
