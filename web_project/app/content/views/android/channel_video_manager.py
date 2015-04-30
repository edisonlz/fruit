# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import AndroidChannel, AndroidChannelVideo, VideoType, AndroidVideoListModule, Status, BaseVideo
from content.models.game import AndroidGame
from content.views import get_paged_dict
from content.views.common import handle_batch_items
from django.db.models import Max
from app.content.views.common import redefine_item_pos, set_position


def channel_videos(request):
    if request.method == 'POST':
        video_ids = request.POST.get('item_ids')
        if video_ids:
            try:
                redefine_item_pos(AndroidChannelVideo, video_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get("channel_id")
        channel = get_object_or_404(AndroidChannel, pk=channel_id)
        channel_videos = AndroidChannelVideo.objects.filter(channel_id=channel_id, is_delete=False).order_by(
            '-position')
        for video in channel_videos:
            video.video_type_name = VideoType.to_s(video.video_type)
        return render(request, 'android/channel/channel_videos/android_channel_videos.html',
                      {'videos': channel_videos, 'channel': channel,
                       'video_state_hash': Status.STATUS_HASH,
                       'channel_id': channel_id
                      })


@login_required
def add_channel_video(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        video = AndroidChannelVideo()
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = request.POST.get('video_type', '')
        print "-------------", request.POST
        video.channel_id = channel_id
        channel = video.channel
        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'game_gift':
            video.add_game_gift_type_fields(request.POST)
        elif video_type_name == "game_details" or video_type_name == 'game_download':
            video.add_game_download_type_fields(request.POST)
        elif video_type_name == "video_with_game_details":
            video.add_video_with_game_details_type_fields(request.POST)
        elif video_type_name == "video_list":
            video.add_video_list_type_fields(request.POST)
        else:
            video.add_video_type_fields(request.POST)
        max_position = AndroidChannelVideo.objects.aggregate(Max('position'))[
                           'position__max'] or 0
        video.position = max_position + 1

        if BaseVideo.get_exist_video_in_box(video_type_name, AndroidChannelVideo, channel, 'channel_id', video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.state = 0
        video.save()
        return HttpResponseRedirect(reverse('android_query_channel_video', args={video.id, }))
    else:
        current_channel_id = request.GET.get('channel_id')
        video_type_list = AndroidChannelVideo.video_types(mock=True)
        return render(request, 'android/channel/channel_videos/android_add_video.html', {
            'video_type_list': video_type_list,
            'current_channel_id': current_channel_id,
        })


@login_required
def query_channel_video(request, video_id):
    video = get_object_or_404(AndroidChannelVideo, pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    channel = video.channel
    if video_type_name == 'game_details' or video_type_name == 'game_download':
        game = get_object_or_404(AndroidGame, pk=video.game_id)
        return render(request, 'android/channel/channel_videos/update_game_details.html', {'video': video,
                                                                                           'channel_id': channel.id,
                                                                                           'game': game})
    elif video_type_name == 'video_list':
        video_lists = AndroidVideoListModule.objects.filter(is_delete=False).order_by('position')
        return render(request, 'android/channel/channel_videos/update_video_list_details.html', {'video': video,
                                                                                                 'video_lists': video_lists,
                                                                                                 'channel_id': channel.id})
    elif video_type_name in ('video', 'show', 'playlist', 'url'):
        if video.attached_game_type:
            game = AndroidGame.objects.get(id=video.game_id)
            return render(request, 'android/channel/channel_videos/update_video_with_game_details.html',
                          {'video': video,
                           'game': game, 'channel_id': channel.id, })
        else:
            return render(request, 'android/channel/channel_videos/update_video_form_fields.html',
                          {'video': video, 'channel_id': channel.id})

            # return render(request, 'subchannel_and_module_items/android_update_item.html',
            #               {'item': item, 'channel_id': channel_id, 'subchannel_id': subchannel_id, 'module_id': module_id})


@login_required
def update_channel_video(request):
    if request.method == 'POST':
        channel_id = ''
        try:
            post_dict = request.POST.dict()
            channel_id = post_dict.pop('channel_id')
            video_id = post_dict.pop('id')
            if video_id:
                video = AndroidChannelVideo.objects.get(pk=video_id)
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
        return HttpResponseRedirect(reverse('android_channel_videos') + "?channel_id=" + channel_id)

        #return render(request, 'subchannel_and_module_items/android_update_item.html')


@login_required
# according to different "video_type" to dispatch corresponding field
def channel_video_add_video_fields(request):
    video_type = request.POST.get("video_type")
    if (video_type == "video"):
        return render(request, "android/channel/channel_videos/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "android/channel/channel_videos/url_form_fields.html")
    elif video_type == "video_list":
        video_lists = AndroidVideoListModule.objects.filter(is_delete=False).order_by('position')
        return render(request, "android/channel/channel_videos/video_list_form_fields.html", locals())


@login_required
def update_channel_video_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        value = request.POST.get('value')
        if pk:
            try:
                video = AndroidChannelVideo.objects.get(id=int(pk))
                if value == '1':
                    origin_video = AndroidChannelVideo.objects.filter(channel_id=video.channel_id, state=1,
                                                                      is_delete=0).exclude(id=video.id)
                    if not origin_video:
                        video.state = int(value)
                        video.save()
                        response = {'status': 'success'}
                    else:
                        response = {'status': 'error', 'msg': u"已有视频处于开启状态，请先关闭。"}
                else:
                    video.state = int(value)
                    video.save()
                    response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error', 'msg': u"视频不存在!"}
        else:
            response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def update_channel_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")

        if video_id and value and attribute:
            try:
                video = AndroidChannelVideo.objects.get(pk=int(video_id))
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
def delete_channel_video(request, video_id):
    channel_id = request.GET.get("channel_id", '')
    try:
        AndroidChannelVideo.objects.filter(pk=video_id).update(is_delete=1)
    except (AndroidChannelVideo.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('android_channel_videos') + "?channel_id=" + channel_id)


