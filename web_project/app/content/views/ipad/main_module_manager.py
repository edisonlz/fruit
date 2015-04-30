#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json

from app.content.models import HomeBox, HomeCommonBox, IpadHomeBoxTag, IpadChannel
from app.content.models import Platform, Status, BoxType,CidDetail
from app.content.lib.main_page_publish_tool import MainPagePublishTool
from app.content.lib.cache_plan import CachePlan
from django.db import transaction
from content.views.common import redefine_item_pos



@login_required
def modules(request):
    if request.method == 'POST':
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
        return HttpResponseRedirect(reverse('ipad_modules'))
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("ipad"))
        #TODO: add filter(module_type='modules') for box_type_list
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("ipad")
        datas = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('-position')
        return render(request, 'ipad/main_page/module_manage/module/modules.html',
                      {'modules': datas, 'box_type_list': box_type_list,
                       'box_type_hash': box_type_hash})


@login_required
def uniq_modules(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            try:
                redefine_item_pos(HomeBox, box_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("ipad"))
        #TODO: add filter(module_type='modules') for box_type_list
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("ipad")
        boxes = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('-position')
        common_boxes = HomeCommonBox.objects.filter(is_delete=False)
        cid_details = CidDetail.objects.filter(is_delete=False)
        for box in boxes:
            box.common_box_title = '未关联'
            for common_box in common_boxes:
                if common_box.id == box.attached_common_id:
                    box.common_box_title = common_box.title
        navigation_list = ["内容管理", "抽屉列表"]
        return render(request, 'ipad/main_page/module_manage/module/uniq_modules.html',
                      {'modules': boxes, 'box_type_list': box_type_list,
                       'cid_details':cid_details,
                       'box_type_hash': box_type_hash,
                       'module_state_hash': Status.STATUS_HASH,
                       'navigation_list': enumerate(navigation_list),
                       'common_boxes': common_boxes})


@login_required
def update_module_status(request):
    if request.method == 'POST':
        module_ids = request.POST.get("module_ids")
        value = request.POST.get("value")
        if module_ids and value:
            try:
                hbs = HomeBox.objects.extra(where=['id IN (%s)' % module_ids]).update(state=int(value))
                response = {'status': 'success', 'module_ids': module_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
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
def update_is_membership(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            hb = HomeBox.objects.get(id=int(pk))
            hb.for_membership = int(request.POST.get("value"))
            hb.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_module(request, module_id):
    home_box = HomeBox.objects.get(pk=module_id)
    home_box.is_delete = 1
    home_box.save()
    return HttpResponseRedirect(reverse('ipad_uniq_modules'))


@login_required
def query_module(request, box_id):
    module = get_object_or_404(HomeBox, pk=box_id)
    box_type_info = Platform.box_types(Platform.to_i("ipad"))
    box_type_hash = {item['id']: item['desc'] for item in box_type_info}
    box_type_list = box_type_hash.items()
    common_boxes = HomeCommonBox.objects.filter(is_delete=False)
    cid_details = CidDetail.objects.filter(is_delete=False)

    tag_type_hash = {item['id']: item['desc'] for item in module.tag_type_info()}
    tag_type_list = tag_type_hash.items()
    title_tag = IpadHomeBoxTag.objects.filter(is_delete=False, tag_type="title", box_id=box_id).first()
    normal_tags = IpadHomeBoxTag.objects.filter(is_delete=False, tag_type='normal', box_id=box_id)
    channels = IpadChannel.objects.filter(is_delete=False).exclude(cid=0).order_by('position')
    return render(request, 'ipad/main_page/module_manage/module/update_module.html',
                  {'module': module,
                   'cid_details':cid_details,
                   "box_type_list": box_type_list,
                   'box_type_hash': box_type_hash,
                   'common_boxes': common_boxes,
                   "tag_type_list": tag_type_list,
                   "tag_type_hash": tag_type_hash,
                   "title_tag": title_tag,
                   "normal_tags": normal_tags,
                   'channels': channels
                  })


@login_required
def add_module(request):
    if request.method == 'POST':
        platform_type = Platform.to_i("ipad")

        home_box = HomeBox()
        home_box.platform = int(platform_type)
        home_box.update_value(request.POST)
        while home_box.id in HomeBox.STATIC_BOX_ID.values():
            home_box.is_delete = True
            home_box = HomeBox()
            home_box.update_value(request.POST)
        home_box.create_default_title_tag()
        return HttpResponseRedirect(reverse('ipad_uniq_modules'))
    else:
        return render(request, 'ipad/main_page/module_manage/module/add_module.html')


@login_required
def update_module(request):
    box_id = request.POST.get("id")
    try:
        home_box = HomeBox.objects.get(id=box_id)
        home_box.update_value(request.POST)
        home_box.update_default_title_tag()
    except HomeBox.DoesNotExist, e:
        pass
    return HttpResponseRedirect(reverse('ipad_uniq_modules'))


@transaction.commit_on_success
def main_page_publish(request, ):
    if request.method == "POST":
        box_ids = request.POST.get("module_ids")
        box_ids = box_ids.split(',')
        result = MainPagePublishTool.boxes_publish(box_ids, platform="ipad")
        if result['status'] == 'error':
            response = result
            response['desc'] = '发布失败! ' + result['detail']

        elif result['status'] == 'publish_success':
            response = {'status': 'success'}
            try:
                for cache_key in ['ipad_home_page', 'ipad_home_page_3_2']:
                    CachePlan.clean_cache(key=cache_key, params=None)
            except:
                response = {'status': 'error', 'desc': '清缓存失败'}

        return HttpResponse(json.dumps(response), content_type="application/json")







