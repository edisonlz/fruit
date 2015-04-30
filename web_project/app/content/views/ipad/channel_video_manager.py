# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from content.models import IpadChannel, IpadChannelVideo, VideoType
from content.models.game import IosGame
from content.views import get_paged_dict
from content.views.common import handle_batch_items


def channel_videos(request):
    channel_id = request.GET.get("channel_id")
    channel = get_object_or_404(IpadChannel, pk=channel_id)
    channel_content_type_to_s = IpadChannel.CONTENT_TYPE[int(channel.content_type)]
    channel_videos = IpadChannelVideo.objects.filter(channel_id=channel_id, is_delete=False)
    for video in channel_videos:
        video.video_type_name = VideoType.to_s(video.video_type)
    navigation_list = ["频道管理", "Ipad频道", channel_content_type_to_s, '视频列表']
    return render(request, 'ipad/channel/channel_videos/ipad_channel_videos.html',
                  {'videos': channel_videos, 'channel': channel,
                   'navigation_list': enumerate(navigation_list),
                  })


@login_required
def add_channel_video(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        video = IpadChannelVideo()
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = request.POST.get('video_type', '')
        video.channel_id = channel_id
        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        else:
            video.add_video_type_fields(request.POST)
        video.position = 0
        video.state = 1
        video.save()
        return HttpResponseRedirect(reverse('ipad_query_channel_video', args={video.id, }))
    else:
        current_channel_id = request.GET.get('channel_id')
        video_type_list = IpadChannelVideo.video_types(mock=True)
        return render(request, 'ipad/channel/channel_videos/ipad_add_video.html', {
            'video_type_list': video_type_list,
            'current_channel_id': current_channel_id,
        })


@login_required
def query_channel_video(request, video_id):
    video = get_object_or_404(IpadChannelVideo, pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    channel = video.channel
    if video_type_name == 'game_details' or video_type_name == 'game_download':
        game = get_object_or_404(IosGame, pk=video.game_id)
        return render(request, 'ipad/channel/channel_videos/update_game_details.html', {'video': video,
                                                                                       'channel_id': channel.id,
                                                                                       'game': game})
    elif video_type_name in ('video', 'show', 'playlist', 'url'):
        if video.attached_game_type:
            game = IosGame.objects.get(id=video.game_id)
            return render(request, 'ipad/channel/channel_videos/update_video_with_game_details.html', {'video': video,
                                                                                                       'game': game,
                                                                                                       'channel_id': channel.id, })
        else:
            return render(request, 'ipad/channel/channel_videos/update_video_form_fields.html',
                          {'video': video, 'channel_id': channel.id})

            # return render(request, 'subchannel_and_module_items/ipad_update_item.html',
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
                video = IpadChannelVideo.objects.get(pk=video_id)
                for k, v in post_dict.iteritems():
                    if hasattr(video, k):
                        setattr(video, k, v)
                if VideoType.to_s(int(video.video_type)) in ("game_details", 'game_download'):
                    video.game_id = IosGame.create_or_update(request.POST)
                if video.attached_game_type:
                    video.update_game_details_type_fields(request.POST)
                video.save()
        except Exception, e:
            print e
        return HttpResponseRedirect(reverse('ipad_channel_videos') + "?channel_id=" + channel_id)

        #return render(request, 'subchannel_and_module_items/ipad_update_item.html')


@login_required
def update_channel_video_status(request):
    if request.method == 'POST':
        video_ids = request.POST.get("video_ids")
        value = request.POST.get("value")
        if video_ids and value:
            try:
                hbs = IpadChannelVideo.objects.extra(where=['id IN (%s)' % video_ids]).update(state=int(value))
                response = {'status': 'success', 'video_ids': video_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"视频不存在!"}
        else:
            response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_channel_video(request, video_id):
    channel_id = request.GET.get("channel_id", '')
    try:
        IpadChannelVideo.objects.filter(pk=video_id).update(is_delete=1)
    except (IpadChannelVideo.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('ipad_channel_videos') + "?channel_id=" + channel_id)


