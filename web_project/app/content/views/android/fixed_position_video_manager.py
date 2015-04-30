# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import AndroidSubChannelModuleVideo, AndroidSubChannelVideo, AndroidChannel, AndroidSubChannel, \
    AndroidSubChannelModule, VideoType, AndroidVideoListModule, AndroidVideoListVideo, SyncJob, Status, \
    AndroidFixedPositionVideo, SubChannelType, BaseVideo
from content.models.game import AndroidGame
from content.views.common import redefine_item_pos, set_position


@login_required
def fixed_position_videos(request):
    channel_id = request.GET.get('channel_id', '')
    subchannel_id = request.GET.get('subchannel_id', '')
    module_id = request.GET.get('module_id', '')
    channel, subchannel, module = (None,) * 3
    videos = []
    try:
        if subchannel_id and channel_id:
            channel = AndroidChannel.objects.get(pk=int(channel_id), is_delete=0)
            subchannel = AndroidSubChannel.objects.get(pk=int(subchannel_id), is_delete=0)
            if module_id:
                module = AndroidSubChannelModule.objects.get(pk=int(module_id), is_delete=0)
                videos = AndroidFixedPositionVideo.objects.filter(is_delete=0, module_id=int(module_id)).order_by(
                    '-updated_at')
            else:
                videos = AndroidFixedPositionVideo.objects.filter(is_delete=0,
                                                                  subchannel_id=int(subchannel_id)).order_by(
                    '-updated_at')

    except (AndroidChannel.DoesNotExist, AndroidSubChannel.DoesNotExist, AndroidSubChannelModuleVideo.DoesNotExist,
            AndroidSubChannelVideo.DoesNotExist):
        pass
    for index, video in enumerate(videos):
        videos[index].copyright_for_view = video.copyright_for_view()
        videos[index].pay_type_for_view = video.pay_type_for_view()
        videos[index].video_type_for_view = video.video_type_for_view()
    commit_dict = {'channel': channel,
                   'subchannel': subchannel, 'module': module,
                   'video_state_hash': Status.STATUS_HASH,
                   'videos': videos}
    return render(request, 'android/channel/fixed_position_videos/videos.html', commit_dict)


