# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import IpadChannel, IpadSubChannel, IpadSubChannelModule, Status
from content.views.common import redefine_item_pos, set_position
from content.views.android.sub_channel_module_manager import get_filterinfo


@login_required
def subchannel_modules(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(IpadSubChannelModule, item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        channels = IpadChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel = (None,) * 2
        modules, subchannels = ([],) * 2
        if channels and len(channels) > 0:
            channel = IpadChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(type=1, is_delete=0).order_by('-position')
        if subchannels and len(subchannels) > 0:
            subchannel = IpadSubChannel.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id else subchannels[0]
            modules = subchannel.module.filter(is_delete=0).order_by('-position')
        areas, years, video_types, pay_kinds = get_filterinfo(channel.cid)
        exist_subchannels = IpadSubChannel.objects.defer('id', 'title')
        # subchannel_box_types_hash = IpadSubChannelModule.MODULE_TYPES
        # subchannel_box_types = IpadSubChannelModule.MODULE_TYPES.items()
        return render(request, 'subchannel_module/ipad_subchannel_modules.html', {
            'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
            'this_subchannel': subchannel, 'modules': modules, 'jump_channels': exist_subchannels,
            'areas': areas, 'video_types': video_types, 'years': years, 'pay_kinds': pay_kinds,
            # 'box_types': subchannel_box_types,
            # 'subchannel_box_types_hash': subchannel_box_types_hash,
            'module_state_hash': Status.STATUS_HASH})


@require_POST
@login_required
def add_subchannel_module(request):
    post_dict = request.POST.dict()
    channel_id, subchannel_id = (None,) * 2
    try:
        channel_id = post_dict.pop('channel_id')
        subchannel_id = post_dict.get('subchannel_id', '')
        module = IpadSubChannelModule()
        set_position(module, IpadSubChannelModule, {'subchannel_id': subchannel_id})
        for k, v in post_dict.iteritems():
            if hasattr(module, k):
                setattr(module, k, v)
        module.save()
    except KeyError:
        pass
    return HttpResponseRedirect(
        reverse('ipad_sub_channel_modules') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id)


@login_required
def query_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    module = get_object_or_404(IpadSubChannelModule, pk=module_id)
    return render(request, 'subchannel_module/ipad_update_subchannel_module.html',
                  {'module': module, 'channel_id': channel_id, 'subchannel_id': subchannel_id})


@require_POST
@login_required
def update_subchannel_module(request):
    channel_id, subchannel_id = request.POST.get('channel_id', ''), request.POST.get('subchannel_id', '')
    try:
        module = IpadSubChannelModule.objects.get(pk=int(request.POST.get('id')))
        name_dict = {'title': '', 'video_count': 20}
        for name, remain in name_dict.iteritems():
            if hasattr(module, name):
                setattr(module, name, request.POST.get(name, remain))
        module.save()
    except (ValueError, IpadSubChannelModule.DoesNotExist), e:
        pass
    finally:
        return HttpResponseRedirect(reverse('ipad_sub_channel_modules') + "?select_channel=" + channel_id +
                                    "&select_subchannel=" + subchannel_id)


@login_required
def update_subchannel_module_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk", '')
        module, response = (None,) * 2
        if pk.isdigit():
            try:
                module = IpadSubChannelModule.objects.get(id=int(pk))
                name, value = request.POST.get('name'), request.POST.get('value')
                if hasattr(module, name):
                    setattr(module, name, value)
                module.save()
                response = {'status': 'success'}
            except IpadSubChannelModule.DoesNotExist:
                response = {'status': 'error', 'msg': u"子频道模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        IpadSubChannelModule.objects.filter(pk=module_id).update(is_delete=1)
    except IpadSubChannelModule.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('ipad_sub_channel_modules') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id)
