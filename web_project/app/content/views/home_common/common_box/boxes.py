# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.content.models import HomeCommonBox, HomeCommonVideo, HomeBoxTag, AndroidHomeBoxTag, IphoneHomeBoxTag
from app.content.models import Platform, Status, BoxType, TagType, IpadChannel, HomeBox
from django.db.models import Max
from content.views.common import redefine_item_pos
from content.views.utils import get_paged_dict


def boxes(request, ):
    if request.method == 'POST':
        module_ids = request.POST.get('item_ids')
        if module_ids:
            try:
                redefine_item_pos(HomeCommonBox, module_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        # 测试session:
        # print "-----------------session:",request.session.__getitem__('name'), "-------------"
        box_type_info = Platform.box_types(Platform.to_i("android"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()

        boxes_list = HomeCommonBox.objects.filter(is_delete=False).order_by('-position')
        # paginator = Paginator(boxes_list,5)
        page = request.GET.get('page', 1)
        page_context = get_paged_dict(boxes_list, page)
        # try:
        #     boxes = paginator.page(page)
        # except PageNotAnInteger:
        #     boxes = paginator.page(1)

        context = {'boxes': boxes,
                   'box_type_list': box_type_list,
                   'box_type_hash': box_type_hash,
                   'box_state_hash': Status.STATUS_HASH,
                   'current_box_page': page,
                   }
        context.update(page_context)
        return render(request, 'home_common/common_box/boxes.html', context)


def add_box(request):
    if request.method == 'POST':
        platform_type = Platform.to_i("android")
        title = request.POST.get('title', '')
        box = HomeCommonBox()
        box.platform = int(platform_type)
        box.title = title
        max_position = HomeCommonBox.objects.filter(platform=box.platform).aggregate(Max('position'))[
                           'position__max'] or 0
        box.position = max_position + 1
        box.save()
        return HttpResponseRedirect(reverse('home_common_boxes'))
    else:
        return render(request, 'home_common/common_box/add_box.html')


# TODO: move videos_in_box to video-manage-page
def videos_in_box(request, current_box_page, box_pk):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(HomeCommonVideo, item_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        from_box_page = current_box_page
        videos = HomeCommonVideo.objects.filter(box_id=int(box_pk), is_delete=False).order_by('-position')
        box = HomeCommonBox.objects.get(id=int(box_pk))
        override_boxes = HomeBox.objects.filter(attached_common_id=box_pk,is_delete=False).order_by('platform')
        # override_platform = HomeBox.objects.filter(attached_common_id=box_pk).
        # override_box = ', '.join([Platform.to_s(x['platform']) for x in override_platform])
        return render(request, 'home_common/common_video/videos.html',
                      {
                          "videos": videos,
                          "box": box,
                          'box_state_hash': Status.STATUS_HASH,
                          "from_box_page": from_box_page,
                          "override_boxes": override_boxes,
                          # "navigation_list": enumerate(navigation_list)
                      })


@login_required
def update_box(request, box_pk):
    if request.method == 'POST':
        box_type = request.POST.get('box_type', 1)
        title = request.POST.get('title', '')
        video_count_for_pad = request.POST.get('video_count_for_pad', 4)
        video_count_for_phone = request.POST.get('video_count_for_phone', 4)
        cid = request.POST.get('cid')
        image = request.POST.get('normal_img', '')
        image_link = request.POST.get('image_link', '')
        try:
            box = HomeCommonBox.objects.get(id=box_pk)
            box.box_type = int(box_type)
            box.image = image
            box.title = title
            box.image_link = image_link
            box.video_count_for_pad = int(video_count_for_pad)
            box.video_count_for_phone = int(video_count_for_phone)
            box.position = 0
            box.cid = cid
            # box.state = Status.StatusOpen
            box.is_youku_channel = 1
            box.save()
        except HomeCommonBox.DoesNotExist, e:
            pass
        return HttpResponseRedirect(reverse('home_common_boxes'))
    else:
        box = HomeCommonBox.objects.get(id=int(box_pk))
        box_type_info = Platform.box_types(Platform.to_i("android"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        return render(request, 'home_common/common_box/update_box.html', {"box": box, "box_type_hash": box_type_hash})


@login_required
def delete_box(request, box_pk):
    box = HomeCommonBox.objects.get(pk=box_pk)
    box.is_delete = 1
    box.save()
    return HttpResponseRedirect(reverse('home_common_boxes'))


def box_sync(request, module_id):
    pass


# def update_status(request):
#     if request.method == 'POST':
#         pk = request.POST.get("pk")
#         if pk:
#             hb = HomeCommonBox.objects.get(id=int(pk))
#             hb.state = int(request.POST.get("value"))
#             hb.save()
#
#             response = {'status': 'success'}
#         else:
#             response = {'status': 'error', 'msg': u"模块不存在!"}
#     else:
#         response = {'status': 'error', 'msg': u"仅支持POST!"}
#
#     return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_status(request):
    if request.method == 'POST':
        module_ids = request.POST.get("module_ids")

        value = request.POST.get("value")
        if module_ids and value:
            try:
                hbs = HomeCommonBox.objects.extra(where=['id IN (%s)' % module_ids]).update(state=int(value))
                response = {'status': 'success', 'module_ids': module_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_box_title(request):
    if request.method == 'POST':
        box_id = request.POST.get("box_id")
        title = request.POST.get("value")
        if box_id and title:
            try:
                hb = HomeCommonBox.objects.get(pk=int(box_id))
                hb.title = title
                hb.save()
                response = {'status': 'success', 'title': hb.title}
            except Exception, e:
                response = {'status': 'error', 'msg': u"修改抽屉标题失败!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_is_youku_channel(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hb = HomeCommonBox.objects.get(id=int(pk))
            hb.is_youku_channel = int(request.POST.get("value"))
            hb.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_is_multiply_units(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hb = HomeCommonBox.objects.get(id=int(pk))
            hb.is_phone_use_multiply_units = int(request.POST.get("value"))
            hb.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
@login_required
# def query_module(request, box_id):
#     module = get_object_or_404(HomeCommonBox, pk=box_id)
#     box_type_info = Platform.box_types(Platform.to_i("android"))
#     box_type_hash = {item['id']: item['desc'] for item in box_type_info}
#     box_type_list = box_type_hash.items()
#     tag_type_info = AndroidHomeBoxTag.tag_types()
#     title_tag = AndroidHomeBoxTag.objects.filter(is_delete=False,tag_type="title",box_id=box_id).first()
#     normal_tags = AndroidHomeBoxTag.objects.filter(is_delete=False,tag_type='normal',box_id=box_id)
#     tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
#     tag_type_list = tag_type_hash.items()
#     channels = AndroidChannel.objects.filter(is_delete=False).order_by('position')
#     return render(request, 'android/main_page/module_manage/module/update_module.html',
#                   {'module': module,
#                    "box_type_list": box_type_list,
#                    "tag_type_list": tag_type_list,
#                    "tag_type_hash": tag_type_hash,
#                    "title_tag":title_tag,
#                    "normal_tags":normal_tags,
#                    "channels":channels,
#                    })


def home_common_videos(request, ):
    pass


    