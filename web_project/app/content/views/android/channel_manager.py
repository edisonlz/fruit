# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

import json
from app.content.models import AndroidChannel, VideoType, Status, CidDetail,AndroidChannelNavigation
from app.content.views.common import redefine_item_pos, set_position
from app.content.lib.channel_page_publish_tool import ChannelPagePublishTool
from app.content.lib.cache_plan import CachePlan


@login_required
def channels(request):
    if request.method == 'POST':  # save the position
        channel_ids = request.POST.get('channel_ids')
        if channel_ids:
            redefine_item_pos(AndroidChannel, channel_ids)
        return HttpResponseRedirect(reverse(''))
    else:
        channels = AndroidChannel.objects.filter(is_delete=0).order_by('-position')
        color_board = AndroidChannel.COLOR_BOARD
        return render(request, 'channel/android_channels.html', {'channels': channels, 'color_board': color_board})


@login_required
def add_channel(request):
    if request.method == 'POST':
        channel = AndroidChannel()
        set_position(channel, AndroidChannel)
        for key, value in request.POST.iteritems():
            if hasattr(channel, key):
                print(key, value)
                setattr(channel, key, value)
        channel.save()
        return HttpResponseRedirect(reverse('android_channels'))


@login_required
def update_channel_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hm = AndroidChannel.objects.get(id=int(pk))
            data = int(request.POST.get("value"))
            field = request.POST.get("name")
            hm.__dict__[field] = data
            hm.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def query_channel(request, channel_id):
    channel = get_object_or_404(AndroidChannel, pk=channel_id)
    color_board = AndroidChannel.COLOR_BOARD
    return render(request, 'channel/android_update_channel.html', {'channel': channel, 'color_board': color_board})


@login_required
def update_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = AndroidChannel.objects.get(id=pk_id)
            for k, v in request.POST.iteritems():
                if k != "id" and hasattr(channel, k):
                    setattr(channel, k, v)
            channel.save()
        except AndroidChannel.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('android_channels'))


@login_required
def delete_channel(request, channel_id):
    try:
        AndroidChannel.objects.filter(pk=channel_id).update(is_delete=1)
    except AndroidChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('android_channels'))


