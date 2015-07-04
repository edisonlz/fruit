# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import ShoppingAddress, City
from app.content.models import Status


@login_required
def cms_address(request):

    if request.method == 'GET':

        key = request.GET.get("key")
        city_id = request.GET.get("city_id")
        citys = City.all()

        addresses = ShoppingAddress.all()

        if key:
            addresses = addresses.filter(name__contains="%s" % key)
        
        #默认最早的一个城市
        if not city_id:
            if citys:
                city_id = citys.first().id

        if city_id:
            addresses = addresses.filter(city__id=city_id)
            

        return render(request, 'address/address.html', {
            'addresses': addresses,
            'key' : key,
            'citys':citys,
            'select_city_id': int(city_id)
        })

@login_required
def cms_address_create(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        onlinetime = request.POST.get("onlinetime")
        city_id = request.POST.get("city_id")
        manager = request.POST.get("manager")

        ad = ShoppingAddress()
        ad.name = name
        ad.phone = phone
        ad.address = address
        ad.onlinetime = onlinetime
        ad.status = Status.StatusOpen
        ad.city_id = city_id
        ad.manager = manager
        ad.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def cms_address_update(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")
        onlinetime = request.POST.get("onlinetime")
        city_id = request.POST.get("city_id")
        manager = request.POST.get("manager")

        ad = ShoppingAddress.objects.get(id=pk)
        ad.name = name
        ad.phone = phone
        ad.address = address
        ad.onlinetime = onlinetime
        ad.city_id = city_id
        ad.manager = manager
        ad.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pk = request.GET.get("pk")
        citys = City.all()
        ad = ShoppingAddress.objects.get(id=pk)
        return render(request, 'address/edit_address.html', {
            'ad': ad,
            'citys':citys,
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


@login_required
def delete(request):

    if request.method == 'POST':

        pk =  request.POST.get("id")

        box = ShoppingAddress.objects.get(id=pk)
        box.is_delete = True
        box.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def map(request):

    pk = request.GET.get("id")
    address = ShoppingAddress.objects.get(id=pk)

    return render(request, 'address/map.html', {
            'address' : address
        })

