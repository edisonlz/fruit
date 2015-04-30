# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import IphoneSubChannelModuleV4, IphoneSubChannelModuleV4Item, IphoneChannel, IphoneSubChannel, \
    IphoneSubChannelModule, IphoneSubChannelModuleVideo, IphoneSubChannelVideo, VideoType, IosGame, BaseVideo, \
    SubChannel
from content.views import get_paged_dict
from content.views.common import handle_batch_items, redefine_item_pos, set_position


@login_required
def subchannel_module_v4_items(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        channel_id = request.POST.get('this_channel_id')
        subchannel_id = request.POST.get('this_subchannel_id')
        module_id = request.POST.get('this_module_id')
        if module_id and item_ids:
            redefine_item_pos(IphoneSubChannelModuleV4Item, item_ids)
        return HttpResponseRedirect(reverse('iphone_sub_channel_module_v4_items') + "?select_channel=" + channel_id +
                                    "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        module_id = request.GET.get('select_module', '')
        channels = IphoneChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel, module = (None,) * 3
        subchannels, modules, items_list = ([],) * 3

        if channels and len(channels) > 0:
            channel = IphoneChannel.objects.get(pk=channel_id) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(is_delete=0, is_choiceness=1).order_by('-position')
        if subchannels and len(subchannels) > 0:
            subchannel = subchannels.get(pk=subchannel_id, is_delete=0) if subchannel_id else subchannels[0]
            if subchannel:
                modules = subchannel.module_v4.filter(is_delete=0).order_by('-position')
                if modules and len(modules) > 0:
                    module = IphoneSubChannelModuleV4.objects.get(is_delete=0, pk=module_id) if module_id else modules[
                        0]
                    items_list = module.moduleItem.filter(is_delete=0).order_by('-position')

        video_type_list = IphoneSubChannelModuleV4Item.video_types(mock=True)
        page_info_dict = get_paged_dict(items_list, request.GET.get('page', 1))
        for index, item in enumerate(page_info_dict['items']):
            page_info_dict['items'][index].video_type_name = VideoType.to_s(item.video_type)
            page_info_dict['items'][index].copyright_for_view = item.copyright_for_view()
            page_info_dict['items'][index].pay_type_for_view = item.pay_type_for_view()
        commit_dict = {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules, 'this_module': module,
                       'video_type_list': video_type_list}
        commit_dict.update(page_info_dict)
        return render(request, 'subchannel_and_module_items/iphone_v4_items.html', commit_dict)


@login_required
def add_subchannel_module_v4_item(request, platform='iphone'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')

        video = IphoneSubChannelModuleV4Item()
        set_position(video, IphoneSubChannelModuleV4Item, {'module_id': module_id})
        video.module_id = module_id
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        # video_type_name = VideoType.to_s(video.video_type)  # assert module_id

        video_type = request.POST.get('video_type', '')
        if video_type == 'url':  # handle url type
            video.add_url_type_fields(request.POST)
            # TODO: change 'screen-img' to 'h_image'
        else:  # handle video show playlist type
            video.add_video_type_fields(request.POST)

        video.state = 0
        video.save()

        return HttpResponseRedirect(reverse(
            'iphone_sub_channel_module_v4_items') + "?select_module=" + module_id + "&select_channel=" + channel_id + "&select_subchannel=" + subchannel_id)

    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        video_type_list = None
        if current_module_id:
            video_type_list = IphoneSubChannelModuleV4Item.video_types(mock=True)
        return render(request, 'subchannel_and_module_items/iphone_v4_add_item.html', {'platform': platform,
                                                                                       'video_type_list': video_type_list,
                                                                                       'current_channel_id': current_channel_id,
                                                                                       'current_subchannel_id': current_subchannel_id,
                                                                                       'current_module_id': current_module_id})


@login_required
def query_subchannel_module_v4_item(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    item_id = request.GET.get('item_id', '')
    item = None
    if module_id:
        item = get_object_or_404(IphoneSubChannelModuleV4Item, pk=item_id)
        if item:
            item.video_type_name = VideoType.to_s(item.video_type)
    return render(request, 'subchannel_and_module_items/iphone_v4_update_item.html',
                  {'item': item, 'channel_id': channel_id, 'subchannel_id': subchannel_id, 'module_id': module_id})


@login_required
def update_subchannel_module_v4_item(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        channel_id = post_dict.pop('channel_id')
        subchannel_id = post_dict.pop('subchannel_id')
        item_id = post_dict.pop('id')
        module_id = post_dict.get('module_id')
        try:
            if item_id:
                module_item = IphoneSubChannelModuleV4Item.objects.get(pk=item_id)
                for k, v in post_dict.iteritems():
                    if hasattr(module_item, k):
                        setattr(module_item, k, v)
                module_item.save()
        except IphoneSubChannelModuleV4Item.DoesNotExist:
            pass

        return HttpResponseRedirect(reverse(
            'iphone_sub_channel_module_v4_items') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)

    return render(request, 'subchannel_and_module_items/iphone_v4_update_item.html')


@login_required
def update_subchannel_module_v4_item_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        subchannel_id = request.GET.get('subchannel_id')
        module_id = request.GET.get('module_id')
        if pk and module_id:
            mi = IphoneSubChannelModuleV4Item.objects.get(id=int(pk))
            mi.state = int(request.POST.get("value"))
            mi.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module_v4_item(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    item_id = request.GET.get('item_id', '')
    if module_id:
        try:
            IphoneSubChannelModuleV4Item.objects.filter(pk=item_id).update(is_delete=1)
        except IphoneSubChannelModuleV4Item.DoesNotExist:
            pass
    return HttpResponseRedirect(reverse('iphone_sub_channel_module_v4_items') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id + "&select_module" + module_id)


@login_required
def update_v4_batch_items(request):
    get_dict = request.GET.dict()
    if get_dict.get('module_id'):
        model_name = 'IphoneSubChannelModuleV4Item'
        param_str = handle_batch_items(model_name, get_dict, request.POST.dict())
        return HttpResponseRedirect(reverse('iphone_sub_channel_module_v4_items') + param_str)
    else:
        HttpResponseRedirect(reverse('iphone_sub_channel_module_v4_items'))


@login_required
def subchannel_module_items(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        module_id = request.POST.get('module_id')
        if item_ids:
            try:
                if module_id:
                    redefine_item_pos(IphoneSubChannelModuleVideo, item_ids)
                else:
                    redefine_item_pos(IphoneSubChannelVideo, item_ids)
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
        channels = IphoneChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel, module = (None,) * 3
        subchannels, modules, items_list, video_type_list = ([],) * 4
        try:
            if channels and len(channels) > 0:
                channel = IphoneChannel.objects.get(pk=channel_id) if channel_id else channels[0]
                subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = IphoneSubChannel.objects.get(pk=subchannel_id) if subchannel_id else subchannels[0]
                if subchannel.type == 1:
                    modules = subchannel.module.filter(is_delete=0).order_by('-position')
                    if modules and len(modules) > 0:
                        module = IphoneSubChannelModule.objects.get(is_delete=0, pk=module_id) if module_id else \
                            modules[0]
                        items_list = module.moduleVideo.filter(is_delete=0).order_by('-position')
                        video_type_list = IphoneSubChannelModuleVideo.video_types(mock=True)
                else:
                    items_list = subchannel.subchannelVideo.order_by('-position')
                    video_type_list = IphoneSubChannelVideo.video_types(mock=True)
        except:
            pass

        page_info_dict = get_paged_dict(items_list, request.GET.get('page', 1))
        for index, item in enumerate(page_info_dict['items']):
            page_info_dict['items'][index].video_type_name = VideoType.to_s(item.video_type)
            page_info_dict['items'][index].copyright_for_view = item.copyright_for_view()
            page_info_dict['items'][index].pay_type_for_view = item.pay_type_for_view()
        print channel, channel.__dict__
        commit_dict = {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules, 'this_module': module,
                       'video_type_list': video_type_list}
        commit_dict.update(page_info_dict)
        # if commit_dict['this_module'] or commit_dict['this_subchannel']:
        # query_d = {
        # 'subchannel_id': subchannel.id if subchannel else None,
        #         'module_id': module.id if module else None,
        #         'plat_str': 'ipad',
        #     }
        #     commit_dict.update({'plans': SyncJob.plan_list(**query_d)})
        # else:
        #     commit_dict.update({'plans': []})
        return render(request, 'subchannel_and_module_items/iphone_items.html', commit_dict)


@login_required
def add_subchannel_module_item(request, platform='iphone'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', 0)
        subchannel_id = request.POST.get('subchannel_id', 0)
        module_id = request.POST.get('module_id', 0)
        if module_id:
            video = IphoneSubChannelModuleVideo()
            set_position(video, IphoneSubChannelModuleVideo, {'module_id': module_id})
            video.module_id = module_id
            box_id = module_id
            box_id_column = 'module_id'
            box_class = IphoneSubChannelModule
            video_class = IphoneSubChannelModuleVideo
        else:
            video = IphoneSubChannelVideo()
            set_position(video, IphoneSubChannelVideo, {'subchannel_id': subchannel_id})
            video.subchannel_id = subchannel_id
            box_id = subchannel_id
            box_id_column = 'subchannel_id'
            box_class = IphoneSubChannel
            video_class = IphoneSubChannelVideo
        box = box_class.objects.get(id=box_id)
        video_type_name = request.POST.get('video_type', '')
        video.video_type = VideoType.to_i(video_type_name or 0)

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video':
            video.add_video_type_fields(request.POST)
        elif video_type_name == "game_list":
            video.add_game_list_type_fields(request.POST)
        elif video_type_name == "game_details":
            video.add_game_download_type_fields(request.POST)
        # video.state = 0
        if BaseVideo.get_exist_video_in_box(video_type_name, video_class, box, box_id_column, video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.save()
        if box_id:
            box = box_class.objects.get(pk=box_id)
            video.__class__.remove_redundant_videos_in_box(box, SubChannel.MaxVideoCountInSubChannel, box_id_column)
        return HttpResponseRedirect(reverse(
            'iphone_query_sub_channel_module_item') + '?item_id=' + str(
            video.id) + '&channel_id=' + channel_id + '&subchannel_id=' + subchannel_id + '&module_id=' + module_id)
    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        video_type_list = None
        module_type = 0
        if current_module_id:
            video_type_list = IphoneSubChannelModuleVideo.video_types(mock=True)
            module = IphoneSubChannelModule.objects.filter(id=current_module_id).first()
            module_type = module.module_type if module else 0
        else:
            video_type_list = IphoneSubChannelVideo.video_types(mock=True)

        try:
            subchannel = IphoneSubChannel.objects.get(id=current_subchannel_id)
            choice_type = subchannel.is_choiceness
        except IphoneSubChannel.DoesNotExist, TypeError:
            choice_type = 0
        if not choice_type:
            video_type_list = video_type_list[:2]
        print video_type_list
        for v in video_type_list:
            print v['desc']
        return render(request, 'subchannel_and_module_items/iphone_add_item.html', {
            'platform': platform,
            'video_type_list': video_type_list,
            'module_type': module_type,
            'current_channel_id': current_channel_id,
            'current_subchannel_id': current_subchannel_id,
            'current_module_id': current_module_id
        })


@login_required
def query_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    video_id = request.GET.get('item_id', '')
    query_d = {'is_delete': 0}
    module_type = 0
    if module_id:
        query_d.update({'module_id': module_id})
        video = IphoneSubChannelModuleVideo.objects.get(id=video_id)
        module = IphoneSubChannelModule.objects.filter(id=module_id).first()
        module_type = module.module_type if module else 0
    else:
        query_d.update({'subchannel_id': subchannel_id})
        video = IphoneSubChannelVideo.objects.get(id=video_id)
    args = {
        'channel_id': channel_id,
        'subchannel_id': subchannel_id,
        'module_id': module_id,
        'module_type': module_type,
        'video': video,
    }
    video_type_name = VideoType.to_s(video.video_type)
    if video_type_name == "url":
        return render(request, 'subchannel_and_module_items/iphone_update_url.html', args)
    elif video_type_name in ['video', 'show', 'playlist']:
        return render(request, 'subchannel_and_module_items/iphone_update_video.html', args)
    elif video_type_name == "game_list":
        return render(request, 'subchannel_and_module_items/iphone_update_game_list.html', args)
    elif video_type_name == 'game_details':
        game = get_object_or_404(IosGame, pk=video.game_id)
        args['game'] = game
        return render(request, 'subchannel_and_module_items/iphone_update_game_details.html', args)


@login_required
def update_subchannel_module_item(request):
    if request.method == 'POST':
        try:
            post_dict = request.POST.dict()
            channel_id = post_dict.pop('channel_id')
            subchannel_id = post_dict.pop('subchannel_id')
            item_id = post_dict.pop('id')
            module_id = post_dict.get('module_id')
            if item_id:
                if module_id:
                    module_item = IphoneSubChannelModuleVideo.objects.get(pk=item_id)
                else:
                    module_item = IphoneSubChannelVideo.objects.get(pk=item_id)
                for k, v in post_dict.iteritems():
                    if hasattr(module_item, k):
                        setattr(module_item, k, v)
                module_item.save()
        except:
            pass

        return HttpResponseRedirect(reverse(
            'iphone_sub_channel_module_items') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)

    return render(request, 'subchannel_and_module_items/iphone_update_video.html')


@login_required
def update_subchannel_module_item_status(request):
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


@login_required
def delete_subchannel_module_item(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    item_id = request.GET.get('item_id', '')
    if module_id:
        IphoneSubChannelModuleVideo.objects.filter(pk=item_id).update(is_delete=1)
    elif subchannel_id:
        IphoneSubChannelVideo.objects.filter(pk=item_id).update(is_delete=1)
    return HttpResponseRedirect(reverse('iphone_sub_channel_module_items') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id + "&select_module=" + module_id)


@login_required
def update_batch_items(request):
    get_dict = request.GET.dict()
    if get_dict.get('module_id'):
        model_name = 'IphoneSubChannelModuleVideo'
    else:
        model_name = 'IphoneSubChannelVideo'
    param_str = handle_batch_items(model_name, get_dict, request.POST.dict())
    return HttpResponseRedirect(reverse('iphone_sub_channel_module_items') + param_str)


def update_subchannel_module_item_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                if module_id:
                    video = IphoneSubChannelModuleVideo.objects.get(id=int(video_id))
                else:
                    video = IphoneSubChannelVideo.objects.get(id=int(video_id))
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


def channel_page_add_video_fields(request):
    """control the image desc when add a new video"""
    video_type = str(request.POST.get("video_type"))
    module_type = request.POST.get("module_type", 0)
    args = {
        'module_type': int(module_type),
        's_image_desc': '448x252',
        'h_image_desc': '448x252',
        'v_image_desc': '200x300',
    }
    if video_type == "video":
        return render(request, "android/channel/sub_channel_and_box_videos/add_video_form_fields.html")
    elif video_type == "url":
        return render(request, "android/channel/sub_channel_and_box_videos/url_form_fields.html", args)
    elif video_type == "game_list":
        return render(request, "iphone/channel/sub_channel_and_box_videos/game_list_form_fields.html", args)
    elif video_type == "game_details":
        return render(request, "iphone/channel/sub_channel_and_box_videos/game_details_form_fields.html", args)


def get_img_desc(request):
    """control the image desc when update the video"""
    post = request.POST
    sub_id = post.get('subchannel_id')
    mod_id = post.get('module_id')

    img_descs = {
        'h_image_desc': '448x252',
        'v_image_desc': '200x300',
        's_image_desc': '448x252'
    }
    return HttpResponse(json.dumps(img_descs), content_type="application/json")