@login_required
def add_fixed_position_video(request, platform='android'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        video = AndroidFixedPositionVideo()
        if module_id:
            video.module_id = module_id
            video.subchannel_type = SubChannelType.to_i('editable_box')
            box = AndroidSubChannelModule.objects.get(id=module_id)
            box_column_name = 'module_id'
        else:
            video.subchannel_type = SubChannelType.to_i('editable_video_list')
            box = AndroidSubChannel.objects.get(id=subchannel_id)
            box_column_name = 'subchannel_id'
        video.subchannel_id = subchannel_id
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = request.POST.get('video_type', '')
        video.fixed_position = request.POST.get('fixed_position', 0)

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'game_gift':
            video.add_game_gift_type_fields(request.POST)
        elif video_type_name == "game_list":
            video.add_game_list_type_fields(request.POST)
        elif video_type_name == "game_details" or video_type_name == 'game_download':
            video.add_game_download_type_fields(request.POST)
        elif video_type_name == "video_with_game_details":
            video.add_video_with_game_details_type_fields(request.POST)
        else:
            video.add_video_type_fields(request.POST)
        video.channel_id = channel_id
        video.state = 0
        if BaseVideo.get_exist_video_in_box(video_type_name, AndroidFixedPositionVideo, box, box_column_name, video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.save()
        return HttpResponseRedirect(reverse('android_query_fixed_position_video') + "?module_id=" + module_id +
                                    "&channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&video_id=" + str(
            video.id))
    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        channel, subchannel, module = (None,) * 3
        channel = AndroidChannel.objects.get(pk=current_channel_id, is_delete=0)
        subchannel = AndroidSubChannel.objects.get(pk=current_subchannel_id, is_delete=0)
        if current_module_id:
            module = AndroidSubChannelModule.objects.get(pk=current_module_id, is_delete=0)
            s_image_tag = int(module.is_headline_module)
            game_banner_tag = int(module.is_game_banner_module)
            show_button_tag = int(channel.is_game_channel and s_image_tag)  #游戏频道下的轮播图类型抽屉 只显示一张轮播图 显示下载按钮
            videos = AndroidFixedPositionVideo.objects.filter(is_delete=0, module_id=int(current_module_id))
        else:
            videos = AndroidFixedPositionVideo.objects.filter(is_delete=0,
                                                              subchannel_id=int(current_subchannel_id)).order_by(
                '-updated_at')
            s_image_tag, game_banner_tag, show_button_tag = (0,) * 3
        video_type_list = AndroidFixedPositionVideo.video_types(mock=True)
        fixed_positions = [video.fixed_position for video in videos]
        fixed_position_list = list(set(range(1, 17)) - set(fixed_positions))
        return render(request, 'android/channel/fixed_position_videos/add_video.html', {'platform': platform,
                                                                                        'video_type_list': video_type_list,
                                                                                        'current_channel_id': current_channel_id,
                                                                                        'current_subchannel_id': current_subchannel_id,
                                                                                        'current_module_id': current_module_id,
                                                                                        'module': module,
                                                                                        'channel': channel,
                                                                                        'subchannel': subchannel,
                                                                                        'fixed_position_list': fixed_position_list,
                                                                                        's_image_tag': s_image_tag,
                                                                                        'show_button_tag': show_button_tag,
                                                                                        'game_banner_tag': game_banner_tag})


@login_required
def query_fixed_position_video(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    video_id = request.GET.get('video_id', '')
    video = get_object_or_404(AndroidFixedPositionVideo, pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    channel = AndroidChannel.objects.get(pk=channel_id, is_delete=0)
    if module_id:
        fixed_position_videos = AndroidFixedPositionVideo.objects.filter(is_delete=0, module_id=int(module_id)).exclude(
            id=video.id)
        module = AndroidSubChannelModule.objects.get(pk=module_id, is_delete=0)
        s_image_tag = int(module.is_headline_module)
        game_banner_tag = int(module.is_game_banner_module)
        show_button_tag = int(channel.is_game_channel and s_image_tag)
    else:
        s_image_tag, game_banner_tag, show_button_tag = (0,) * 3
        fixed_position_videos = AndroidFixedPositionVideo.objects.filter(is_delete=0,
                                                                         subchannel_id=int(subchannel_id)).exclude(
            id=video.id)
    if game_banner_tag:
        #这里横图 竖图 对应 老版本 横屏 竖屏 待确认
        h_image_desc = '1248x110',
        v_image_desc = '688x110'
    else:
        h_image_desc = '448x252'
        v_image_desc = '200x300'
    s_image_desc = '720x194'
    fixed_positions = [fixed_position_video.fixed_position for fixed_position_video in fixed_position_videos]
    fixed_position_list = list(set(range(1, 17)) - set(fixed_positions))
    args = {
        's_image_tag': s_image_tag,
        'game_banner_tag': game_banner_tag,
        'show_button_tag': show_button_tag,
        'h_image_desc': h_image_desc,
        'v_image_desc': v_image_desc,
        's_image_desc': s_image_desc,
        'channel_id': channel_id,
        'subchannel_id': subchannel_id,
        'module_id': module_id,
        'video': video,
        'fixed_position_list': fixed_position_list
    }
    if (video_type_name == "url"):
        return render(request, 'android/channel/fixed_position_videos/update_url_form_fields.html', args)
    elif (video_type_name == "game_gift"):
        return render(request, 'android/channel/sub_channel_and_box_videos/update_game_gift.html', args)
    elif (video_type_name == "game_list"):
        return render(request, 'android/channel/sub_channel_and_box_videos/update_game_list.html', args)
    elif video_type_name == 'game_details' or video_type_name == 'game_download':
        game = get_object_or_404(AndroidGame, pk=video.game_id)
        args['game'] = game
        return render(request, 'android/channel/fixed_position_videos/update_item_game_details.html', args
        )
    elif video_type_name in ('video', 'show', 'playlist'):
        if video.attached_game_type:
            game = AndroidGame.objects.get(id=video.game_id)
            args['game'] = game
            return render(request, 'android/channel/fixed_position_videos/update_video_with_game_details.html', args)
        else:
            return render(request, 'android/channel/fixed_position_videos/update_video.html', args)
            # return render(request, 'subchannel_and_module_items/android_update_item.html',
            #               {'item': item, 'channel_id': channel_id, 'subchannel_id': subchannel_id, 'module_id': module_id})


@login_required
def update_fixed_position_video(request):
    if request.method == 'POST':
        channel_id, subchannel_id, module_id = ('',) * 3
        try:
            post_dict = request.POST.dict()
            print post_dict
            channel_id = post_dict.pop('channel_id')
            subchannel_id = post_dict.pop('subchannel_id')
            video_id = post_dict.pop('id')
            module_id = post_dict.get('module_id')
            if video_id:
                video = AndroidFixedPositionVideo.objects.get(pk=video_id)
                if not module_id:
                    del post_dict['module_id']  #如果传过来module_id为''数据保存报错
                for k, v in post_dict.iteritems():
                    if hasattr(video, k):
                        setattr(video, k, v)
                if VideoType.to_s(int(video.video_type)) in ("game_details", 'game_download'):
                    video.game_id = AndroidGame.create_or_update(request.POST)
                if video.attached_game_type:
                    video.update_game_details_type_fields(request.POST)
                video.save()
        except Exception, e:
            print e
        return HttpResponseRedirect(reverse(
            'android_fixed_position_videos') + "?channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)


@login_required
def update_fixed_position_video_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        subchannel_id = request.GET.get('subchannel_id')
        module_id = request.GET.get('module_id')
        item = None
        if pk:
            if module_id:
                item = AndroidSubChannelModuleVideo.objects.get(id=int(pk))
            elif subchannel_id:
                item = AndroidSubChannelVideo.objects.get(id=int(pk))
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


@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def update_fixed_position_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                video = AndroidFixedPositionVideo.objects.get(id=int(video_id))
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
        fixed_position_video = AndroidFixedPositionVideo.objects.filter(module_id=int(module_id), is_delete=0, state=1,
                                                                        fixed_position=int(value))
    else:
        fixed_position_video = AndroidFixedPositionVideo.objects.filter(subchannel_id=int(subchannel_id), is_delete=0,
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
        AndroidFixedPositionVideo.objects.filter(pk=video_id).update(is_delete=1)
    except (AndroidSubChannelModuleVideo.DoesNotExist, AndroidSubChannelVideo.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('android_fixed_position_videos') + "?channel_id=" + channel_id +
                                "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)


