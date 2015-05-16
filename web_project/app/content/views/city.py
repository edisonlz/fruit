# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import City
from django.db import transaction
from app.content.models import Status


@login_required
def cms_city(request):

    if request.method == 'GET':

        citys = City.all()

        return render(request, 'city/city.html', {
            'citys': citys,
        })

@login_required
def cms_city_create(request):
    if request.method == 'POST':

        name = request.POST.get("name")
        city_code = request.POST.get("city_code")
        phone = request.POST.get("phone")
        manager = request.POST.get("manager")
        
        city = City()
        city.name = name
        city.phone = phone
        city.city_code = city_code
        city.manager = manager
        city.status = Status.StatusOpen
        city.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def cms_city_update(request):
    if request.method == 'POST':

        pk = request.POST.get("pk")
        name = request.POST.get("name")
        cide_code = request.POST.get("city_code")
        phone = request.POST.get("phone")
        manager = request.POST.get("manager")

        city = City.objects.get(id=pk)
        city.name = name
        city.phone = phone
        city.cide_code = cide_code
        city.manager = manager
        city.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pk = request.GET.get("pk")
        city = City.objects.get(id=pk)
        return render(request, 'city/edit_city.html', {
            'city': city,
        })


@login_required
def delete(request):

    if request.method == 'POST':

        pk =  request.POST.get("id")

        city = City.objects.get(id=pk)
        city.is_delete = True
        city.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {'status': 'fail'}
        return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def update_status(request):

    pk =  request.POST.get("pk")
    value = int(request.POST.get("value")[0])
    
    city = City.objects.get(id=pk)
    city.state = value
    city.save()

    response = {'status': 'success'}
    return HttpResponse(json.dumps(response), content_type="application/json")