#以下为匹配原型图 新方法
@login_required
def new_channels(request):
    if request.method == 'POST':  # save the position
        channel_ids = request.POST.get('item_ids')
        if channel_ids:
            try:
                redefine_item_pos(AndroidChannel, channel_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channels = AndroidChannel.objects.prefetch_related('channelVideo').filter(is_delete=0).order_by('-position')
        content_type = request.GET.get("content_type")
        navigations = AndroidChannelNavigation.objects.filter(is_delete=0,state=1).order_by('nav_type')
        if content_type:
            content_type = int(content_type)
        else:
            if navigations:
                content_type = navigations[0].nav_type
            else:
                content_type = 0
        channels = channels.filter(content_type=content_type)
        content_type_hash = {navi.nav_type:navi.title for navi in navigations} if navigations else {}
        color_board = AndroidChannel.COLOR_BOARD
        cid_details = CidDetail.objects.filter(is_delete=False)
        navigation_list = ["频道管理", "Android频道", "频道列表"]
        youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
        mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
        for channel in channels:
            if channel.show_type == 1:
                channel.show_type_info = '普通频道'
            else:
                #channel.show_type_info = VideoType.to_s(channel.channelVideo.first().video_type) 直接用外键关联依然有1+n问题
                cache_videos = channel._prefetched_objects_cache['channelVideo']
                available_videos = filter(lambda video : video.state == 1 and video.is_delete == 0,cache_videos)
                if available_videos:
                    video_type_to_s = VideoType.to_s(available_videos[0].video_type)
                    channel.show_type_info = '视频推广' + "-" + video_type_to_s
                else:
                    channel.show_type_info = '视频推广'

        return render(request, 'android/channel/channels.html', {'channels': channels, 'color_board': color_board,
                                                                 'channel_navigations': navigations,
                                                                 'content_type_hash': content_type_hash,
                                                                 'content_type': content_type,
                                                                 'channel_state_hash': Status.STATUS_HASH,
                                                                 'navigation_list': enumerate(navigation_list),
                                                                 'youku_cid_details': youku_cid_details,
                                                                 'mobile_cid_details': mobile_cid_details})


@login_required
def update_new_channel_status(request):
    if request.method == 'POST':
        channel_ids = request.POST.get("channel_ids")
        value = request.POST.get("value")
        if channel_ids and value:
            try:
                hbs = AndroidChannel.objects.extra(where=['id IN (%s)' % channel_ids]).update(state=int(value))
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
        channel = AndroidChannel()
        content_type = request.POST.get("content_type") or '1'
        print content_type,"content_type"
        set_position(channel, AndroidChannel)
        for key, value in request.POST.iteritems():
            if hasattr(channel, key):
                setattr(channel, key, value)
        channel.save()
        return HttpResponseRedirect(reverse('android_new_channels') + "?content_type=" + content_type)


@login_required
def query_new_channel(request, channel_id):
    channel = get_object_or_404(AndroidChannel, pk=channel_id)
    channel.content_type_info = AndroidChannel.CONTENT_TYPE.get(channel.content_type)
    cid_details = CidDetail.objects.filter(is_delete=False)
    if channel.show_type == 1:
        channel.show_type_info = '普通频道'
    else:
        channel.show_type_info = '视频推广'
    color_board = AndroidChannel.COLOR_BOARD
    current_cid = CidDetail.objects.get(cid=channel.cid) if channel.cid else None
    is_youku_channel = current_cid.is_youku_channel if current_cid else None
    youku_cid_details = CidDetail.objects.filter(is_youku_channel=1, is_delete=False).order_by('cid')
    mobile_cid_details = CidDetail.objects.filter(is_youku_channel=0, is_delete=False).order_by('cid')
    return render(request, 'android/channel/update_channel.html',
                  {'channel': channel, 'color_board': color_board, 'current_cid': current_cid,
                   'is_youku_channel': is_youku_channel, 'youku_cid_details': youku_cid_details,
                   'mobile_cid_details': mobile_cid_details})


@login_required
def update_new_channel(request):
    if request.method == 'POST':
        pk_id = request.POST.get("id")
        try:
            channel = AndroidChannel.objects.get(id=pk_id)
            for k, v in request.POST.iteritems():
                if k != "id" and hasattr(channel, k):
                    setattr(channel, k, v)
            channel.save()
        except AndroidChannel.DoesNotExist:
            pass
        return HttpResponseRedirect(reverse('android_new_channels') + "?content_type=" + str(channel.content_type))


@login_required
def delete_new_channel(request, channel_id):
    try:
        AndroidChannel.objects.filter(pk=channel_id).update(is_delete=1)
        content_type = request.GET.get("content_type", '1')
    except AndroidChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('android_new_channels') + "?content_type=" + content_type)


@login_required
def channel_publish(request):
    if request.method == 'POST':
        channel_ids = [int(i) for i in request.POST.get('channel_ids').split(',')]
        # ret = ChannelPagePublishTool.channels_publish(channel_ids=channel_ids, platform='android')
        # 暂时不走发布逻辑，但是要调用发布校验
        channels = AndroidChannel.objects.filter(pk__in=channel_ids)
        for channel in channels:
            check_result = ChannelPagePublishTool.check_channel_publish(platform='android', channel=channel)
            if check_result['status'] != 'success':
                if check_result.get('description', '') == 'channel_is_closed':
                    channel_ids.remove(channel.id)
                else:
                    desc = ChannelPagePublishTool.channel_check_error_info(check_result)
                    response = {'status': 'error', 'desc': desc}
                    return HttpResponse(json.dumps(response), content_type="application/json")
        try:
            for cache_key in ['android_subchannel_tabs', 'android_subchannel_detail', 'android_user_tag']:
                CachePlan.clean_cache(key=cache_key, params={'channel_ids': channel_ids})
            response = {'status': 'success'}
        except Exception, e:
            print e
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pass





