# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import IphoneChannel,VideoType,Status
from app.content.views.common import redefine_item_pos, set_position
from app.content.lib.channel_page_publish_tool import ChannelPagePublishTool
from app.content.models import IphoneChannel,VideoType,Status,CidDetail
from app.content.views.common import redefine_item_pos, set_position
from app.content.lib.channel_page_publish_tool import ChannelPagePublishTool
from app.content.lib.cache_plan import CachePlan


def save_channel(request, channel):
    print '1'
    print request.POST
    channel.cid = request.POST.get('cid')
    channel.color = request.POST.get('color')
    channel.icon = request.POST.get('normal-img', '')
    channel.icon_52 = request.POST.get('selected-img', '')
    channel.icon_3_2 = request.POST.get('small-img', '')
    channel.icon_3_2_selected = request.POST.get('selected-img-small', '')
    channel.title = request.POST.get('title', '')
    # channel.position = 0
    # channel.state = 0
    channel.state_iphone_3_2, channel.switch_all, channel.switch_choiceness = 1, 0, 0
    channel.image_type_choiceness = 0
    channel.image_type_all = 0
    channel.save()


@login_required
def channels(request):
    if request.method == 'POST':
        channel_ids = request.POST.get('channel_ids')
        if channel_ids:
            redefine_item_pos(IphoneChannel, channel_ids)
        return HttpResponseRedirect(reverse('iphone_channels'))
    else:
        channels = IphoneChannel.objects.filter(is_delete=0).order_by('-position')
        return render(request, 'channel/iphone_channels.html', {'channels': channels})


@login_required
def add_channel(request):
    if request.method == 'POST':
        channel = IphoneChannel()
        set_position(channel, IphoneChannel)
        save_channel(request, channel)
        return HttpResponseRedirect(reverse('iphone_channels'))


@login_required
def update_channel_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            channel = IphoneChannel.objects.get(id=int(pk))
            value = request.POST.get("value")
            name = request.POST.get("name")
            if hasattr(channel, name):
                setattr(channel, name, value)
            channel.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"该数据不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def query_channel(request, channel_id):
    channel = get_object_or_404(IphoneChannel, pk=channel_id)
    return render(request, 'channel/iphone_update_channel.html', {'channel': channel})


@login_required
def update_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = IphoneChannel.objects.get(id=pk_id)
            save_channel(request, channel)
        except IphoneChannel.DoesNotExist, e:
            pass
        return HttpResponseRedirect(reverse('iphone_channels'))


@login_required
def delete_channel(request, channel_id):
    try:
        IphoneChannel.objects.filter(pk=channel_id).update(is_delete=1)
    except IphoneChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('iphone_channels'))


#以下为匹配原型图 新方法

@login_required
def new_channels(request):
    if request.method == 'POST':  # save the position
        channel_ids = request.POST.get('item_ids')
        if channel_ids:
            try:
                redefine_item_pos(IphoneChannel, channel_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channels = IphoneChannel.objects.filter(is_delete=0).order_by('-position')
        # content_type = request.GET.get("content_type",1)
        cid_details = CidDetail.objects.filter(is_delete=False)
        # if content_type:
        #    content_type = int(content_type)
        #    channels = channels.filter(content_type=content_type)
        content_type_hash = IphoneChannel.CONTENT_TYPE
        navigation_list = ["频道管理","Iphone频道","频道列表"]
        youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
        mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
        return render(request, 'iphone/channel/channels.html', {'channels': channels,
                                                                     # 'content_type_hash':content_type_hash,
                                                                     # 'content_type_list': content_type_hash.items(),
                                                                     # 'content_type': content_type,
                                                                     'channel_state_hash':Status.STATUS_HASH,
                                                                     'youku_cid_details': youku_cid_details,
                                                                     'mobile_cid_details': mobile_cid_details,
                                                                     'navigation_list': enumerate(navigation_list)})

@login_required
def update_new_channel_status(request):
    if request.method == 'POST':
        channel_ids = request.POST.get("channel_ids")
        value = request.POST.get("value")
        if channel_ids and value:
            try:
                hbs = IphoneChannel.objects.extra(where=['id IN (%s)' % channel_ids]).update(state=int(value))
                response = {'status': 'success', 'channel_ids': channel_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"视频不存在!"}
        else:
            response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def add_new_channel(request):
    if request.method == 'POST':
        channel = IphoneChannel()
        set_position(channel, IphoneChannel)
        save_channel(request, channel)
        # for key, value in request.POST.iteritems():
        #     if hasattr(channel, key):
        #         print(key,value)
        #         setattr(channel, key, value)
        # channel.save()
        return HttpResponseRedirect(reverse('iphone_new_channels'))

@login_required
def query_new_channel(request, channel_id):
    channel = get_object_or_404(IphoneChannel, pk=channel_id)
    current_cid = CidDetail.objects.get(cid=channel.cid) if channel.cid else None
    is_youku_channel = current_cid.is_youku_channel if current_cid else None
    youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
    mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
    return render(request, 'iphone/channel/update_channel.html', {'channel': channel,
                                                                  'youku_cid_details': youku_cid_details,
                                                                  'mobile_cid_details': mobile_cid_details,
                                                                  'current_cid': current_cid,
                                                                  'is_youku_channel': is_youku_channel})


@login_required
def update_new_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = IphoneChannel.objects.get(id=pk_id)
            # for k, v in request.POST.iteritems():
            #     if k != "id" and hasattr(channel, k):
            #         setattr(channel, k, v)
            # channel.save()
            save_channel(request, channel)
        except IphoneChannel.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('iphone_new_channels'))


@login_required
def delete_new_channel(request, channel_id):
    try:
        IphoneChannel.objects.filter(pk=channel_id).update(is_delete=1)
        content_type = request.GET.get("content_type",'1')
    except IphoneChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('iphone_new_channels'))


@login_required
def channel_publish(request):
    if request.method == 'POST':
        channel_ids = [int(i) for i in request.POST.get('channel_ids').split(',')]
        # ret = ChannelPagePublishTool.channels_publish(channel_ids=channel_ids, platform='iphone')
        # 暂时不走发布逻辑，但是要调用发布校验
        channels = IphoneChannel.objects.filter(pk__in=channel_ids)
        for channel in channels:
            check_result = ChannelPagePublishTool.check_channel_publish(platform='iphone', channel=channel)
            if check_result['status'] != 'success':
                if check_result.get('description', '') == 'channel_is_closed':
                    channel_ids.remove(channel.id)
                else:
                    desc = ChannelPagePublishTool.channel_check_error_info(check_result)
                    response = {'status': 'error', 'desc': desc}
                    return HttpResponse(json.dumps(response), content_type="application/json")
        try:
            for cache_key in ['iphone_channel_subtabs', 'iphone_subchannel_detail', 'iphone_channel_nav']:
                CachePlan.clean_cache(key=cache_key, params={'channel_ids': channel_ids})
            response = {'status': 'success'}
        except Exception, e:
            print e
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pass
