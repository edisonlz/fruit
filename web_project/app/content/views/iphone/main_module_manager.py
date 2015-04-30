# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import HomeBox, HomeBoxTag, IphoneHomeBoxTag, HomeCommonBox, CidDetail
from app.content.models import Platform, Status, BoxType, TagType, IphoneChannel
from app.content.lib.main_page_publish_tool import MainPagePublishTool
from django.db import transaction
from app.content.lib.cache_plan import CachePlan
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
        return HttpResponseRedirect(reverse('iphone_modules'))
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("iphone"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("iphone")
        datas = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('-position')
        return render(request, 'iphone/main_page/module_manage/module/modules.html',
                      {'modules': datas, 'box_type_list': box_type_list,
                       'box_type_hash': box_type_hash})


@login_required
def uniq_modules(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        print box_ids, 'box_ids'
        if box_ids:
            try:
                redefine_item_pos(HomeBox, box_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("iphone"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("iphone")
        common_boxes = HomeCommonBox.objects.filter(is_delete=False)
        cid_details = CidDetail.objects.filter(is_delete=False)
        boxes = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('-position')
        for box in boxes:
            box.common_box_title = '未关联'
            for common_box in common_boxes:
                if common_box.id == box.attached_common_id:
                    box.common_box_title = common_box.title
        navigation_list = ["内容管理", "抽屉列表"]
        return render(request, 'iphone/main_page/module_manage/module/uniq_modules.html', {
            'modules': boxes, 'box_type_list': box_type_list,
            'cid_details': cid_details,
            'box_type_hash': box_type_hash,
            'module_state_hash': Status.STATUS_HASH,
            'common_boxes': common_boxes,
            'navigation_list': enumerate(navigation_list)
        })


@login_required
def update_module_status(request):
    if request.method == 'POST':
        module_ids = request.POST.get("module_ids")
        value = request.POST.get("value")
        if module_ids and value:
            try:
                #TODO: modify the below sql with filter(id__in=module_id_list)
                hbs = HomeBox.objects.extra(where=['id IN (%s)' % module_ids]).update(state=int(value))
                response = {'status': 'success', 'module_ids': module_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
        elif request.POST.get('name'):
            try:
                HomeBox.objects.filter(id=request.POST.get('pk')).update(state=request.POST.get('value'))
                response = {'status': 'success'}
            except HomeBox.DoesNotExist:
                pass
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
def delete_module(request, module_id):
    home_box = HomeBox.objects.get(pk=module_id)
    home_box.is_delete = 1
    home_box.save()
    return HttpResponseRedirect(reverse('iphone_uniq_modules'))


@login_required
def query_module(request, box_id):
    module = get_object_or_404(HomeBox, pk=box_id)
    box_type_info = Platform.box_types(Platform.to_i("iphone"))
    box_type_hash = {item['id']: item['desc'] for item in box_type_info}
    tag_type_info = module.tag_type_info()
    title_tag = IphoneHomeBoxTag.objects.filter(is_delete=False, tag_type="title", box_id=box_id).first()
    normal_tags = IphoneHomeBoxTag.objects.filter(is_delete=False, tag_type='normal', box_id=box_id)
    tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
    tag_type_list = tag_type_hash.items()
    common_boxes = HomeCommonBox.objects.filter(is_delete=False)
    cid_details = CidDetail.objects.filter(is_delete=False)
    channels = IphoneChannel.objects.filter(is_delete=False).exclude(cid=0).order_by('position')
    return render(request, 'iphone/main_page/module_manage/module/update_module.html',
                  {'module': module,
                   'cid_details': cid_details,
                   "box_type_hash": box_type_hash,
                   "tag_type_list": tag_type_list,
                   "tag_type_hash": tag_type_hash,
                   "title_tag": title_tag,
                   "normal_tags": normal_tags,
                   "channels": channels,
                   "common_boxes": common_boxes
                  })


@login_required
def add_module(request):
    if request.method == 'POST':
        platform_type = Platform.to_i("iphone")
        home_box = HomeBox()
        home_box.platform = int(platform_type)
        home_box.update_value(request.POST)
        while home_box.id in HomeBox.STATIC_BOX_ID.values():
            home_box.is_delete = True
            home_box = HomeBox()
            home_box.update_value(request.POST)
        home_box.create_default_title_tag()
        return HttpResponseRedirect(reverse('iphone_uniq_modules'))
    else:
        return render(request, 'iphone/main_page/module_manage/module/add_module.html')


@login_required
def update_module(request):
    module_id = request.POST.get("id")
    try:
        home_box = HomeBox.objects.get(id=module_id)
        home_box.update_value(request.POST)
        home_box.update_default_title_tag()
        home_box.save()
    except HomeBox.DoesNotExist, e:
        pass
    return HttpResponseRedirect(reverse('iphone_uniq_modules'))


def get_module_tag_titles(request):
    '''
    获取已有tag标题，用于页面tag标题总字数验证
    若当前tag类型为title 返回空
    若当前tag类型为 normal 返回除当前tag外当前抽屉其余normal类型tag标题
    '''
    module_id = int(request.GET.get("box_id"))
    tag_id = int(request.GET.get("tag_id", 0))
    current_tag = IphoneHomeBoxTag.objects.filter(id=tag_id, is_delete=False)
    if current_tag and current_tag[0].tag_type == 'title':
        result = {}
    else:
        tags = IphoneHomeBoxTag.objects.filter(box_id=module_id, tag_type='normal', is_delete=False).exclude(id=tag_id)
        titles = [item.title for item in tags]
        result = {}
        if len(titles) > 0:
            result = {'titles': "".join(titles)}
    return HttpResponse(json.dumps(result), content_type="application/json")


@transaction.commit_on_success
def main_page_publish(request, ):
    if request.method == "POST":
        box_ids = request.POST.get("module_ids")
        box_ids = box_ids.split(',')
        result = MainPagePublishTool.boxes_publish(box_ids, platform="iphone")
        if result['status'] == 'error':
            response = result
            response['desc'] = '发布失败! ' + result['detail']

        elif result['status'] == 'publish_success':
            response = {'status': 'success'}

        try:
            for cache_key in ['iphone_home_page_under_4', 'iphone_home_page_4_x']:
                CachePlan.clean_cache(key=cache_key, params=None)
        except:
            response = {'status': 'error', 'desc': '清缓存失败'}

        return HttpResponse(json.dumps(response), content_type="application/json")

