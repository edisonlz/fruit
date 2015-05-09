# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import Box, BoxType , ShoppingAddress
from django.db import transaction
from app.content.models import Status



@login_required
def cms_address_create(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        onlinetime = request.POST.get("onlinetime")

        ad = ShoppingAddress()
        ad.name = name
        ad.phone = phone
        ad.address = address
        ad.onlinetime = onlinetime
        ad.status = Status.StatusOpen
        ad.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def cms_address(request):
    if request.method == 'GET':
        addresses = ShoppingAddress.objects.filter(is_delete=False).order_by('-position')
        return render(request, 'address/address.html', {
            'addresses': addresses,
        })


@login_required
def update_status(request):

    pk =  request.POST.get("pk")
    value = int(request.POST.get("value")[0])
    
    box = ShoppingAddress.objects.get(id=pk)
    box.state = value
    box.save()

    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_position(request):
    if request.method == 'POST':

        address_ids = request.POST.get('address_ids')
        if address_ids:
            address_ids = address_ids.split(',')
        else:
            address_ids = []

        address_ids.reverse()
        position = 1
        for aid in address_ids:
            box = ShoppingAddress.objects.get(id=aid)
            box.position = position
            position += 1
            box.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")



