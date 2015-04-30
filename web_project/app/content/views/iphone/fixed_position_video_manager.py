# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import IphoneSubChannelModuleVideo, IphoneSubChannelVideo, IphoneChannel, IphoneSubChannel, \
    IphoneSubChannelModule, VideoType, IphoneFixedPositionVideo, Status, SubChannelType, VideoType, Platform, \
    BaseVideo, IosGame
from content.views.common import redefine_item_pos, set_position


def fixed_position_videos(request):
    channel_id = request.GET.get('channel_id', '')
    subchannel_id = request.GET.get('subchannel_id', '')
    module_id = request.GET.get('module_id', '')
    channel = subchannel = module = None
    videos = []
    try:
        if subchannel_id and channel_id:
            channel = IphoneChannel.objects.get(pk=int(channel_id), is_delete=0)
            subchannel = IphoneSubChannel.objects.get(pk=int(subchannel_id), is_delete=0)
            if module_id:
                module = IphoneSubChannelModule.objects.get(pk=int(module_id), is_delete=0)
                videos = IphoneFixedPositionVideo.objects.filter(is_delete=0, module_id=module_id)\
                    .order_by('fixed_position')
            else:
                videos = IphoneFixedPositionVideo.objects.filter(is_delete=0, subchannel_id=subchannel_id)\
                    .order_by('fixed_position')

    except (IphoneChannel.DoesNotExist, IphoneSubChannel.DoesNotExist, IphoneSubChannelModuleVideo.DoesNotExist,
            IphoneSubChannelVideo.DoesNotExist):
        pass
    for index, video in enumerate(videos):
        videos[index].copyright_for_view = video.copyright_for_view()
        videos[index].pay_type_for_view = video.pay_type_for_view()
        videos[index].video_type_for_view = video.video_type_for_view()
    commit_dict = {'channel': channel,
                   'subchannel': subchannel, 'module': module,
                   'video_state_hash': Status.STATUS_HASH,
                   'videos': videos}
    return render(request, 'iphone/channel/fixed_pos_videos/videos.html', commit_dict)


