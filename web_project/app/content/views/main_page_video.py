#coding=utf-8

import urllib, urllib2, json, logging

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
#from lib.util import DateUtil
from app.content.models import IpadBoxVideo, IphoneBoxVideo, AndroidBoxVideo, WinPhoneBoxVideo, HomeBox, \
    Platform, VideoType, Status, IosGame, AndroidGame

from django.conf import settings

#TODO: is this file useful?

@login_required
def videos(request, platform='ipad'):
    #platform = Platform.get_platform(request.path)

    #for drogable-sort
    if request.method == 'POST':
        pass
    else:
        #GET Come here
        #for index-page show
        #TODO: active modules

        box_list = HomeBox.objects.filter(platform=Platform.to_i(platform)).order_by('position')
        first_box_id = box_list.first() and box_list.first().id
        current_box_id = int(request.GET.get('box_id', 0)) or first_box_id

        if (platform == "ipad"):
            videos = IpadBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("position")
        elif (platform == "iphone"):
            videos = IphoneBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("position")
        elif (platform == "android"):
            videos = AndroidBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("position")
        elif (platform == "win_phone"):
            videos = WinPhoneBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("position")

        return render(request, 'videos/videos.html',
                      {
                          'videos': videos,
                          'platform': platform,
                          'box_list': box_list,
                          'current_box_id': current_box_id,
                          "platform": platform

                      })


