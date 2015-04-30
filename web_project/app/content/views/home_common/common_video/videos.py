#coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import HomeCommonBox, HomeCommonVideo, HomeBoxTag, AndroidHomeBoxTag, IphoneHomeBoxTag
from app.content.models import Platform, Status, BoxType, TagType, IpadChannel, VideoType, BaseVideo
import logging


def add_video(request, from_box_page, box_pk):
    if request.method == 'POST':

        video = HomeCommonVideo()
        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        current_box_id = request.POST.get("box_id")
        if current_box_id:
            video.box_id = int(current_box_id)
            box = HomeCommonBox.objects.get(pk=video.box_id)
        else:
            raise Exception('No parent box')
        video.add_position(box_pk)

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        elif video_type_name == 'video':  #video/show/playlist
            video.add_video_type_fields(request.POST)
        elif video_type_name == 'live_broadcast':
            video.add_live_broadcast_type_fields(request.POST)
        if BaseVideo.get_exist_video_in_box(video_type_name,HomeCommonVideo,box,'box_id',video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
        video.save()

        video.save()
        # 去掉冗余视频
        if video.box_id:
            box = HomeCommonBox.objects.get(pk=video.box_id)
            HomeCommonVideo.remove_redundant_videos_in_box(box, HomeCommonBox.MaxVideoCountInBox)

        return HttpResponseRedirect(reverse("home_common_videos_update_video", args=(from_box_page, box_pk, video.id,)))
        #return HttpResponseRedirect(reverse('update_video', args=(platform, )))
    else:
        video_type_list = HomeCommonVideo.video_types(mock=True)
        current_box_id = int(box_pk)
        return render(request, 'home_common/common_video/add_video.html',
                      {
                          'video_type_list': video_type_list,
                          'current_box_id': current_box_id,
                          'from_box_page': from_box_page,
                      })


def add_video_fields(request):
    video_type = request.POST.get("video_type")
    if (video_type == "video"):
        return render(request, "home_common/common_video/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "home_common/common_video/add_url_form_fields.html")
    elif video_type == "live_broadcast":
         return render(request, "home_common/common_video/add_live_broadcast_form_fields.html")

@login_required
def update_video(request, from_box_page, box_pk, video_pk):
    if request.method == 'POST':
        #if request.POST.get("video_type") == 'video':

        video = HomeCommonVideo.objects.get(id=int(video_pk))

        video_type_name = VideoType.to_s(video.video_type)

        if ( video_type_name == 'url'):
            video.update_url_type_fields(request.POST)
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            video.update_video_type_fields(request.POST)
        elif (video_type_name == 'live_broadcast'):
            video.update_live_broadcast_type_fields(request.POST)

        return HttpResponseRedirect(reverse('home_common_boxes_videos_in_box', args=(from_box_page, box_pk, )))
    else:
        video = get_object_or_404(HomeCommonVideo, pk=int(video_pk))
        #数据库中没有pay_type_for_view此字段(与后面调用的函数同名),是临时添加的属性
        video.pay_type_for_view = video.pay_type_for_view()
        video_type_name = VideoType.to_s(video.video_type)
        #video = HomeCommonVideo.objects.get(id=int(request.GET.get("id")))

        if (video_type_name == "url"):
            return render(request, 'home_common/common_video/update_url_form_fields.html',
                          {'video': video, "from_box_page": from_box_page})
        elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
            return render(request, 'home_common/common_video/update_video_form_fields.html',
                          {'video': video, "from_box_page": from_box_page})
        elif (video_type_name == 'live_broadcast'):
            live_broadcast_paid = live_broadcast_type_is_paid()
            return render(request, 'home_common/common_video/update_live_broadcast_form_fields.html',
                          {'video': video, "from_box_page": from_box_page,"live_broadcast_paid":live_broadcast_paid})


@login_required
def delete_video(request, from_box_page, box_pk, video_pk):
    video = HomeCommonVideo.objects.get(pk=int(video_pk))
    video.is_delete = 1
    video.save()
    return HttpResponseRedirect(reverse('home_common_boxes_videos_in_box', args=(from_box_page, int(box_pk), )))


@login_required
def update_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")

        if video_id and value and attribute:
            try:
                video = HomeCommonVideo.objects.get(pk=int(video_id))
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
def update_status(request):
    if request.method == 'POST':
        module_ids = request.POST.get("module_ids")

        value = request.POST.get("value")
        if module_ids and value:
            try:
                hbs = HomeCommonVideo.objects.extra(where=['id IN (%s)' % module_ids]).update(state=int(value))
                response = {'status': 'success', 'module_ids': module_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


def sync_box_videos(request, ):
    if request.method == 'POST':
        video_ids = request.POST.get("video_ids")
        print "******************"
        if video_ids:
            video_ids = video_ids.split(',')
            current_box_id = request.POST.get("current_box_id")
            current_box = HomeCommonBox.objects.get(pk=current_box_id)
            try:
                current_box.sync_box_videos(video_ids)
                response = {'status': 'success'}
            except Exception, e:
                logging.error(e)
                response = {'status': 'failed', 'message': e.message}
        else:
            response = {'status': 'failed', 'message': '请先选择同步视频。'}
        return HttpResponse(json.dumps(response))
    else:
        pass


def live_broadcast_type_is_paid():
    cost = {"id": 1, "desc": "付费"}
    free = {"id": 0, "desc": "免费"}
    live_broadcast_paid = []
    live_broadcast_paid.append(cost)
    live_broadcast_paid.append(free)

    return live_broadcast_paid


