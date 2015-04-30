#coding=utf-8
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from app.content.models.android_search_background import SearchBackgroundVideo
from app.content.models import VideoType, BaseVideo, AndroidVideoListModule,AndroidGame
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
import json

def search_back_img(request,):
    if request.method == 'POST':
        pass
    else:
        device_type_param = request.GET.get("device_type", "")
        print "--------------,device_type", device_type_param
        device_type = device_type_param or 'phone'
        videos = SearchBackgroundVideo.objects.filter(is_delete=0, device_type=device_type).order_by('-position')
        for index, video in enumerate(videos):
            videos[index].copyright_for_view = video.copyright_for_view()
        return render(request, "background_img/search_back/show_search_back_imgs.html",{'videos':videos, 'device_type':device_type})


def search_back_img_add_video(request,):
    if request.method == 'POST':
        video = SearchBackgroundVideo()
        video.add_position()
        #video.add_position(module_pk)

        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        device_type = request.POST.get('device_type')
        video.device_type = device_type
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        if video_type_name == 'video':  #video/show/playlist
            video.add_video_type_fields(request.POST)
            video.save()
            return render(request, "background_img/search_back/update_video_form_fields.html",
                          {"video":video, 'device_type':device_type})
        elif video_type_name == 'url':
            video.add_url_type_fields(request.POST)
            video.save()
            return render(request, "background_img/search_back/update_url_form_fields.html",
                          {"video":video, 'device_type':device_type})
        elif video_type_name == "live_broadcast":
            video.add_live_broadcast_type_fields(request.POST)
            video.save()
            live_broadcast_paid = live_broadcast_type_is_paid()
            return render(request, "background_img/search_back/update_live_broadcast_form_fields.html",
                          {"video":video, 'device_type':device_type, 'live_broadcast_paid':live_broadcast_paid })
        elif video_type_name == "video_list":
            video.video_list_id = request.POST.get('video_list_id')
            video.title = request.POST.get('title')
            video.save()
            video_lists = AndroidVideoListModule.objects.filter(is_delete=0)
            return render(request, "background_img/search_back/update_video_list_form_fields.html",
                          {"video":video, 'device_type':device_type, 'video_lists': video_lists })
        elif video_type_name in ['game_download','game_details']:
            video.add_game_download_type_fields(request.POST)
            video.save()
            return HttpResponseRedirect(reverse('search_back_img_manage')+"?device_type="+device_type)
        elif video_type_name == "game_list":
            video.add_game_list_type_fields(request.POST)
            video.save()
            return render(request, "background_img/search_back/update_game_list.html",
                          {"video":video, 'device_type':device_type})
    else:
        device_type = request.GET.get('device_type')
        video_type_list = SearchBackgroundVideo.video_types()
        return render(request, 'background_img/search_back/add_video.html',
                      {
                          'video_type_list': video_type_list,
                          'device_type': device_type
                          #'module_id': request.GET.get('module_id', 0)
                      })

