# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from app.content.views.common import redefine_item_pos, set_position
from app.content.models import Status
from app.content.models import AndroidChannel, IphoneChannel, IpadChannel
from app.content.models import AndroidSubChannel, IphoneSubChannel, IpadSubChannel
from app.content.models import BrandModule, BrandVideo, AndroidGame, HomeBox, BaseVideo
from app.content.models import VideoType
from django.contrib import messages
import json
from wi_model_util.imodel import get_object_or_none

def videos(request,):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        print "item_ids", item_ids
        if item_ids:
            try:
                redefine_item_pos(BrandVideo, item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        module_pk = int(request.GET.get('module_id', 0))
        module = get_object_or_none(BrandModule, pk=module_pk)
        videos = BrandVideo.objects.filter(is_delete=0, brand_module_id=module_pk).order_by('-position')
        return render(request, "brand/videos/videos.html",
                  {
                      "module_id": module_pk,
                      "videos": videos,
                      "module": module
                  })


def add_video(request,):

    if request.method == 'POST':
        video = BrandVideo()
        module_pk = int(request.GET.get('module_id', 0))
        video.brand_module_id = module_pk
        video.add_position(module_pk)
        box = BrandModule.objects.get(pk=video.brand_module_id)

        #对于video类型的视频此处只是临时保存video_type,下一步将通过url来获取video_type
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = VideoType.to_s(video.video_type)
        if video_type_name == 'video':  #video/show/playlist
            video.add_video_type_fields(request.POST)
            if BaseVideo.get_exist_video_in_box(video_type_name,BrandVideo,box,'brand_module_id',video):
                messages.error(request, '视频已经存在')
                return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
            video.save()
            return render(request, "brand/videos/update_video_form_fields.html",
                          {"video":video, "module_id":module_pk})
        elif video_type_name == 'url':
            video.add_url_type_fields(request.POST)
            if BaseVideo.get_exist_video_in_box(video_type_name,BrandVideo,box,'brand_module_id',video):
                messages.error(request, '视频已经存在')
                return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
            video.save()
            return render(request, "brand/videos/update_url_form_fields.html",
                          {"video":video, "module_id":module_pk})
        elif video_type_name == "user":
            video.add_user_type_fields(request.POST)
            if BaseVideo.get_exist_video_in_box(video_type_name,BrandVideo,box,'brand_module_id',video):
                messages.error(request, '视频已经存在')
                return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
            video.save()
            return render(request, "brand/videos/update_user_form_fields.html",
                          {"video":video, "module_id":module_pk })
        elif video_type_name in ['game_list','game_download','game_details']:
            video.add_game_download_type_fields(request.POST)
            if BaseVideo.get_exist_video_in_box(video_type_name,BrandVideo,box,'brand_module_id',video):
                messages.error(request, '视频已经存在')
                return HttpResponseRedirect( request.META.get('HTTP_REFERER') )
            video.save()
            return HttpResponseRedirect(reverse('brand_videos')+"?module_id="+str(module_pk))

    else:
        video_type_list = BrandVideo.video_types()
        return render(request, 'brand/videos/add_video.html',
                      {
                          'video_type_list': video_type_list,
                          'module_id': request.GET.get('module_id', 0)
                      })

def update_video(request, video_pk):

    if request.method == "POST":
        module_pk = int(request.GET.get('module_id', 0))
        video = get_object_or_404(BrandVideo, pk=int(video_pk))
        brand_module_id = request.GET.get("brand_module_id", 0)

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
        elif video_type_name == 'user':
            video.update_video_type_fields(request.POST)
        elif video_type_name in ('game_list','game_details', 'game_download'):
            video.update_game_download_type_fields(request.POST)

        return HttpResponseRedirect(reverse('brand_videos')+"?module_id="+str(module_pk))
    else:
        video = get_object_or_404(BrandVideo, pk=int(video_pk))
        module_pk = request.GET.get("module_id", 0)

        video_type_name = VideoType.to_s(video.video_type)
        if video_type_name == 'video':  #video/show/playlist
            return render(request, "brand/videos/update_video_form_fields.html",
                          {"video":video, "module_id":module_pk })
        elif video_type_name == 'url':
            return render(request, "brand/videos/update_url_form_fields.html",
                          {"video":video, "module_id":module_pk })
        elif video_type_name == "user":
            return render(request, "brand/videos/update_user_form_fields.html",
                          {"video":video, "module_id":module_pk })
        elif video_type_name in ['game_list','game_download','game_details']:
            game = AndroidGame.objects.get(id=video.game_id)
            return render(request, "brand/videos/update_game_details.html",
                          {"video":video, "module_id":module_pk, "game":game})


def delete_video(request, video_pk):
    video = get_object_or_404(BrandVideo, pk=int(video_pk))
    module_id = request.GET.get("module_id")
    video.is_delete = 1
    video.save()
    return HttpResponseRedirect(reverse('brand_videos')+"?module_id="+module_id)


def update_status(request, ):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        video = get_object_or_404(BrandVideo, pk=post_dict.pop('pk'))
        if hasattr(video, post_dict.get('name')):
            setattr(video, post_dict.get('name'), post_dict.get('value', 0))
            video.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


# according to different "video_type" to dispatch corresponding field
@login_required
def add_fields(request):
    video_type = request.POST.get("video_type")
    print "video_type---------------:",video_type
    if (video_type == "video"):
        return render(request, "brand/videos/add_video_form_fields.html")
    elif (video_type == "url"):
        return render(request, "brand/videos/url_form_fields.html")
    elif video_type == "game_list":
        return render(request, "brand/videos/game_details_form_fields.html")
    elif video_type == "game_details":
        return render(request, "brand/videos/game_details_form_fields.html")
    elif video_type == "game_download":
        return render(request, "brand/videos/game_details_form_fields.html")
    elif video_type == "user":
        return render(request, "brand/videos/user_form_fields.html")

