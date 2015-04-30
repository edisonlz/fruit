#coding=utf-8
import urllib, urllib2, json, logging
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
#from lib.util import DateUtil
from app.content.models import IpadBoxVideo, AndroidBoxVideo, HomeBox, \
    Platform, VideoType, Status,BoxType,BaseVideo
from django.conf import settings
from content.views.common import redefine_item_pos
from django.contrib import messages


@login_required
def videos(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        box_id = request.POST.get('box_id')
        if item_ids:
            try:
                redefine_item_pos(IpadBoxVideo, item_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        #TODO: active modules
        box_list = HomeBox.objects.filter(platform=Platform.to_i("ipad")).order_by('position')
        first_box_id = box_list.first() and box_list.first().id
        current_box_id = request.GET.get('box_id') or first_box_id
        current_box = HomeBox.objects.get(pk=int(current_box_id))
        videos = IpadBoxVideo.objects.filter(box_id=current_box.id, is_delete=0).order_by("-position")
        navigation_list = ['Ipad抽屉',current_box.title + '-视频列表']
        for index, video in enumerate(videos):
            videos[index].copyright_for_view = video.copyright_for_view()
            videos[index].pay_type_for_view = video.pay_type_for_view()
            videos[index].video_type_for_view = video.video_type_for_view()
        slider_tag = current_box.is_slider_box()
        return render(request, 'ipad/main_page/video_manage/videos.html',
                      {
                          'videos': videos,
                          'box_list': box_list,
                          'current_box_id': current_box_id,
                          'navigation_list': enumerate(navigation_list),
                          'video_state_hash':Status.STATUS_HASH,
                          'slider_tag': slider_tag
                      })


@login_required
#def add_video(request, box_id):
def add_video(request):
    if request.method == 'POST':
        video = IpadBoxVideo()

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
        elif video_type_name == 'video': #video/show/playlist
            video.add_video_type_fields(request.POST)
        elif video_type_name == 'live_broadcast':
            video.add_live_broadcast_type_fields(request.POST)

        box = HomeBox.objects.get(pk=video.box_id)
        if BaseVideo.get_exist_video_in_box(video_type_name,IpadBoxVideo,box,'box_id',video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
        video.save()
        # 去掉冗余视频
        if video.box_id:
            box = HomeBox.objects.get(pk=video.box_id)
            AndroidBoxVideo.remove_redundant_videos_in_box(box, HomeBox.MaxVideoCountInBox)

        return HttpResponseRedirect(reverse("ipad_update_video") + "?id=" + str(video.id))
        #return HttpResponseRedirect(reverse('update_video', args=(platform, )))
    else:
        video_type_list = IpadBoxVideo.video_types(mock=True)
        current_box_id = request.GET.get('box_id')
        current_box = HomeBox.objects.get(pk=int(current_box_id))
        return render(request, 'ipad/main_page/video_manage/add_video.html',
                      {
                          'video_type_list': video_type_list,
                          'current_box_id': current_box_id,
                          'current_box':current_box
                      })


@login_required
def query_video(request, id):
    video = get_object_or_404(IpadBoxVideo, pk=id)

    return HttpResponseRedirect(reverse('ipad_update_video') + "?id=" + str(video.id))


@login_required
def update_video(request):
    if request.method == 'POST':
        video = IpadBoxVideo.objects.filter(id=request.POST.get("id")).first()
        video_type_name = VideoType.to_s(video.video_type)
        if request.POST.get('s_image'):
            video.s_image = request.POST.get("s_image", '')
        if ( video_type_name == 'url'):
            video.update_url_type_fields(request.POST)
        elif(video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            video.update_video_type_fields(request.POST)
        elif (video_type_name == 'live_broadcast'):
            video.update_live_broadcast_type_fields(request.POST)

        return HttpResponseRedirect(reverse('ipad_main_page_videos') + "?box_id=" + str(video.box_id))
    else:
        video_pk = request.GET.get('id')
        video = get_object_or_404(IpadBoxVideo, pk=video_pk)
        #数据库中没有pay_type_for_view此字段(与后面调用的函数同名),是临时添加的属性
        video.pay_type_for_view = video.pay_type_for_view()
        video.video_type_for_view = video.video_type_for_view()
        video_type_name = VideoType.to_s(video.video_type)
        if video.box.box_type == BoxType.to_i('slider'):
            image_desc = "轮播图(596X400):"
            image_name = "s_image"
            image_url = video.s_image
        else:
            image_desc = '横图(448X252):'
            image_name = 'h_image'
            image_url = video.h_image
        args = {'video':video,'image_desc':image_desc,'image_name':image_name,'image_url':image_url}
        if (video_type_name == "url"):
            return render(request, 'ipad/main_page/video_manage/update_url_form_fields.html', args)
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            return render(request, 'ipad/main_page/video_manage/update_video_form_fields.html',args)
        elif (video_type_name == 'live_broadcast'):
            live_broadcast_paid = live_broadcast_type_is_paid()
            args['live_broadcast_paid'] = live_broadcast_paid
            return render(request, 'ipad/main_page/video_manage/update_live_broadcast_form_fields.html',args)


@login_required
def update_video_status(request):
    print "------", request.POST, "------"
    if request.method == 'POST':
        video_ids = request.POST.get("video_ids")
        value = request.POST.get('value')
        if video_ids and value:
            bv = IpadBoxVideo.objects.extra(where=['id in (%s)' % video_ids]).update(state=int(value))
            response = {'status': 'success','video_ids': video_ids.split(',')}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def update_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")

        if video_id and value and attribute:
            try:
                video = IpadBoxVideo.objects.get(pk=int(video_id))
                setattr(video,attribute,value)
                video.save()
                response = {'status': 'success', 'value': getattr(video,attribute)}
            except Exception, e:
                response = {'status': 'error', 'msg': u"更改视频属性失败!"}
        else:
            response = {'status': 'error', 'msg': u"属性不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")



@login_required
def delete_video(request, id):

    video = IpadBoxVideo.objects.get(pk=id)
    video.is_delete = 1
    video.save()
    box_id = video.box_id
    return HttpResponseRedirect(reverse('ipad_main_page_videos') + "?box_id=" + str(box_id))


@login_required
# according to different "video_type" to dispatch corresponding field
def add_video_fields(request):
    video_type = request.POST.get("video_type")
    box_id = request.POST.get('box_id',0)
    current_box = HomeBox.objects.filter(is_delete=False,id=int(box_id))
    slider_tag = 1 if current_box and current_box[0].box_type == BoxType.to_i('slider') else 0
    if slider_tag:
        image_name = 's_image'
        image_desc = '轮播图(596x400):'
    else:
        image_name = 'h_image'
        image_desc = '横图(448x252):'
    args = {'image_name':image_name,'image_desc':image_desc}
    if (video_type == "video"):
        return render(request, "ipad/main_page/video_manage/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "ipad/main_page/video_manage/url_form_fields.html",args)
    # elif video_type == "game_gift":
    #     return render(request, "ipad/main_page/video_manage/game_gift_form_fields.html")
    # elif video_type == "game_list":
    #     return render(request, "ipad/main_page/video_manage/game_list_form_fields.html")
    # elif video_type == "game_details":
    #     return render(request, "ipad/main_page/video_manage/game_details_form_fields.html")
    elif video_type == "live_broadcast":
         return render(request, "ipad/main_page/video_manage/live_broadcast_form_fields.html")
    # elif video_type == "user":
    #     return render(request, "ipad/main_page/video_manage/user_form_fields.html")


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
