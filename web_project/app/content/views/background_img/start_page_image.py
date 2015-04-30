# coding: utf8
from content.models import EntranceImage
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
import json


def start_images(request):
    terminal_type = int(request.GET.get('terminal_type', '0'))
    if terminal_type not in EntranceImage.terminal_int_type_set():
        terminal_type = 1
    start_image_objs = EntranceImage.objects.filter(terminal_type=terminal_type)
    return render(request, 'background_img/show_client_start_images.html', {
        'start_image_objs': start_image_objs,
        'terminal_type_str': EntranceImage.get_terminal_str(terminal_type),
        'terminal_type': terminal_type,
        'terminal_tuple': EntranceImage.TERMINAL
    })


def add_start_image(request):
    if request.method == 'GET':
        terminal_type = int(request.GET.get('terminal_type', '0'))
        return render(request, 'background_img/add_client_start_image.html', {
            'terminal_type_str': EntranceImage.get_terminal_str(terminal_type),
            'terminal_type': terminal_type
        })
    else:
        post = request.POST
        params = ['terminal_type', 'image', 'image_4s', 'image_5s', 'image_6', 'image_6plus', 'effect_at', 'expired_at']
        data_bucket = {k: post.get(k, '') for k in params}
        EntranceImage.objects.create(**data_bucket)
        return HttpResponseRedirect(reverse('client_start_pages') + '?terminal_type=' + data_bucket['terminal_type'])


def query_start_image(request, query_id):
    terminal_type = int(request.GET.get('terminal_type', '0'))
    try:
        image_object = EntranceImage.objects.get(pk=query_id)
    except EntranceImage.DoesNotExist:
        return HttpResponseRedirect(reverse('client_start_pages'))

    return render(request, 'background_img/update_client_start_image.html', {
        'terminal_type_str': EntranceImage.get_terminal_str(terminal_type),
        'terminal_type': terminal_type,
        'obj': image_object
    })


def update_start_image(request, obj_id):
    if request.method == 'POST':
        params = ['terminal_type', 'image', 'image_4s', 'image_5s', 'image_6', 'image_6plus', 'effect_at', 'expired_at']
        data_bucket = {k: request.POST.get(k, '') for k in params}
        EntranceImage.objects.filter(pk=obj_id).update(**data_bucket)
        return HttpResponseRedirect(reverse('client_start_pages') + '?terminal_type=' + data_bucket['terminal_type'])


def update_start_image_state(request, obj_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        response = {'status': 'error', 'msg': '出现错误，刷新后重试'}
        try:
            target = EntranceImage.objects.get(pk=obj_id)
            if hasattr(target, name):
                setattr(target, name, value)
                target.save()
            response = {'status': 'success'}
        except EntranceImage.DoesNotExist:
            pass
        return HttpResponse(json.dumps(response), content_type="application/json")


def delete_start_image(request, obj_id):
    terminal_type = request.GET.get('terminal_type', '')
    try:
        EntranceImage.objects.filter(pk=obj_id).delete()
    except EntranceImage.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('client_start_pages') + '?terminal_type=' + terminal_type)