def add_fixed_position_video(request, platform='iphone'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        video = IphoneFixedPositionVideo()
        if module_id:
            video.module_id = module_id
            video.subchannel_type = SubChannelType.to_i('editable_box')
        else:
            video.subchannel_type = SubChannelType.to_i('editable_video_list')
        video.subchannel_id = subchannel_id
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video.fixed_position = request.POST.get('fixed_position', 0)

        video_type_name = str(request.POST.get('video_type', ''))
        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video':
            video.add_video_type_fields(request.POST)
        elif video_type_name == "game_list":
            video.add_game_list_type_fields(request.POST)
        elif video_type_name == "game_details":
            video.add_game_download_type_fields(request.POST)
        video.save()
        return HttpResponseRedirect(reverse('iphone_query_fixed_position_video') + "?module_id=" + module_id +
                                    "&channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&video_id=" +
                                    str(video.id))
    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        channel = subchannel = module = fixed_position_list = video_type_list = None
        if current_module_id:
            module = IphoneSubChannelModule.objects.filter(id=current_module_id).first()
        module_type = module.module_type if module else 0
        try:
            channel = IphoneChannel.objects.get(pk=current_channel_id, is_delete=0)
            subchannel = IphoneSubChannel.objects.get(pk=current_subchannel_id, is_delete=0)
            video_type_list = list(IphoneSubChannelModuleVideo.video_type_supports()) if subchannel else []
            if video_type_list and subchannel.is_choiceness == 0:
                video_type_list = video_type_list[0:4]
            video_type_list = VideoType.platformization(Platform.to_i('iphone'), video_type_list)
            video_type_list = BaseVideo.get_page_show_v_types(video_type_list)
            if current_module_id:
                videos = IphoneFixedPositionVideo.objects.filter(is_delete=0, module_id=current_module_id)
            else:
                videos = IphoneFixedPositionVideo.objects.filter(is_delete=0, subchannel_id=current_subchannel_id)
            fixed_positions = [video.fixed_position for video in videos]
            fixed_position_list = list(set(range(1, 17)) - set(fixed_positions))
        except:
            pass

        return render(request, 'iphone/channel/fixed_pos_videos/add_video.html', {
            'platform': platform, 'video_type_list': video_type_list, 'current_channel_id': current_channel_id,
            'current_subchannel_id': current_subchannel_id, 'current_module_id': current_module_id, 'module': module,
            'channel': channel, 'subchannel': subchannel, 'fixed_position_list': fixed_position_list,
            'module_type': module_type
        })


@login_required
def query_fixed_position_video(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    video_id = request.GET.get('video_id', '')
    video = get_object_or_404(IphoneFixedPositionVideo, pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    channel = IphoneChannel.objects.get(pk=channel_id, is_delete=0)

    module = IphoneSubChannelModule.objects.filter(id=module_id).first() if module_id else None
    module_type = module.module_type if module else 0
    query_d = {'is_delete': 0}

    if module_id:
        query_d.update({'module_id': module_id})
    else:
        query_d.update({'subchannel_id': subchannel_id})
    fixed_position_videos = IphoneFixedPositionVideo.objects.filter(**query_d).exclude(id=video.id)
    fixed_positions = [fixed_position_video.fixed_position for fixed_position_video in fixed_position_videos]
    fixed_position_list = list(set(range(1, 17)) - set(fixed_positions))
    args = {
        'h_image_desc': '448x252',
        'v_image_desc': '200x300',
        's_image_desc': '448x252',
        'channel_id': channel_id,
        'subchannel_id': subchannel_id,
        'module_id': module_id,
        'module_type': module_type,
        'video': video,
        'fixed_position_list': fixed_position_list
    }
    if video_type_name == "url":
        return render(request, 'iphone/channel/fixed_pos_videos/update_url_form_fields.html', args)
    elif video_type_name in ['video', 'show', 'playlist']:
        return render(request, 'iphone/channel/fixed_pos_videos/update_video.html', args)
    elif video_type_name == "game_list":
        return render(request, 'iphone/channel/sub_channel_and_box_videos/update_game_list.html',args)
    elif video_type_name == 'game_details':
        game = get_object_or_404(IosGame, pk=video.game_id)
        args['game'] = game
        return render(request, 'iphone/channel/sub_channel_and_box_videos/update_item_game_details.html',args)


@login_required
def update_fixed_position_video(request):
    if request.method == 'POST':
        channel_id = subchannel_id = module_id = ''
        try:
            post_dict = request.POST.dict()
            channel_id = post_dict.pop('channel_id')
            subchannel_id = post_dict.pop('subchannel_id')
            module_id = post_dict.get('module_id')
            video_id = post_dict.pop('id')
            if video_id:
                video = IphoneFixedPositionVideo.objects.get(pk=video_id)
                if not module_id:
                    del post_dict['module_id']  # 如果传过来module_id为''数据保存报错
                for k, v in post_dict.iteritems():
                    if hasattr(video, k):
                        setattr(video, k, v)
                        # if VideoType.to_s(int(video.video_type)) in ("game_details", 'game_download'):
                        # video.game_id = IphoneGame.create_or_update(request.POST)
                if video.attached_game_type:
                    video.update_game_details_type_fields(request.POST)
                video.save()
        except Exception, e:
            print e
        return HttpResponseRedirect(reverse('iphone_fixed_position_videos') + "?channel_id=" + channel_id +
                                    "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)


@login_required
def update_fixed_position_video_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        subchannel_id = request.GET.get('subchannel_id')
        module_id = request.GET.get('module_id')
        item = None
        if pk:
            if module_id:
                item = IphoneSubChannelModuleVideo.objects.get(id=int(pk))
            elif subchannel_id:
                item = IphoneSubChannelVideo.objects.get(id=int(pk))
            name = request.POST.get('name')
            value = request.POST.get('value')
            if hasattr(item, name):
                setattr(item, name, value)
            item.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


def update_fixed_position_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        # module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                video = IphoneFixedPositionVideo.objects.get(id=int(video_id))
                setattr(video, attribute, value)
                video.save()
                response = {'status': 'success', 'value': getattr(video, attribute)}
            except Exception, e:
                response = {'status': 'error', 'msg': u"修改视频失败!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def check_fixed_position(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    value = request.GET.get("value", '')
    method = request.GET.get("method", "")
    video_id = request.GET.get("video_id", '')
    if module_id:
        fixed_position_video = IphoneFixedPositionVideo.objects.filter(module_id=int(module_id), is_delete=0, state=1,
                                                                       fixed_position=int(value))
    else:
        fixed_position_video = IphoneFixedPositionVideo.objects.filter(subchannel_id=int(subchannel_id), is_delete=0,
                                                                       state=1, fixed_position=int(value))
    if method == 'update':
        fixed_position_video = fixed_position_video.exclude(id=video_id)
    if fixed_position_video:
        return HttpResponse('false')
    else:
        return HttpResponse('true')


@login_required
def delete_fixed_position_video(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    video_id = request.GET.get('video_id', '')
    try:
        IphoneFixedPositionVideo.objects.filter(pk=video_id).update(is_delete=1)
    except (IphoneSubChannelModuleVideo.DoesNotExist, IphoneSubChannelVideo.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('iphone_fixed_position_videos') + "?channel_id=" + channel_id +
                                "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)

