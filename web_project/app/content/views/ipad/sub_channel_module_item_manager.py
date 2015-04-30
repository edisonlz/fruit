# coding=utf-8
from app.content.views import get_paged_dict
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import IpadChannel, IpadSubChannel, IpadSubChannelModule, IpadSubChannelModuleItem, \
    IpadSubChannelItem, VideoType, Platform, SyncJob, SubChannel, BaseVideo
from app.content.models import IosGame
from app.content.views.common import handle_batch_items, redefine_item_pos, set_position


@login_required
def subchannel_module_items(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        module_id = request.POST.get('module_id')
        if item_ids:
            try:
                if module_id:
                    redefine_item_pos(IpadSubChannelModuleItem, item_ids)
                else:
                    redefine_item_pos(IpadSubChannelItem, item_ids)
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
        channels = IpadChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel, module = (None,) * 3
        subchannels, modules, items_list = ([],) * 3

        if channels and len(channels) > 0:
            channel = IpadChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
        if subchannels and len(subchannels) > 0:
            subchannel = IpadSubChannel.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id else subchannels[0]
            if subchannel.type == 1:
                modules = subchannel.module.filter(is_delete=0).order_by('-position')
            else:
                items_list = subchannel.subchannelItem.filter(is_delete=0).order_by('-position')
        if modules and len(modules) > 0:
            module = IpadSubChannelModule.objects.get(pk=module_id, is_delete=0) if module_id else modules[0]
            items_list = module.moduleItem.filter(is_delete=0).order_by('-position')

        page_info_dict = get_paged_dict(items_list, request.GET.get('page', 1))
        for index, item in enumerate(page_info_dict['items']):
            page_info_dict['items'][index].video_type_name = VideoType.to_s(item.video_type)
            page_info_dict['items'][index].copyright_for_view = item.copyright_for_view()
            page_info_dict['items'][index].pay_type_for_view = item.pay_type_for_view()

        commit_dict = {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules, 'this_module': module,
                       'platform': Platform.to_i('ipad')}
        commit_dict.update(page_info_dict)
        # if commit_dict['this_module'] or commit_dict['this_subchannel']:
        # query_d = {
        # 'subchannel_id': subchannel.id if subchannel else None,
        # 'module_id': module.id if module else None,
        #         'plat_str': 'ipad',
        #     }
        #     commit_dict.update({'plans': SyncJob.plan_list(**query_d)})
        # else:
        #     commit_dict.update({'plans': []})
        return render(request, 'subchannel_and_module_items/ipad_items.html', commit_dict)


@login_required
def add_subchannel_module_item(request, platform='ipad'):
    module_id = request.GET.get('module_id', '')
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')

        if module_id:
            video = IpadSubChannelModuleItem()
            set_position(video, IpadSubChannelModuleItem, {'module_id': module_id})
            video.module_id = module_id
            query_id = module_id
            module_id_column = 'module_id'
            module_class = IpadSubChannelModule
            video_class = IpadSubChannelModuleItem
        else:
            video = IpadSubChannelItem()
            set_position(video, IpadSubChannelItem, {'subchannel_id': subchannel_id})
            video.subchannel_id = subchannel_id
            query_id = subchannel_id
            module_id_column = 'subchannel_id'
            module_class = IpadSubChannel
            video_class = IpadSubChannelItem
        the_module = module_class.objects.get(id=query_id)

        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)  # assert module_id

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name in ['video', 'show', 'playlist']:
            video.add_video_type_fields(request.POST)
        if BaseVideo.get_exist_video_in_box(video_type_name, video_class, the_module, module_id_column, video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.state = 0
        video.save()
        if module_id:
            box = module_class.objects.get(pk=module_id)
            video.__class__.remove_redundant_videos_in_box(box, SubChannel.MaxVideoCountInSubChannel, module_id_column)
        return HttpResponseRedirect(reverse(
            'ipad_query_sub_channel_module_item') + "?module_id=" + module_id + "&channel_id=" + channel_id +
                                    "&subchannel_id=" + subchannel_id + '&video_id=' + str(video.id))

    else:
        if module_id:
            video_type_list = IpadSubChannelModuleItem.video_types(mock=True)
        else:
            video_type_list = IpadSubChannelItem.video_types(mock=True)
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        return render(request, 'ipad/channel/sub_channel_and_box_videos/add_video.html', {
            'platform': platform,
            'video_type_list': video_type_list,
            'current_channel_id': current_channel_id,
            'current_subchannel_id': current_subchannel_id,
            'current_module_id': current_module_id
        })


@login_required
def query_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    video_id = request.GET.get('video_id', '')
    if module_id:
        video = get_object_or_404(IpadSubChannelModuleItem, pk=video_id)
        module = IpadSubChannelModule.objects.get(pk=module_id, is_delete=0)
        s_image_tag = int(module.is_headline_module)
    else:
        video = get_object_or_404(IpadSubChannelItem, pk=video_id)
        s_image_tag = 0
    video_type_name = VideoType.to_s(video.video_type)
    h_image_desc = '448x252'
    v_image_desc = '200x300'
    s_image_desc = IpadChannel.objects.get(pk=channel_id).image_size_of_slider_module
    args = {
        's_image_tag': s_image_tag,
        'h_image_desc': h_image_desc,
        'v_image_desc': v_image_desc,
        's_image_desc': s_image_desc,
        'channel_id': channel_id,
        'subchannel_id': subchannel_id,
        'module_id': module_id,
        'video': video,
    }
    if video_type_name == "url":
        return render(request, 'ipad/channel/sub_channel_and_box_videos/update_url_form_fields.html', args)
    elif video_type_name in ('video', 'show', 'playlist'):
        return render(request, 'ipad/channel/sub_channel_and_box_videos/update_video.html', args)


@login_required
def update_subchannel_module_item(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        module_id = post_dict.pop("module_id")
        channel_id = post_dict.pop("channel_id")
        subchannel_id = post_dict.pop("subchannel_id")
        sel_id = int(post_dict.pop('id'))
        sel_item = IpadSubChannelModuleItem.objects.get(id=sel_id) if module_id else IpadSubChannelItem.objects.get(
            id=sel_id)
        for k, v in post_dict.iteritems():
            if hasattr(sel_item, k):
                setattr(sel_item, k, v)
        sel_item.save()
        # TODO 其他视频类型
        return HttpResponseRedirect(reverse(
            'ipad_sub_channel_module_items') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)


@login_required
# 频道页新增视频 根据视频类型渲染不同页面 与首页视频区分
def channel_page_add_video_fields(request):
    video_type = request.POST.get("video_type")
    module_id = request.POST.get("module_id") or 0
    module = IpadSubChannelModule.objects.filter(id=int(module_id), is_delete=0)
    s_image_tag = 1 if module and module[0].is_headline_module else 0
    h_image_desc = '448x252'
    v_image_desc = '200x300'
    s_image_desc = '720x194'
    args = {'s_image_tag': s_image_tag,
            'h_image_desc': h_image_desc, 'v_image_desc': v_image_desc, 's_image_desc': s_image_desc
    }
    if (video_type == "video"):
        return render(request, "ipad/channel/sub_channel_and_box_videos/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "ipad/channel/sub_channel_and_box_videos/url_form_fields.html", args)


@login_required
def update_subchannel_module_item_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        subchannel_id = request.GET.get('subchannel_id')
        module_id = request.GET.get('module_id')
        if pk:
            if module_id:
                mi = IpadSubChannelModuleItem.objects.get(id=int(pk))
            else:
                mi = IpadSubChannelItem.objects.get(id=int(pk))
            mi.state = int(request.POST.get("value"))
            mi.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    item_id = request.GET.get('item_id', '')
    page = request.GET.get('page', '1')
    if not page.isdigit():
        page = 1
    if module_id:
        IpadSubChannelModuleItem.objects.filter(pk=item_id).update(is_delete=1)
    else:
        IpadSubChannelItem.objects.filter(pk=item_id).update(is_delete=1)

    return HttpResponseRedirect(reverse('ipad_sub_channel_module_items') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id + "&select_module=" + module_id + "&page=" + page)


@login_required
def update_batch_items(request):
    get_dict = request.GET.dict()
    if get_dict.get('module_id'):
        model_name = 'IpadSubChannelModuleItem'
    else:
        model_name = 'IpadSubChannelItem'

    param_str = handle_batch_items(model_name, get_dict, request.POST.dict())
    return HttpResponseRedirect(reverse('ipad_sub_channel_module_items') + param_str)


@login_required
def update_subchannel_module_item_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                if module_id:
                    video = IpadSubChannelModuleItem.objects.get(id=int(video_id))
                else:
                    video = IpadSubChannelItem.objects.get(id=int(video_id))
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