@login_required
#def add_video(request, box_id):
def add_video(request, platform='ipad'):
    if request.method == 'POST':
        if platform == 'ipad':
            video = IpadBoxVideo()
        elif platform == 'iphone':
            video = IphoneBoxVideo()
        elif platform == 'android':
            video = AndroidBoxVideo()
        elif platform == 'win_phone':
            video = WinPhoneBoxVideo()
        else:
            raise Exception('PlatformError')

        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        video.video_type = VideoType.to_i(request.POST.get("video_type[]") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        current_box_id = request.POST.get("box_id")
        if current_box_id:
            video.box_id = int(current_box_id)
        else:
            raise Exception('No parent box')

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video': #video/show/playlist
            video.add_video_type_fields(request.POST)
        elif video_type_name == "live_broadcast":
            video.add_live_broadcast_type_fields(request.POST)
        elif video_type_name == "user":
            video.add_user_type_fields(request.POST)
        elif video_type_name == "game_list":
            video.add_game_list_type_fields(request.POST)
        elif video_type_name == "game_details":
            game_id = IosGame.create_or_update_ios_game(http_post=request.POST)
            if game_id:
                video.game_id = game_id
            else:
                # TODO 抛出游戏添加失败异常
                print '添加游戏失败'
                raise Exception
            # 游戏详情添加完跳转到视频列表页
            video.save()
            return HttpResponseRedirect(
                reverse("cms_main_page_videos", args=(platform, )) + "?box_id=" + str(current_box_id))
        elif video_type_name == "game_download":
            pass
        elif video_type_name == "video_with_game_details":
            pass
        elif video_type_name == "game_gift":
            video.add_game_gift_type_fields(request.POST)

        video.save()
        return HttpResponseRedirect(reverse("update_video", args=(platform, )) + "?id=" + str(video.id))
        #return HttpResponseRedirect(reverse('update_video', args=(platform, )))
    else:
        if platform == 'ipad':
            video_type_list = IpadBoxVideo.video_types(mock=True)
        elif platform == 'iphone':
            video_type_list = IphoneBoxVideo.video_types(mock=True)
        elif platform == 'android':
            video_type_list = AndroidBoxVideo.video_types(mock=True)
        elif platform == 'win_phone':
            video_type_list = WinPhoneBoxVideo.video_types(mock=True)
        else:
            raise Exception('PlatformError')
        current_box_id = request.GET.get('box_id')
        return render(request, 'videos/add_video_test.html', {'platform': platform, 'video_type_list': video_type_list,
                                                              'current_box_id': current_box_id})


@login_required
def query_video(request, platform, id):
    if (platform == "ipad"):
        video = get_object_or_404(IpadBoxVideo, pk=id)
    elif (platform == "iphone"):
        video = get_object_or_404(IphoneBoxVideo, pk=id)
    elif (platform == "android"):
        video = get_object_or_404(AndroidBoxVideo, pk=id)
    elif (platform == "win_phone"):
        video = get_object_or_404(WinPhoneBoxVideo, pk=id)

    return HttpResponseRedirect(reverse('update_video', args=(platform, )) + "?id=" + str(video.id))


@login_required
def update_video(request, platform):
    if request.method == 'POST':
        #if request.POST.get("video_type") == 'video':

        if (platform == "ipad"):
            video = IpadBoxVideo.objects.filter(id=request.POST.get("id")).first()
        elif (platform == "iphone"):
            video = IphoneBoxVideo.objects.filter(id=request.POST.get("id")).first()
        elif (platform == "android"):
            video = AndroidBoxVideo.objects.filter(id=request.POST.get("id")).first()
        elif (platform == "win_phone"):
            video = WinPhoneBoxVideo.objects.filter(id=request.POST.get("id")).first()

        video_type_name = VideoType.to_s(video.video_type)

        # common fields to save
        video.title = request.POST.get("title", '')
        video.subtitle = request.POST.get("subtitle", '')
        video.intro = request.POST.get("intro", '')
        video.h_image = request.POST.get("h_image", '')

        # video_type relative fields to save
        # please add exactly needed fields for each video_type
        if ( video_type_name == 'url' or
                     video_type_name == 'video' or
                     video_type_name == 'show' or
                     video_type_name == 'playlist' ):
            pass
        elif video_type_name == 'game_gift':
            video.game_page_id = request.POST.get('game_page_id', '')

        elif video_type_name == 'game_details':
            game_id = IosGame.create_or_update_ios_game(http_post=request.POST)
            video.game_id = game_id
        video.save()

        return HttpResponseRedirect(reverse('cms_main_page_videos', args=(platform, )) + "?box_id=" + str(video.box_id))
    else:
        video_pk = request.GET.get('id')
        if (platform == "ipad"):
            video = get_object_or_404(IpadBoxVideo, pk=video_pk)
        elif (platform == "iphone"):
            video = get_object_or_404(IphoneBoxVideo, pk=video_pk)
        elif (platform == "android"):
            video = get_object_or_404(AndroidBoxVideo, pk=video_pk)
        elif (platform == "win_phone"):
            video = get_object_or_404(WinPhoneBoxVideo, pk=video_pk)

        video_type_name = VideoType.to_s(video.video_type)
        #video = IpadBoxVideo.objects.get(id=int(request.GET.get("id")))

        print "\n-------video_type", video.video_type, "--------\n"
        if (video_type_name == "url"):
            return render(request, 'videos/update_url_form_fields.html', {'video': video, 'platform': platform})
        elif (video_type_name == 'video' or
                      video_type_name == 'show' or
                      video_type_name == 'playlist' ):
            return render(request, 'videos/update_video_form_fields.html', {'video': video, 'platform': platform})
        elif (video_type_name == "game_list"):
            game_type_list = get_game_type_list()
            print "-----game_type_list:", game_type_list, "----------------"
            return render(request, 'videos/update_game_list.html',
                          {'video': video, 'platform': platform, 'game_type_list': game_type_list})
        elif (video_type_name == "game_details"):
            print '*' * 100
            game = IosGame.objects.get(id=video.game_id)
            return render(request, 'videos/update_item_game_details.html', locals())
        elif (video_type_name == "game_gift"):
            return render(request, 'videos/update_game_gift.html', {'video': video, 'platform': platform})
        elif (video_type_name == "live_broadcast"):
            live_broadcast_paid = live_broadcast_type_is_paid()
            return render(request, 'videos/update_live_broadcast_form_fields.html',
                          {'video': video, 'platform': platform, "live_broadcast_paid": live_broadcast_paid})
        elif (video_type_name == "user"):
            return render(request, 'videos/update_user_form_fields.html', {'video': video, 'platform': platform})


            #last_video = IpadBoxVideo.objects.order_by("-id")[0]
            #return render(request, 'videos/update_video.html', {'video': last_video, 'platform': platform})


@login_required
def update_video_status(request, platform):
    print "------", request.POST, "------"
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            if (platform == "ipad"):
                bv = IpadBoxVideo.objects.get(id=int(pk))
            elif (platform == "iphone"):
                bv = IphoneBoxVideo.objects.get(id=int(pk))
            elif (platform == "android"):
                bv = AndroidBoxVideo.objects.get(id=int(pk))
            elif (platform == "win_phone"):
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
def delete_video(request, platform, id):
    if (platform == "ipad"):
        video = IpadBoxVideo.objects.get(pk=id)
    elif (platform == "iphone"):
        video = IphoneBoxVideo.objects.get(pk=id)
    elif (platform == "android"):
        video = AndroidBoxVideo.objects.get(pk=id)
    elif (platform == "win_phone"):
        video = WinPhoneBoxVideo.objects.get(pk=id)


    video.is_delete = 1
    video.save()
    box_id = video.box_id
    return HttpResponseRedirect(reverse('cms_main_page_videos', args=(platform, )) + "?box_id=" + str(box_id))


@login_required
# according to different "video_type" to dispatch corresponding field
def add_video_fields(request):
    video_type = request.POST.get("video_type")
    if (video_type == "video"):
        return render(request, "videos/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "videos/url_form_fields.html")
    elif video_type == "game_gift":
        return render(request, "videos/game_gift_form_fields.html")
    elif video_type == "game_list":
        return render(request, "videos/game_list_form_fields.html")
    elif video_type == "game_details":
        return render(request, "videos/game_details_form_fields.html")
    elif video_type == "live_broadcast":
        return render(request, "videos/live_broadcast_form_fields.html")
    elif video_type == "user":
        return render(request, "videos/user_form_fields.html")


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
                    data = {'error':e.code}
                else:
                    data = {'error':e}
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
                    data = {'error':e.code}
                else:
                    data = {'error':e}
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
    video_type_list = IpadBoxVideo.video_types(mock=True)
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


def sync_common_video(request, platform='ipad'):
    common_type = VideoType.KEYS[0:4]
    common_video_type = list(common_type)
    init_type_id = VideoType.to_i("video")
    current_type_id = int(request.GET.get("type_id", init_type_id))
    videos = IpadBoxVideo.objects.filter(video_type=current_type_id).order_by("position")
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


def sync_common_box(request, platform='ipad'):
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
    return  render(request, "common_module/iphone_box.html")