def search_back_img_update_video(request, video_pk):
    if request.method == "POST":
        #video_pk = int(request.GET.get('video_id', 0))
        video = get_object_or_none(SearchBackgroundVideo, pk=int(video_pk))
        device_type = request.GET.get('device_type')

        video_type_name = VideoType.to_s(video.video_type)

        # common fields to save
        video.title = request.POST.get("title", '')
        video.subtitle = request.POST.get("subtitle", '')
        video.intro = request.POST.get("intro", '')
        video.h_image = request.POST.get("h_image", '')

        # video_type relative fields to save
        # please add exactly needed fields for each video_type
        if video_type_name == 'video':
            video.update_video_type_fields(request.POST)
        if video_type_name == 'url':
            video.update_url_type_fields(request.POST)
        elif video_type_name == 'live_broadcast':
            video.update_live_broadcast_type_fields(request.POST)
        elif video_type_name == 'video_list':
            video.update_video_list_type_fields(request.POST)
        elif video_type_name in ('game_details', 'game_download'):
            video.update_game_download_type_fields(request.POST)
        elif video_type_name == 'game_list':
            video.update_game_list_type_fields(request.POST)

        return HttpResponseRedirect(reverse('search_back_img_manage')+"?device_type="+device_type)
    else:
        video = get_object_or_none(SearchBackgroundVideo, pk=int(video_pk))
        device_type = request.GET.get('device_type')

        video_type_name = VideoType.to_s(video.video_type)
        if video_type_name == 'video':  #video/show/playlist
            return render(request, "background_img/search_back/update_video_form_fields.html",
                          {"video":video, "device_type":device_type })
        elif video_type_name == 'url':
            return render(request, "background_img/search_back/update_url_form_fields.html",
                          {"video":video, "device_type":device_type })
        elif video_type_name == "live_broadcast":
            live_broadcast_paid = live_broadcast_type_is_paid()
            return render(request, "background_img/search_back/update_live_broadcast_form_fields.html",
                          {"video":video, "device_type":device_type, 'live_broadcast_paid':live_broadcast_paid})
        elif video_type_name == 'video_list':
            video_lists = AndroidVideoListModule.objects.filter(is_delete=0)
            return render(request, "background_img/search_back/update_video_list_form_fields.html",
                          {"video":video, "device_type":device_type, 'video_lists':video_lists })
        elif video_type_name in ['game_download','game_details']:
            game = AndroidGame.objects.get(id=video.game_id)
            return render(request, "background_img/search_back/update_game_details.html",
                          {"video":video, "device_type":device_type, "game":game})
        elif video_type_name == 'game_list':
            return render(request, "background_img/search_back/update_game_list.html",
                          {"video":video, "device_type":device_type })


def search_back_img_delete_video(request, video_pk):
    video = get_object_or_none(SearchBackgroundVideo, pk=video_pk)
    device_type = request.GET.get('device_type')
    video.is_delete = 1
    video.save()
    return HttpResponseRedirect(reverse('search_back_img_manage')+"?device_type="+device_type)

def search_back_img_update_status(request,):
    if request.method == 'POST':
        opened_videos = SearchBackgroundVideo.objects.filter(is_delete=0, state=1, device_type=request.GET.get('device_type'))
        state = int(request.POST.get('value'))
        if opened_videos and state:
            response = {'status': 'error', 'msg': u"只能开启一个!"}
        else:
            video = get_object_or_none(SearchBackgroundVideo, pk=int(request.POST.get('pk')))
            if video:
                video.state = state
                video.save()
                response = {'status': 'success'}
            else:
                response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")

def live_broadcast_type_is_paid():
    cost = {"id": 1, "desc": "付费"}
    free = {"id": 0, "desc": "免费"}
    live_broadcast_paid = []
    live_broadcast_paid.append(cost)
    live_broadcast_paid.append(free)

    return live_broadcast_paid


# according to different "video_type" to dispatch corresponding field
def search_back_img_add_fields(request):
    video_type = request.POST.get("video_type")
    device_type = request.POST.get("device_type")
    if (video_type == "video"):
        return render(request, "background_img/search_back/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "background_img/search_back/url_form_fields.html", {"device_type": device_type })
    elif video_type == "game_list":
        return render(request, "background_img/search_back/game_list_form_fields.html", {'device_type': device_type })
    elif video_type in ["game_download", "game_details"]:
        return render(request, "background_img/search_back/game_details_form_fields.html", {'device_type': device_type })
    elif video_type == "live_broadcast":
        return render(request, "background_img/search_back/live_broadcast_form_fields.html")
    elif video_type == "video_list":
        video_list_modules = AndroidVideoListModule.objects.filter(is_delete=0)
        return render(request, "background_img/search_back/video_list_form_fields.html", {'video_list_modules':video_list_modules})


