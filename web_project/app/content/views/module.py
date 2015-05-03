# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import Box, BoxType
from django.db import transaction


@login_required
def update_box_position(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            item_ids = map(int, item_ids.split(',')) or []
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
def cms_box(request):
    if request.method == 'GET':
        boxes = Box.objects.filter(is_delete=False).order_by('-position')
        return render(request, 'box/box.html', {
            'boxes': boxes,
            'box_types': BoxType.TYPES
        })

@login_required
def index(request):
    return render(request, 'base.html', {})


