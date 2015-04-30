# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import AndroidSubChannelModuleVideo, AndroidSubChannelVideo, AndroidChannel, AndroidSubChannel, \
    AndroidSubChannelModule, VideoType, AndroidVideoListModule, AndroidVideoListVideo, SyncJob, Status, SubChannel, \
    BaseVideo
from content.models.game import AndroidGame
from content.views import get_paged_dict
from content.views.common import handle_batch_items, redefine_item_pos, set_position


@login_required
def subchannel_module_items(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        module_id = request.POST.get('module_id')
        if item_ids:
            try:
                if module_id:
                    redefine_item_pos(AndroidSubChannelModuleVideo, item_ids)
                else:
                    redefine_item_pos(AndroidSubChannelVideo, item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        module_id = request.GET.get('select_module', '')
        channels = AndroidChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel, module = (None,) * 3
        subchannels, modules, items_list = ([],) * 3
        try:
            if channels and len(channels) > 0:
                channel = AndroidChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
                subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = AndroidSubChannel.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id else \
                    subchannels[0]
                if subchannel.type == 1:
                    modules = subchannel.module.filter(is_delete=0).order_by('-position')
                    if modules and len(modules) > 0:
                        module = AndroidSubChannelModule.objects.get(pk=module_id, is_delete=0) if module_id else \
                            modules[0]
                        items_list = module.moduleVideo.filter(is_delete=0).order_by('-position')
                else:
                    items_list = subchannel.subchannelVideo.filter(is_delete=0).order_by('-position')
        except (AndroidChannel.DoesNotExist, AndroidSubChannel.DoesNotExist, AndroidSubChannelModuleVideo.DoesNotExist,
                AndroidSubChannelVideo.DoesNotExist):
            pass
        for index, video in enumerate(items_list):
            items_list[index].copyright_for_view = video.copyright_for_view()
            items_list[index].pay_type_for_view = video.pay_type_for_view()
            items_list[index].video_type_for_view = video.video_type_for_view()
        commit_dict = {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules, 'this_module': module,
                       'video_state_hash': Status.STATUS_HASH,
                       'items': items_list}
        return render(request, 'android/channel/sub_channel_and_box_videos/videos.html', commit_dict)


@login_required
def add_subchannel_module_item(request, platform='android'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        if module_id:
            box_id = module_id
            box_id_column = 'module_id'
            box_class = AndroidSubChannelModule
            video_class = AndroidSubChannelModuleVideo
            video = AndroidSubChannelModuleVideo()
            set_position(video, AndroidSubChannelModuleVideo, {'module_id': module_id})
            video.module_id = module_id
        else:
            box_id = subchannel_id
            box_id_column = 'subchannel_id'
            box_class = AndroidSubChannel
            video_class = AndroidSubChannelVideo
            video = AndroidSubChannelVideo()
            set_position(video, AndroidSubChannelVideo, {'subchannel_id': subchannel_id})
            video.subchannel_id = subchannel_id
        box = box_class.objects.get(pk=box_id)
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = request.POST.get('video_type', '')

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
        if BaseVideo.get_exist_video_in_box(video_type_name, video_class, box, box_id_column, video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.state = 0
        video.save()
        # 去掉冗余视频
        if box_id:
            box = box_class.objects.get(pk=box_id)
            video.__class__.remove_redundant_videos_in_box(box, SubChannel.MaxVideoCountInSubChannel, box_id_column)

        return HttpResponseRedirect(reverse('android_query_sub_channel_module_item') + "?module_id=" + module_id +
                                    "&channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&item_id=" + str(
            video.id))
    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        channel = AndroidChannel.objects.get(pk=current_channel_id, is_delete=0)
        # subchannel = AndroidSubChannel.objects.get(pk=current_subchannel_id,is_delete=0)
        if current_module_id:
            module = AndroidSubChannelModule.objects.get(pk=current_module_id, is_delete=0)
            video_type_list = module.get_video_types(channel)
            s_image_tag = int(module.is_headline_module)
            game_banner_tag = int(module.is_game_banner_module)
            show_button_tag = int(channel.is_game_channel and s_image_tag)  #游戏频道下的轮播图类型抽屉 只显示一张轮播图 显示下载按钮
        else:
            s_image_tag, game_banner_tag, show_button_tag = (0,) * 3
            video_type_list = AndroidSubChannelVideo.video_types(mock=True)
        return render(request, 'android/channel/sub_channel_and_box_videos/add_video.html', {'platform': platform,
                                                                                             'video_type_list': video_type_list,
                                                                                             'current_channel_id': current_channel_id,
                                                                                             'current_subchannel_id': current_subchannel_id,
                                                                                             'current_module_id': current_module_id,
                                                                                             's_image_tag': s_image_tag,
                                                                                             'show_button_tag': show_button_tag,
                                                                                             'game_banner_tag': game_banner_tag})


@login_required
def query_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    item_id = request.GET.get('item_id', '')
    channel = AndroidChannel.objects.get(pk=channel_id, is_delete=0)

    if module_id:
        item = get_object_or_404(AndroidSubChannelModuleVideo, pk=item_id)
        module = AndroidSubChannelModule.objects.get(pk=module_id, is_delete=0)
        s_image_tag = int(module.is_headline_module)
        game_banner_tag = int(module.is_game_banner_module)
        show_button_tag = int(channel.is_game_channel and s_image_tag)
    else:
        s_image_tag, game_banner_tag, show_button_tag = (0,) * 3
        item = get_object_or_404(AndroidSubChannelVideo, pk=item_id)
    if game_banner_tag:
        #这里横图 竖图 对应 老版本 横屏 竖屏 待确认
        h_image_desc = '1248x110'
        v_image_desc = '688x110'
    else:
        h_image_desc = '448x252'
        v_image_desc = '200x300'
    s_image_desc = '448x252'
    video_type_name = VideoType.to_s(item.video_type)
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
        'video': item
    }
    if (video_type_name == "url"):
        return render(request, 'android/channel/sub_channel_and_box_videos/update_url_form_fields.html', args)
    elif (video_type_name == "game_gift"):
        return render(request, 'android/channel/sub_channel_and_box_videos/update_game_gift.html', args)
    elif (video_type_name == "game_list"):
        return render(request, 'android/channel/sub_channel_and_box_videos/update_game_list.html', args)
    elif video_type_name == 'game_details' or video_type_name == 'game_download':
        game = get_object_or_404(AndroidGame, pk=item.game_id)
        args['game'] = game
        return render(request, 'android/channel/sub_channel_and_box_videos/update_item_game_details.html', args)
    elif video_type_name in ('video', 'show', 'playlist'):
        if item.attached_game_type:
            game = AndroidGame.objects.get(id=item.game_id)
            args['game'] = game
            return render(request, 'android/channel/sub_channel_and_box_videos/update_video_with_game_details.html',
                          args)
        else:
            return render(request, 'android/channel/sub_channel_and_box_videos/update_video.html', args)
            # return render(request, 'subchannel_and_module_items/android_update_item.html',
            #               {'item': item, 'channel_id': channel_id, 'subchannel_id': subchannel_id, 'module_id': module_id})


@login_required
def update_subchannel_module_item(request):
    if request.method == 'POST':
        channel_id, subchannel_id, module_id = ('',) * 3
        try:
            post_dict = request.POST.dict()
            print post_dict
            channel_id = post_dict.pop('channel_id')
            subchannel_id = post_dict.pop('subchannel_id')
            item_id = post_dict.pop('id')
            module_id = post_dict.get('module_id')
            if item_id:
                if module_id:
                    module_item = AndroidSubChannelModuleVideo.objects.get(pk=item_id)
                else:
                    module_item = AndroidSubChannelVideo.objects.get(pk=item_id)
                for k, v in post_dict.iteritems():
                    if hasattr(module_item, k):
                        setattr(module_item, k, v)
                if VideoType.to_s(int(module_item.video_type)) in ("game_details", 'game_download'):
                    module_item.game_id = AndroidGame.create_or_update(request.POST)
                if module_item.attached_game_type:
                    module_item.update_game_details_type_fields(request.POST)
                module_item.save()
        except Exception, e:
            print e
        return HttpResponseRedirect(reverse(
            'android_sub_channel_module_items') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)

    return render(request, 'subchannel_and_module_items/android_update_item.html')


@login_required
def update_subchannel_module_item_status(request):
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
#频道页新增视频 根据视频类型渲染不同页面 与首页视频区分
def channel_page_add_video_fields(request):
    video_type = request.POST.get("video_type")
    show_button_tag = int(request.POST.get('show_button_tag'))
    s_image_tag = int(request.POST.get('s_image_tag'))
    game_banner_tag = int(request.POST.get('game_banner_tag'))
    if game_banner_tag:
        #这里横图 竖图 对应 老版本 横屏 竖屏 待确认
        h_image_desc = '1248x110'
        v_image_desc = '688x110'
    else:
        h_image_desc = '448x252'
        v_image_desc = '200x300'
    s_image_desc = '448x252'
    args = {'show_button_tag': show_button_tag, 's_image_tag': s_image_tag, 'game_banner_tag': game_banner_tag,
            'h_image_desc': h_image_desc, 'v_image_desc': v_image_desc, 's_image_desc': s_image_desc
    }
    if (video_type == "video"):
        return render(request, "android/channel/sub_channel_and_box_videos/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "android/channel/sub_channel_and_box_videos/url_form_fields.html", args)
    elif video_type == "game_gift":
        return render(request, "android/channel/sub_channel_and_box_videos/game_gift_form_fields.html", args)
    elif video_type == "game_list":
        return render(request, "android/channel/sub_channel_and_box_videos/game_list_form_fields.html", args)
    elif video_type == "game_details":
        return render(request, "android/channel/sub_channel_and_box_videos/game_details_form_fields.html", args)
    elif video_type == "game_download":
        return render(request, "android/channel/sub_channel_and_box_videos/game_download_form_fields.html", args)
    elif video_type == "video_with_game_details":
        return render(request, "android/channel/sub_channel_and_box_videos/video_with_game_details_form_fields.html")


@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def update_subchannel_module_item_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                if module_id:
                    video = AndroidSubChannelModuleVideo.objects.get(id=int(video_id))
                else:
                    video = AndroidSubChannelVideo.objects.get(id=int(video_id))
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
def delete_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    item_id = request.GET.get('item_id', '')
    try:
        if module_id:
            AndroidSubChannelModuleVideo.objects.filter(pk=item_id).update(is_delete=1)
        elif subchannel_id:
            AndroidSubChannelVideo.objects.filter(pk=item_id).update(is_delete=1)
    except (AndroidSubChannelModuleVideo.DoesNotExist, AndroidSubChannelVideo.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('android_sub_channel_module_items') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)


@login_required
def update_batch_items(request):
    get_dict = request.GET.dict()
    if get_dict.get('module_id'):
        model_name = 'AndroidSubChannelModuleVideo'
    else:
        model_name = 'AndroidSubChannelVideo'
    param_str = handle_batch_items(model_name, get_dict, request.POST.dict())
    return HttpResponseRedirect(reverse('android_sub_channel_module_items') + param_str)
