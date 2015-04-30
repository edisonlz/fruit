#coding=utf-8
from django.shortcuts import render, get_object_or_404
from wi_model_util.imodel import get_object_or_none
from app.content.models.android_search_background import SearchBackgroundVideo
from app.content.models import IosVipGoodsPageBack
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse
import json

def vip_goods_back_img(request,):
    device_type_param = request.GET.get('device_type', '')
    device_type = device_type_param or 'iphone'
    print '--------device_type:', device_type
    back_imgs = IosVipGoodsPageBack.objects.filter(is_delete=0, device_type=device_type).order_by('-position')
    return render(request, "background_img/vip_goods_page_back/vip_goods_page_back_imgs.html", {'back_imgs':back_imgs, 'device_type': device_type})


def vip_goods_back_img_add_img(request,):
    if request.method == "POST":
        device_type = request.GET.get('device_type')
        back_image = IosVipGoodsPageBack()
        back_image.add_position()
        back_image.vip_img = request.POST.get('vip_img')
        back_image.vip_img_hd= request.POST.get('vip_img_hd')
        back_image.device_type = device_type
        back_image.save()
        return HttpResponseRedirect(reverse('vip_goods_page_back_img_manage')+"?device_type="+device_type)

    else:
        device_type = request.GET.get('device_type')
        return render(request, "background_img/vip_goods_page_back/add_vip_goods_back_imgs.html", {'device_type':device_type })

def vip_goods_back_img_update_img(request, img_pk):
    if request.method == 'POST':
        print "post:========", request.POST
        device_type = request.GET.get('device_type')
        back_img = get_object_or_none(IosVipGoodsPageBack, pk=int(img_pk))
        back_img.vip_img = request.POST.get('vip_img')
        back_img.vip_img_hd = request.POST.get('vip_img_hd')
        back_img.save()
        return HttpResponseRedirect(reverse('vip_goods_page_back_img_manage')+"?device_type="+device_type)
    else:
        back_img = get_object_or_none(IosVipGoodsPageBack, pk=int(img_pk))
        device_type = request.GET.get('device_type')
        return render(request, "background_img/vip_goods_page_back/update_vip_goods_back_imgs.html", {'back_img':back_img, 'device_type':device_type })


def vip_goods_back_img_delete_img(request, img_pk):
    back_img = get_object_or_none(IosVipGoodsPageBack, pk=img_pk)
    device_type = request.GET.get('device_type')
    if back_img:
        back_img.is_delete = 1
        back_img.save()
    return HttpResponseRedirect(reverse('vip_goods_page_back_img_manage')+"?device_type="+device_type)


def vip_goods_back_img_update_status(request, ):
    if request.method == 'POST':
        opened_imgs = IosVipGoodsPageBack.objects.filter(is_delete=0, state=1, device_type=request.GET.get('device_type'))
        state = int(request.POST.get('value'))
        if opened_imgs and state:
            response = {'status': 'error', 'msg': u"只能开启一个!"}
        else:
            img = get_object_or_none(IosVipGoodsPageBack, pk=int(request.POST.get('pk')))
            if img:
                img.state = int(request.POST.get('value'))
                img.save()
                response = {'status': 'success'}
            else:
                response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")



