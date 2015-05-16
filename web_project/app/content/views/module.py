# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import Box, BoxType,BoxItem
from django.db import transaction
from app.content.models import Status

@login_required
def update_box_position(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            item_ids = map(int, box_ids.split(',')) or []
            position = 1
            for item_id in reversed(item_ids):

                item = Box.objects.get(id=item_id)
                item.position = position
                item.save()
                
                position += 1

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def cms_box_create(request):
    if request.method == 'POST':
        box_type = request.POST.get("box_type")
        title = request.POST.get("title")
        icount = request.POST.get("icount")

        box = Box()
        box.box_type = box_type
        box.title = title
        box.iner_count = icount
        box.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def cms_box_update(request):

    if request.method == 'POST':

        box_id = request.POST.get("box_id")
        box_type = request.POST.get("box_type")
        title = request.POST.get("title")
        icount = request.POST.get("icount")

        box = Box.objects.get(pk=int(box_id))
        box.box_type = box_type
        box.title = title
        box.iner_count = int(icount)
        box.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:

        box_id = request.GET.get("box_id")
        box = Box.objects.get(pk=box_id)

        return render(request, 'box/edit_box.html', {
            'box': box,
            'box_types': BoxType.TYPES,
        })

@login_required
def cms_box_delete(request):

    if request.method == 'POST':

        box_id = request.POST.get("box_id")

        flage = Box.delete_box(box_id)
        if flage:
            response = {'status': 'success',"box_id":box_id}
        else:
            response = {'status': 'error'}

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")



@login_required
def cms_box(request):
    if request.method == 'GET':
        boxes = Box.objects.filter(is_delete=False).order_by('-position')
        return render(request, 'box/box.html', {
            'boxes': boxes,
            'box_types': BoxType.TYPES,
            "menu":3,
        })

@login_required
def index(request):
    return render(request, 'base.html', {"menu":1})
 

@login_required
def status(request):

    response = []
    for state in Status.STATUS:
        response.append({"value":state[0] , "text": state[1]})

    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def update_status(request):

    pk =  request.POST.get("pk")
    value = int(request.POST.get("value")[0])
    
    box = Box.objects.get(id=pk)
    box.state = value
    box.save()

    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_position(request):
    if request.method == 'POST':

        box_ids = request.POST.get('box_ids')
        if box_ids:
            box_ids = box_ids.split(',')
        else:
            box_ids = []

        box_ids.reverse()
        position = 1
        for box_id in box_ids:
            box = Box.objects.get(id=box_id)
            box.position = position
            position += 1
            box.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")






@login_required
def box_item_list(request):
    """
        获取盒子内容列表
    """
    from app.content.models.item import Item
    if request.method == 'GET':

        box_id = request.GET.get("box_id")

        if not box_id:
            return

        items = BoxItem.objects.filter(is_delete=0,box_id=box_id).order_by('position')
        return render(request, 'box/box_item_list.html', {
            'boxitems': items,
            "box_id":box_id,
        })




@login_required
def add_item_to_box(request):
    """
        添加内容到某个盒子
    """
    if request.method == 'POST':

        box_id = request.POST.get('box_id')
        item_id = request.POST.get('item_id')
        # import pdb
        # pdb.set_trace()
        flage = BoxItem.addItem(int(box_id),int(item_id))

        if flage:
            response = {'status': 'success'}
        else:
            response = {'status': 'fail'}

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_item_to_box(request):
    """
        删除内容到某个盒子
    """
    if request.method == 'POST':

        box_id = request.POST.get('box_id')
        item_id = request.POST.get('item_id')

        flage = BoxItem.deleteItem(box_id,item_id)

        if flage:
            response = {'status': 'success'}
        else:
            response = {'status': 'fail'}


        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")



@login_required
def box_item_update_position(request):
    if request.method == 'POST':

        box_id = request.POST.get('box_id')
        item_ids = request.POST.get("item_ids")
        if item_ids:
            item_ids = item_ids.split(',')
        else:
            item_ids = []

        # item_ids.reverse()
        flage = BoxItem.updatePosition(box_id,item_ids)

        if flage:
            response = {'status': 'success'}
        else:
            response = {'status': 'fail'}

        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")



@login_required
def app_auto_complete(request):
    """auto complete return format"""
    #{ label: "Choice1", value: "value1" }
    from item import Item
    key = request.GET.get('key')

    items = Item.objects.filter(title__icontains=key)


    results = []
    if items:

        for item in items:
            results.append({"label": item.title,
                        "value": {"id": item.id, "title": item.title}
                        })

    # response={
    #     "status":"success",
    #     "data":results
    # }

    return HttpResponse(json.dumps(results), content_type="application/json")
