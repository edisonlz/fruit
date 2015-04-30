#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json

from app.content.models import HomeBox,HomeBoxTag,AndroidHomeBoxTag,IphoneHomeBoxTag
from app.content.models import Platform, Status, BoxType, TagType, IpadChannel


@login_required
def new_modules(request, platform="all"):
    if request.method == 'POST':

        print("in post new modules" + reverse('modules', args=(platform,)))
        module_ids = request.POST.get('module_ids')
        if module_ids:
            module_ids = module_ids.split(',')
        else:
            module_ids = []
        module_ids.reverse()
        position = 1
        for module_id in module_ids:
            module = HomeBox.objects.get(id=module_id)
            module.position = position
            position += 1
            module.save()
        return HttpResponseRedirect(reverse('modules', args=(platform,)))
    else:
        #Get Comes here
        print("current platform :" + platform)
        box_type_info = Platform.box_types(Platform.to_i(platform))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i(platform)
        datas = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('position')
        return render(request, 'new/module/modules.html',
                      {'modules': datas, 'module_platform': platform, 'box_type_list': box_type_list,
                       'box_type_hash': box_type_hash})


@login_required
def update_new_module_status(request, platform="all"):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hb = HomeBox.objects.get(id=int(pk))
            hb.state = int(request.POST.get("value"))
            hb.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_is_youku_channel(request, platform="all"):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hb = HomeBox.objects.get(id=int(pk))
            hb.is_youku_channel = int(request.POST.get("value"))
            hb.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_new_module(request, platform, module_id):
    home_box = HomeBox.objects.get(pk=module_id)
    home_box.is_delete = 1
    home_box.save()
    return HttpResponseRedirect(reverse('modules', args=(platform,)))


@login_required
def query_new_module(request, platform, box_id):
    module = get_object_or_404(HomeBox, pk=box_id)
    box_type_info = Platform.box_types(Platform.to_i(platform))
    box_type_hash = {item['id']: item['desc'] for item in box_type_info}
    box_type_list = box_type_hash.items()
    if platform == 'ipad':
        return render(request, 'new/module/update_module.html',
                      {'module': module, 'module_platform': platform,
                       "box_type_list": box_type_list,
                       })
    else:
        if platform == 'iphone':
            title_tag = IphoneHomeBoxTag.objects.filter(is_delete=False,tag_type="title",box_id=box_id).first()
            normal_tags = IphoneHomeBoxTag.objects.filter(is_delete=False,tag_type='normal',box_id=box_id)
            tag_type_info = IphoneHomeBoxTag.tag_types()
        elif platform == 'android':
            tag_type_info = AndroidHomeBoxTag.tag_types()
            title_tag = AndroidHomeBoxTag.objects.filter(is_delete=False,tag_type="title",box_id=box_id).first()
            normal_tags = AndroidHomeBoxTag.objects.filter(is_delete=False,tag_type='normal',box_id=box_id)
        tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
        tag_type_list = tag_type_hash.items()
        platform_data = Platform.to_i('ipad')
        channels = IpadChannel.objects.filter(platform=platform_data).order_by('position')
        return render(request, 'new/module/update_module.html',
                      {'module': module, 'module_platform': platform,
                       "box_type_list": box_type_list,
                       "tag_type_list": tag_type_list,
                       "tag_type_hash": tag_type_hash,
                       "title_tag":title_tag,
                       "normal_tags":normal_tags,
                       "channels":channels,
                       })




@login_required
def add_new_module(request, platform="all"):
    if request.method == 'POST':
        box_id = request.POST.get("box_id", 0)
        platform_type = Platform.to_i(platform)
        box_type = request.POST.get("box_type", 1)
        title = request.POST.get('title', '')
        video_count_for_pad = request.POST.get('video_count_for_pad', 4)
        video_count_for_phone = request.POST.get('video_count_for_phone', 4)
        cid = request.POST.get('cid')
        image = request.POST.get('normal_img', '')
        image_link = request.POST.get('image_link', '')
        if platform == "ipad":
            membership_tag = request.POST.get('membership', 0)
        if platform == "android":
            use_multiply_units_tag = request.POST.get('use_multiply_units', 0)
        home_box = HomeBox()
        home_box.box_id = int(box_id)
        home_box.platform = int(platform_type)
        home_box.image = image
        home_box.title = title
        home_box.image_link = image_link
        home_box.video_count_for_pad = int(video_count_for_pad)
        home_box.video_count_for_phone = int(video_count_for_phone)
        home_box.box_type = int(box_type)
        home_box.position = 0
        home_box.cid = cid
        home_box.state = Status.StatusOpen
        home_box.is_youku_channel = 1
        if platform == "ipad":
            home_box.for_membership = membership_tag
        if platform == "android":
            home_box.is_phone_use_multiply_units = use_multiply_units_tag
        # home_box.box_type = HomeModule.Module_Box
        home_box.save()

        if platform == "android":
            default_title_tag = AndroidHomeBoxTag()
            default_title_tag.box_id = home_box.id  #todo 重复代码提取
            default_title_tag.tag_type = "title"
            default_title_tag.title = home_box.title
            default_title_tag.jump_type = 1
            default_title_tag.save()
        elif platform == "iphone":
            default_title_tag = IphoneHomeBoxTag()
            default_title_tag.box_id = home_box.id
            default_title_tag.tag_type = "title"
            default_title_tag.title = home_box.title
            default_title_tag.jump_type = 1
            default_title_tag.save()
        return HttpResponseRedirect(reverse('modules', args=(platform,)))
    else:
        return render(request, '/new/module/add_module.html')


@login_required
def update_new_module(request, platform="all"):
    if request.method == 'POST':
        id = request.POST.get("id")
        box_id = request.POST.get("box_id", 0)
        box_type = request.POST.get('box_type', 1)
        title = request.POST.get('title', '')
        video_count_for_pad = request.POST.get('video_count_for_pad', 4)
        video_count_for_phone = request.POST.get('video_count_for_phone', 4)
        cid = request.POST.get('cid')
        image = request.POST.get('normal_img', '')
        image_link = request.POST.get('image_link', '')
        if platform == "ipad":
            membership_tag = request.POST.get('membership', 0)
        if platform == "android":
            use_multiply_units_tag = request.POST.get('use_multiply_units', 0)
        try:
            home_box = HomeBox.objects.get(id=id)
            home_box.box_id = int(box_id)
            home_box.box_type = int(box_type)
            home_box.image = image
            home_box.title = title
            home_box.image_link = image_link
            home_box.video_count_for_pad = int(video_count_for_pad)
            home_box.video_count_for_phone = int(video_count_for_phone)
            home_box.position = 0
            home_box.cid = cid
            home_box.state = Status.StatusOpen
            home_box.is_youku_channel = 1
            if platform == "ipad":
                home_box.for_membership = membership_tag
            if platform == "android":
                home_box.is_phone_use_multiply_units = use_multiply_units_tag
            home_box.save()
        except HomeBox.DoesNotExist, e:
            pass
        return HttpResponseRedirect(reverse('modules', args=(platform,)))
    else:
        return render(request, 'new/module/update_module.html', {'module_type_hash': HomeBox.MODULETYPE})







