#coding=utf-8

import urllib, urllib2, json, logging

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
#from lib.util import DateUtil
from app.content.models import WinPhoneBoxVideo, IphoneBoxVideo, AndroidBoxVideo, WinPhoneBoxVideo, HomeBox, \
    Platform, VideoType, Status, IosGame, AndroidGame, BaseVideo

from django.contrib import messages
from django.conf import settings


@login_required
def videos(request):
    #platform = Platform.get_platform(request.path)

    #for drogable-sort
    if request.method == 'POST':
        pass
    else:
        #GET Come here
        #for index-page show
        #TODO: active modules

        box_list = HomeBox.objects.filter(platform=Platform.to_i("win_phone")).order_by('position')
        first_box_id = box_list.first() and box_list.first().id
        current_box_id = int(request.GET.get('box_id', 0)) or first_box_id

        videos = WinPhoneBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("-position")

        return render(request, 'winphone/main_page/video_manage/videos.html',
                      {
                          'videos': videos,
                          'box_list': box_list,
                          'current_box_id': current_box_id,

                      })


@login_required
#def add_video(request, box_id):
def add_video(request):
    if request.method == 'POST':
        video = WinPhoneBoxVideo()

        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        current_box_id = request.POST.get("box_id")
        if current_box_id:
            video.box_id = int(current_box_id)
        else:
            raise Exception('No parent box')

        video.add_position(video.box_id)

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video':  #video/show/playlist
            video.add_video_type_fields(request.POST)

        box = HomeBox.objects.get(pk=video.box_id)
        if BaseVideo.get_exist_video_in_box(video_type_name, WinPhoneBoxVideo, box, 'box_id', video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.save()
        # 去掉冗余视频
        if video.box_id:
            box = HomeBox.objects.get(pk=video.box_id)
            AndroidBoxVideo.remove_redundant_videos_in_box(box, HomeBox.MaxVideoCountInBox)

        return HttpResponseRedirect(reverse("winphone_update_video") + "?id=" + str(video.id))
        #return HttpResponseRedirect(reverse('update_video', args=(platform, )))
    else:
        video_type_list = WinPhoneBoxVideo.video_types(mock=True)
        current_box_id = request.GET.get('box_id')
        return render(request, 'winphone/main_page/video_manage/add_video_test.html',
                      {'video_type_list': video_type_list,
                       'current_box_id': current_box_id})


@login_required
def query_video(request, id):
    video = get_object_or_404(WinPhoneBoxVideo, pk=id)

    return HttpResponseRedirect(reverse('winphone_update_video') + "?id=" + str(video.id))


@login_required
def update_video(request):
    if request.method == 'POST':
        #if request.POST.get("video_type") == 'video':

        video = WinPhoneBoxVideo.objects.filter(id=request.POST.get("id")).first()

        video_type_name = VideoType.to_s(video.video_type)

        if ( video_type_name == 'url'):
            video.update_url_type_fields(request.POST)
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            video.update_video_type_fields(request.POST)

        return HttpResponseRedirect(reverse('winphone_main_page_videos') + "?box_id=" + str(video.box_id))
    else:
        video_pk = request.GET.get('id')
        video = get_object_or_404(WinPhoneBoxVideo, pk=video_pk)

        video_type_name = VideoType.to_s(video.video_type)

        if (video_type_name == "url"):
            return render(request, 'winphone/main_page/video_manage/update_url_form_fields.html', {'video': video})
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            return render(request, 'winphone/main_page/video_manage/update_video_form_fields.html', {'video': video})


@login_required
def update_video_status(request):
    print "------", request.POST, "------"
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            bv = WinPhoneBoxVideo.objects.get(id=int(pk))
            bv.state = int(request.POST.get("value"))
            bv.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_video(request, id):
    video = WinPhoneBoxVideo.objects.get(pk=id)
    video.is_delete = 1
    video.save()
    box_id = video.box_id
    return HttpResponseRedirect(reverse('winphone_main_page_videos') + "?box_id=" + str(box_id))


@login_required
# according to different "video_type" to dispatch corresponding field
def add_video_fields(request):
    video_type = request.POST.get("video_type")
    if (video_type == "video"):
        return render(request, "winphone/main_page/video_manage/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "winphone/main_page/video_manage/url_form_fields.html")


def get_game_info(request):
    if request.method == 'GET':
        game_info = {}
        product = request.GET.get('product')
        if product == 'iPad':
            game_id = request.GET.get('game_id')
            print game_id
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error': e.code}
                else:
                    data = {'error': e}
        elif product == 'iphone':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error': e.code}
                else:
                    data = {'error': e}
        elif product == 'android':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.ANDROID_GAME_HOST,
                                                         path=settings.ANDROID_GAME_PATH, game_id=game_id)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error': e.code}
                else:
                    data = {'error': e}
    return HttpResponse(json.dumps(data))


def get_game_type_list():
    video_type_list = WinPhoneBoxVideo.video_types(mock=True)
    game_type_list = []
    for video_type in video_type_list:
        if (video_type.get("id") == VideoType.to_i("game_list") or video_type.get("id") == VideoType.to_i(
                "game_details") ):
            game_type_list.append(video_type)

    return game_type_list


def live_broadcast_type_is_paid():
    cost = {"id": 1, "desc": "付费"}
    free = {"id": 0, "desc": "免费"}
    live_broadcast_paid = []
    live_broadcast_paid.append(cost)
    live_broadcast_paid.append(free)

    return live_broadcast_paid


def sync_common_video(request, platform='winphone'):
    common_type = VideoType.KEYS[0:4]
    common_video_type = list(common_type)
    init_type_id = VideoType.to_i("video")
    current_type_id = int(request.GET.get("type_id", init_type_id))
    videos = WinPhoneBoxVideo.objects.filter(video_type=current_type_id).order_by("position")
    platform_list = get_platforms()
    box_list = get_boxes()

    return render(request, "videos/sync_common_video.html",
                  {
                      "videos": videos,
                      "platform": platform,
                      "common_video_type": common_video_type,
                      "current_type_id": current_type_id,
                      "platform_list": platform_list,
                      "box_list": box_list,
                  })


def sync_common_box(request, platform='winphone'):
    pass


def sync_video():
    pass


def get_platforms():
    platform_list = Platform.KEYS
    return platform_list


def get_boxes():
    box_list = []
    box = {}
    for hb in HomeBox.objects.filter(is_delete=0):
        box['box_id'] = hb.box_id
        box['title'] = hb.title
        box_list.append(box)
        box = {}

    return box_list


#######################
#公共模块
#######################
def common_module(request):
    return render(request, "common_module/iphone_box.html")
