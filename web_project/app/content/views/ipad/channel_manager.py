# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import IpadChannel, Status, VideoType, CidDetail
from app.content.views.common import redefine_item_pos, set_position
from app.content.lib.channel_page_publish_tool import ChannelPagePublishTool
from app.content.lib.cache_plan import CachePlan


def save_channel(post_dict, channel):
    for k, v in post_dict.iteritems():
        if hasattr(channel, k):
            setattr(channel, k, v)
    channel.save()


@login_required
def channels(request):
    if request.method == 'POST':
        channel_ids = request.POST.get('channel_ids')
        if channel_ids:
            redefine_item_pos(IpadChannel, channel_ids)
        return HttpResponseRedirect(reverse('ipad_channels'))
    else:
        channels = IpadChannel.objects.filter(is_delete=0).order_by('-position')
        return render(request, 'channel/ipad_channels.html', {'channels': channels})


@login_required
def add_channel(request):
    if request.method == 'POST':
        channel = IpadChannel()
        set_position(channel, IpadChannel)
        save_channel(request.POST.dict(), channel)
        return HttpResponseRedirect(reverse('ipad_channels'))


@login_required
def update_channel_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            channel = IpadChannel.objects.get(id=int(request.POST.get('pk')))
            name = request.POST.get('name')
            value = request.POST.get('value')
            if hasattr(channel, name):
                setattr(channel, name, value)
            channel.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def query_channel(request, channel_id):
    channel = get_object_or_404(IpadChannel, pk=channel_id)
    return render(request, 'channel/ipad_update_channel.html', {'channel': channel})


@login_required
def update_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = IpadChannel.objects.get(id=pk_id)
            save_channel(request.POST.dict(), channel)
        except IpadChannel.DoesNotExist, e:
            pass
        return HttpResponseRedirect(reverse('ipad_new_channels'))


@login_required
def delete_channel(request, channel_id):
    try:
        IpadChannel.objects.filter(pk=channel_id).update(is_delete=1)
    except IpadChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('ipad_new_channels'))


@login_required
def new_channels(request):
    if request.method == 'POST':
        channel_ids = request.POST.get('item_ids')
        if channel_ids:
            try:
                redefine_item_pos(IpadChannel, channel_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channels = IpadChannel.objects.prefetch_related('channelVideo').filter(is_delete=0).order_by('-position')
        navigation_list = ["频道管理", "Ipad频道", "频道列表"]
        youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
        mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
        return render(request, 'ipad/channel/channels.html', {'channels': channels,
                                                              'youku_cid_details': youku_cid_details,
                                                              'mobile_cid_details': mobile_cid_details,
                                                              'channel_state_hash': Status.STATUS_HASH,
                                                              'navigation_list': enumerate(navigation_list)})


@login_required
def add_new_channel(request):
    if request.method == 'POST':
        channel = IpadChannel()
        content_type = request.POST.get("content_type",1)
        set_position(channel, IpadChannel)
        post_dict = request.POST.dict()
        post_dict['content_type'] = '1' # 默认优酷频道
        post_dict['show_type'] = '1' # 默认普通频道
        save_channel(post_dict, channel)
        return HttpResponseRedirect(reverse('ipad_new_channels'))


@login_required
def update_new_channel_status(request):
    if request.method == 'POST':
        channel_ids = request.POST.get("channel_ids")
        value = request.POST.get("value")
        try:
            if channel_ids and value:
                id_list = channel_ids.split(',')
                channel_objs = IpadChannel.objects.filter(id__in=id_list)
                if channel_objs:
                    channel_objs.update(state=value)
                    response = {'status': 'success', 'channel_ids': id_list}
                else:
                    raise IpadChannel.DoesNotExist
            else:
                raise ValueError('channel_ids or value is invalid!')
        except (IpadChannel.DoesNotExist, ValueError):
                response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def query_new_channel(request, channel_id):
    channel = get_object_or_404(IpadChannel, pk=channel_id)
    current_cid = CidDetail.objects.get(cid=channel.cid) if channel.cid else None
    is_youku_channel = current_cid.is_youku_channel if current_cid else None
    youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
    mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
    return render(request, 'ipad/channel/update_channel.html', locals())


@login_required
def update_new_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = IpadChannel.objects.get(id=pk_id)
            save_channel(request.POST.dict(), channel)
        except IpadChannel.DoesNotExist, e:
            pass
        return HttpResponseRedirect(reverse('ipad_new_channels'))


@login_required
def delete_new_channel(request, channel_id):
    try:
        IpadChannel.objects.filter(pk=channel_id).update(is_delete=1)
    except IpadChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('ipad_new_channels'))


@login_required
def channel_publish(request):
    if request.method == 'POST':
        channel_ids = [int(i) for i in request.POST.get('channel_ids').split(',')]
        # ret = ChannelPagePublishTool.channels_publish(channel_ids=channel_ids, platform='ipad')
        # 暂时不走发布逻辑，但是要调用发布校验
        channels = IpadChannel.objects.filter(pk__in=channel_ids)
        for channel in channels:
            check_result = ChannelPagePublishTool.check_channel_publish(platform='ipad', channel=channel)
            if check_result['status'] != 'success':
                if check_result.get('description', '') == 'channel_is_closed':
                    channel_ids.remove(channel.id)
                else:
                    desc = ChannelPagePublishTool.channel_check_error_info(check_result)
                    response = {'status': 'error', 'desc': desc}
                    return HttpResponse(json.dumps(response), content_type="application/json")
        try:
            for cache_key in ['ipad_channel_subtabs', 'ipad_subchannel_detail', 'ipad_nav_channels']:  # iPad3营销频道缓存 清不清？
                CachePlan.clean_cache(key=cache_key, params={'channel_ids': channel_ids})
            response = {'status': 'success'}
        except Exception, e:
            print e
            response = {'status': 'error', 'desc': u'清缓存失败'}

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pass