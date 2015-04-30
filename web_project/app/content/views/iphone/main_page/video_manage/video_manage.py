# coding=utf-8
import urllib2, json, logging
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from app.content.models import IpadBoxVideo, IphoneBoxVideo, AndroidBoxVideo, WinPhoneBoxVideo, HomeBox, \
    Platform, VideoType, Status, IosGame, AndroidGame,BaseVideo
from django.conf import settings
from app.content.views.common import handle_batch_items, redefine_item_pos
from django.core.exceptions import ObjectDoesNotExist
from wi_model_util.imodel import get_object_or_none


ADD_SLIDER_IMAGE = {'name': 's_image', 'desc': '轮播图(600x338)'}
ADD_HORIZONTAL_IMAGE = {'name': 'h_image', 'desc': '横图(448x252)'}


@login_required
def videos(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(IphoneBoxVideo, item_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        #TODO: active modules ?
        try:
            current_box_id = int(request.GET.get('box_id'))
            box = HomeBox.objects.filter(platform=Platform.to_i("iphone"), is_delete=0, pk=current_box_id).order_by(
                '-position').first()
            is_slider_box = box.is_slider_box()#是否是轮播图模块
            videos = IphoneBoxVideo.objects.filter(box_id=current_box_id, is_delete=0).order_by("-position")
            for index, video in enumerate(videos):
                videos[index].copyright_for_view = video.copyright_for_view()
                videos[index].pay_type_for_view = video.pay_type_for_view()
                videos[index].video_type_for_view = video.video_type_for_view()
            return render(request, 'iphone/main_page/video_manage/videos.html', {'videos': videos,
                                                                                 'box': box,
                                                                                 'current_box_id': current_box_id,
                                                                                 'video_state_hash':Status.STATUS_HASH,
                                                                                 'is_slider_box':is_slider_box
                                                                                 })
        except (ValueError, ObjectDoesNotExist), e:
            return HttpResponseRedirect(reverse('iphone_uniq_modules'))


@login_required
def add_video(request):
    if request.method == 'POST':
        video = IphoneBoxVideo()
        is_slider_box = request.POST.get('is_slider_box')
        print "params:-----", request.POST

        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        current_box_id = request.POST.get("box_id")
        if current_box_id:
            video.box_id = int(current_box_id)
        else:
            raise Exception('No parent box')
        # current_box = get_object_or_none(HomeBox, pk=current_box_id)
        # is_slider_box = request.POST.get("is_slider_box", False)
        # print "in add_video-------is_slider_box", is_slider_box
        # if is_slider_box:
        #     video.s_image = request.POST.get("image", "")

        video.add_position(video.box_id)
        if video_type_name == 'url':
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video':  #video/show/playlist
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_video_type_fields(request.POST)
        elif video_type_name == "game_list":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_game_list_type_fields(request.POST)
        elif video_type_name == "live_broadcast":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_live_broadcast_type_fields(request.POST)
        elif video_type_name == "user":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_user_type_fields(request.POST)
        elif video_type_name == "game_details":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_game_download_type_fields(request.POST)
            #video.add_game_details_type_fields(request.POST)
            # 游戏详情添加完跳转到视频列表页
            box = HomeBox.objects.get(pk=video.box_id)
            if BaseVideo.get_exist_video_in_box(video_type_name,IphoneBoxVideo,box,'box_id',video):
                messages.error(request, '视频已经存在')
                return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
            video.save()
            return HttpResponseRedirect(
                reverse("iphone_main_page_videos") + "?box_id=" + str(current_box_id))
        elif video_type_name == "game_gift":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.add_game_gift_type_fields(request.POST)
        # elif video_type_name == "video_with_game_details":
        #     video.add_video_type_fields(request.POST)
        #     video.video_type = VideoType.to_i("video_with_game_details")
        #     video.game_id = IosGame.create_or_update(params=request.POST).id

        box = HomeBox.objects.get(pk=video.box_id)
        if BaseVideo.get_exist_video_in_box(video_type_name,IphoneBoxVideo,box,'box_id',video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
        video.save()
        # 去掉冗余视频
        if video.box_id:
            box = HomeBox.objects.get(pk=video.box_id)
            AndroidBoxVideo.remove_redundant_videos_in_box(box, HomeBox.MaxVideoCountInBox)

        #return HttpResponseRedirect(reverse("iphone_update_video") + "?id=" + str(video.id)+"&is_slider_box=" + is_slider_box)
        return HttpResponseRedirect(reverse("iphone_update_video") + "?id=" + str(video.id))
        #return HttpResponseRedirect(reverse('update_video', args=(platform, )))
    else:
        video_type_list = IphoneBoxVideo.video_types(mock=True)
        current_box_id = int(request.GET.get('box_id'))
        current_box = get_object_or_none(HomeBox, pk=current_box_id)
        is_slider_box = (current_box.box_type == 2)#是否是轮播图模块
        return render(request, 'iphone/main_page/video_manage/add_video_test.html',
                      {
                          'video_type_list': video_type_list,
                          'current_box_id': current_box_id,
                          'is_slider_box': is_slider_box
                      })


@login_required
def query_video(request, id):
    video = get_object_or_404(IphoneBoxVideo, pk=id)
    return HttpResponseRedirect(reverse('iphone_update_video') + "?id=" + str(video.id))


@login_required
def update_video(request):
    if request.method == 'POST':
        video = IphoneBoxVideo.objects.filter(id=request.POST.get("id")).first()
        video_type_name = VideoType.to_s(video.video_type)
        is_slider_box = request.POST.get('is_slider_box')

        # video_type relative fields to save
        # please add exactly needed fields for each video_type
        if ( video_type_name == 'url'):
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_url_type_fields(request.POST)
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_video_type_fields(request.POST)
        elif video_type_name == 'game_list':
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_game_list_type_fields(request.POST)
        elif video_type_name == "live_broadcast":
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_live_broadcast_type_fields(request.POST)
        elif video_type_name == 'game_gift':
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_game_gift_type_fields(request.POST)
        elif video_type_name == 'game_details':
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_game_download_type_fields(request.POST)
        elif video_type_name == 'user':
            if is_slider_box:
                video.s_image = request.POST.get('s_image', '')
            video.update_user_type_fields(request.POST)
        elif video_type_name == 'video_with_game_details':
            pass

        return HttpResponseRedirect(reverse('iphone_main_page_videos') + "?box_id=" + str(video.box_id))
    else:
        video_pk = int(request.GET.get('id'), 0)
        video = get_object_or_404(IphoneBoxVideo, pk=video_pk)
        box = get_object_or_none(HomeBox, pk=video.box_id)
        is_slider_box = (box.box_type == 2)#来自浏览器直接请求
        #delivery_is_slider_box = request.GET.get('is_slider_box')#重定向请求
        #is_slider_box = retrieve_is_slider_box or delivery_is_slider_box
        type_of_image = {}
        print "in update:==============",is_slider_box
        if is_slider_box:
            print "in if:-----------------"
            type_of_image = ADD_SLIDER_IMAGE
            type_of_image['image_url'] = video.s_image
        else:
            print "in else:-----------------"
            type_of_image = ADD_HORIZONTAL_IMAGE
            type_of_image['image_url'] = video.h_image

        video.pay_type_for_view = video.pay_type_for_view()
        video_type_name = VideoType.to_s(video.video_type)

        if video_type_name == "url":
            return render(request, 'iphone/main_page/video_manage/update_url_form_fields.html', {'video': video, 'is_slider_box':is_slider_box, 'type_of_image':type_of_image })
        elif video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist':
            return render(request, 'iphone/main_page/video_manage/update_video_form_fields.html', {'video': video, 'is_slider_box':is_slider_box, 'type_of_image':type_of_image})
        elif video_type_name == "game_list":
            return render(request, 'iphone/main_page/video_manage/update_game_list.html',
                          {
                              'video': video,
                              'is_slider_box':is_slider_box,
                              'type_of_image':type_of_image
                          })
        elif video_type_name == "game_details":
            game = IosGame.objects.get(id=video.game_id)
            is_slider_box = is_slider_box
            type_of_image = type_of_image
            return render(request, 'iphone/main_page/video_manage/update_item_game_details.html', locals())
        elif video_type_name == "game_gift":
            return render(request, 'iphone/main_page/video_manage/update_game_gift.html', {'video': video, 'is_slider_box':is_slider_box, 'type_of_image':type_of_image})
        elif video_type_name == "live_broadcast":
            live_broadcast_paid = live_broadcast_type_is_paid()
            return render(request, 'iphone/main_page/video_manage/update_live_broadcast_form_fields.html',
                          {
                            "video": video,
                            "live_broadcast_paid": live_broadcast_paid,
                            'is_slider_box':is_slider_box,
                            "type_of_image":type_of_image
                          })
        elif video_type_name == "user":
            return render(request, 'iphone/main_page/video_manage/update_user_form_fields.html', {'video': video, 'is_slider_box':is_slider_box, 'type_of_image':type_of_image})
        elif video_type_name == "video_with_game_details":
            game = IosGame.objects.get(id=video.game_id)
            return render(request, 'iphone/main_page/video_manage/update_video_with_game_details.html', locals())


@login_required
def update_video_status(request):
    print "------", request.POST, "------"
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            bv = IphoneBoxVideo.objects.get(id=int(pk))
            bv.state = int(request.POST.get("value"))
            bv.save()
            response = {'status': 'success'}
        else:
            video_ids = request.POST.get("video_ids")
            value = request.POST.get('value')
            if video_ids and value:
                IphoneBoxVideo.objects.extra(where=['id in (%s)' % video_ids]).update(state=int(value))
                response = {'status': 'success', 'video_ids': video_ids.split(',')}
            else:
                response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_video_value(request):
    """
    从视频列表页直接修改视频的title subtitle intro 属性
    注：页面上td的id属性不要改
    """
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")

        if video_id and value and attribute:
            try:
                video = IphoneBoxVideo.objects.get(pk=int(video_id))
                setattr(video, attribute, value)
                video.save()
                response = {'status': 'success', 'value': getattr(video, attribute)}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_video(request, id):
    video = IphoneBoxVideo.objects.get(pk=id)
    video.is_delete = 1
    video.save()
    box_id = video.box_id
    return HttpResponseRedirect(reverse('iphone_main_page_videos') + "?box_id=" + str(box_id))


@login_required
# according to different "video_type" to dispatch corresponding field
def add_video_fields(request):
    video_type = request.POST.get("video_type")
    type_of_image = {}
    is_slider_box = request.POST.get("is_slider_box")
    if is_slider_box == 'True':
        type_of_image = ADD_SLIDER_IMAGE
    elif is_slider_box == 'False':
        type_of_image = ADD_HORIZONTAL_IMAGE
    else:
        raise Exception('in iphone,views:add_video_fields is_slider_box value wrong')
    if (video_type == "video"):
        return render(request, "iphone/main_page/video_manage/add_video_form_fields.html", {"is_slider_box": is_slider_box})
    elif (video_type == "url"):
        return render(request, "iphone/main_page/video_manage/url_form_fields.html", {"is_slider_box": is_slider_box, 'type_of_image': type_of_image})
    elif video_type == "game_gift":
        return render(request, "iphone/main_page/video_manage/game_gift_form_fields.html", {"is_slider_box": is_slider_box, 'type_of_image': type_of_image})
    elif video_type == "game_list":
        return render(request, "iphone/main_page/video_manage/game_list_form_fields.html", {"is_slider_box": is_slider_box, 'type_of_image': type_of_image})
    elif video_type == "game_details":
        return render(request, "iphone/main_page/video_manage/game_details_form_fields.html", {"is_slider_box": is_slider_box, 'type_of_image': type_of_image})
    elif video_type == "live_broadcast":
        return render(request, "iphone/main_page/video_manage/live_broadcast_form_fields.html", {"is_slider_box": is_slider_box})
    elif video_type == "user":
        return render(request, "iphone/main_page/video_manage/user_form_fields.html", {"is_slider_box": is_slider_box})
    elif video_type == "video_with_game_details":
        return render(request, "iphone/main_page/video_manage/video_with_game_details.html", {"is_slider_box": is_slider_box})


def get_game_info(request):
    if request.method == 'GET':
        game_info = {}
        product = request.GET.get('product')
        if product == 'iPad':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
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
    game_type_list = []
    game_list = VideoType.name_to_dict("game_list")
    game_details = VideoType.name_to_dict("game_details")
    game_type_list.append(game_list)
    game_type_list.append(game_details)

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
    return render(request, "common_module/iphone_box.html")


def update_batch_videos(request):
    get_dict = request.GET.dict()

    param_str = handle_batch_items('IphoneBoxVideo', get_dict, request.POST.dict())
    return HttpResponseRedirect(reverse('iphone_main_page_videos') + param_str)
