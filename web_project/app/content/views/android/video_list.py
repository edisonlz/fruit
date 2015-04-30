# coding=utf-8
import json
from django.contrib import messages
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Max
from app.content.models import AndroidVideoListModule, AndroidVideoListVideo, VideoType, Status, BaseVideo
from app.content.views.common import redefine_item_pos


@login_required()
def video_lists(request):
    if request.method == 'POST':
        video_list_ids = request.POST.get('item_ids')
        if video_list_ids:
            try:
                redefine_item_pos(AndroidVideoListModule, video_list_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif request.method == 'GET':
        video_lists = AndroidVideoListModule.objects.filter(is_delete=False).order_by('-position')
        return render(request, 'android/main_page/module_manage/module/video_lists.html', locals())


@login_required()
def add_video_list(request):
    title = request.POST.get('title')
    AndroidVideoListModule.objects.create(title=title)
    return HttpResponseRedirect(reverse('android_video_lists'))


@login_required()
def query_video_list(request, list_id):
    video_list = AndroidVideoListModule.objects.get(id=list_id)
    return render(request, 'android/main_page/module_manage/module/video_list.html', locals())


@login_required()
def update_video_list(request):
    if request.method == 'POST':
        video_list = AndroidVideoListModule.objects.get(pk=request.POST.get('id'))
        video_list.title = request.POST.get('title')
        video_list.save()

        return HttpResponseRedirect(reverse('android_video_lists'))


@login_required()
def update_status_video_list(request):
    if request.method == 'POST':
        pk = request.POST.get('pk')
        AndroidVideoListModule.objects.filter(pk=pk).update(
            state=(AndroidVideoListModule.objects.get(pk=pk).state ^ 1))
        response = {'status': 'success'}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required()
def delete_video_list(request, list_id):
    AndroidVideoListModule.objects.filter(id=list_id).update(is_delete=True)
    return HttpResponseRedirect(reverse('android_video_lists'))


@login_required()
def videos_in_vl(request, list_id):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(AndroidVideoListVideo, item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")

    elif request.method == 'GET':
        video_list = AndroidVideoListModule.objects.get(pk=list_id)
        videos = video_list.androidvideolistvideo_set.filter(is_delete=False).order_by('-position')
        state_hash = Status.STATUS_HASH
        return render(request, 'android/main_page/module_manage/module/videos_in_vl.html', locals())


@login_required()
def video_list_add_video(request, list_id):
    if request.method == 'GET':
        video_type_list = AndroidVideoListVideo.video_types(mock=True)
        video_list = AndroidVideoListModule.objects.get(pk=list_id)
        return render(request, 'android/main_page/module_manage/module/video_list_add_video.html', locals())
    elif request.method == 'POST':
        video = AndroidVideoListVideo()
        video_type_name = request.POST.get('video_type')
        video_list = AndroidVideoListModule.objects.get(pk=list_id)
        max_position = AndroidVideoListVideo.objects.aggregate(Max('position'))['position__max'] or 0
        video.position = max_position + 1
        if video_type_name == 'video':
            video.module_id = list_id
            video.add_video_type_fields(request.POST)
        elif video_type_name == 'url':
            video.video_type = VideoType.to_i(video_type_name)
            video.module_id = list_id
            video.add_url_type_fields(request.POST)
        else:
            messages.error(request, 'invalid video type')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        if BaseVideo.get_exist_video_in_box(video_type_name, AndroidVideoListVideo, video_list, 'module_id', video):
            messages.error(request, '视频已经存在')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        video.save()
        return HttpResponseRedirect(reverse('video_list_query_video', args=(list_id, video.id)))


@login_required()
def video_list_query_video(request, list_id, video_id):
    video = AndroidVideoListVideo.objects.get(pk=video_id)
    video.pay_type_for_view = video.pay_type_for_view()
    video_type_name = VideoType.to_s(video.video_type)
    if (video_type_name == "url"):
        return render(request, 'android/main_page/module_manage/module/video_list_query_video.html',
                      {'video': video})
    elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
        return render(request, 'android/main_page/module_manage/module/video_list_query_video.html',
                      {'video': video})

    return render(request, 'android/main_page/module_manage/module/video_list_query_video.html', locals())


@login_required()
def video_list_update_video(request, list_id, video_id):
    video = AndroidVideoListVideo.objects.get(pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    if ( video_type_name == 'url'):
        video.update_url_type_fields(request.POST)
    elif (video_type_name == 'video' or video_type_name == 'show' or video_type_name == 'playlist' ):
        video.update_video_type_fields(request.POST)
    return HttpResponseRedirect(reverse('videos_in_vl', args=(list_id,)))


@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def video_list_update_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")

        if video_id and value and attribute:
            try:
                video = AndroidVideoListVideo.objects.get(pk=int(video_id))
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


@login_required()
def video_list_update_video_status(request):
    video_ids = request.POST.get("video_ids").split(',')
    value = request.POST.get("value")
    AndroidVideoListVideo.objects.filter(id__in=video_ids).update(state=value)
    response = {'status': 'success', 'video_ids': video_ids}
    return HttpResponse(json.dumps(response), content_type='application/json')


@login_required()
def video_list_delete_video(request, list_id, video_id):
    AndroidVideoListVideo.objects.filter(pk=video_id).update(is_delete=True)
    return HttpResponseRedirect(reverse('videos_in_vl', args=(list_id,)))