#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import HomeBox
from app.content.models import Platform, Status, BoxType
from app.content.lib.main_page_publish_tool import MainPagePublishTool
from django.db import transaction


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
        return HttpResponseRedirect(reverse('winphone_modules'))
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("win_phone"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("win_phone")
        datas = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('position')
        return render(request, 'winphone/main_page/module_manage/module/modules.html',
                      {'modules': datas, 'box_type_list': box_type_list,
                       'box_type_hash': box_type_hash})


@login_required
def uniq_modules(request):
    if request.method == 'POST':
        module_ids = request.POST.get('box_ids')
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
        return HttpResponseRedirect(reverse('winphone_uniq_modules'))
    else:
        #Get Comes here
        box_type_info = Platform.box_types(Platform.to_i("win_phone"))
        box_type_hash = {item['id']: item['desc'] for item in box_type_info}
        box_type_list = box_type_hash.items()
        platform_data = Platform.to_i("win_phone")
        datas = HomeBox.objects.filter(is_delete=False, platform=platform_data).order_by('position')
        navigation_list = ["内容管理", "抽屉列表"]
        return render(request, 'winphone/main_page/module_manage/module/uniq_modules.html',
                      {'modules': datas, 'box_type_list': box_type_list,
                       'box_type_hash': box_type_hash,
                       'module_state_hash': Status.STATUS_HASH,
                       'navigation_list': enumerate(navigation_list)})


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
def delete_module(request, module_id):
    home_box = HomeBox.objects.get(pk=module_id)
    home_box.is_delete = 1
    home_box.save()
    return HttpResponseRedirect(reverse('winphone_uniq_modules'))


@login_required
def query_module(request, box_id):
    module = get_object_or_404(HomeBox, pk=box_id)
    box_type_info = Platform.box_types(Platform.to_i("win_phone"))
    box_type_hash = {item['id']: item['desc'] for item in box_type_info}
    box_type_list = box_type_hash.items()
    return render(request, 'winphone/main_page/module_manage/module/update_module.html',
                  {'module': module,
                   "box_type_list": box_type_list,
                  })


@login_required
def add_module(request):
    if request.method == 'POST':
        platform_type = Platform.to_i("win_phone")
        home_box = HomeBox()
        home_box.platform = int(platform_type)
        home_box.update_value(request.POST)
        return HttpResponseRedirect(reverse('winphone_uniq_modules'))
    else:
        return render(request, 'winphone/main_page/module_manage/module/add_module.html')


@login_required
def update_module(request):
    id = request.POST.get("id")
    try:
        home_box = HomeBox.objects.get(id=id)
        home_box.update_value(request.POST)
    except HomeBox.DoesNotExist, e:
        pass
    return HttpResponseRedirect(reverse('winphone_uniq_modules'))


@transaction.commit_on_success
def main_page_publish(request, ):
    if request.method == "POST":
        box_ids = request.POST.get("module_ids")
        box_ids = box_ids.split(',')
        result = MainPagePublishTool.boxes_publish(box_ids, platform="winphone")
        if result['status'] == 'error':
            response = result
            response['desc'] = '同步失败! ' + result['detail']

        elif result['status'] == 'publish_success':
            response = {'status': 'success'}

        return HttpResponse(json.dumps(response), content_type="application/json")







