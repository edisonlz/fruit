# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from app.content.views.common import redefine_item_pos, set_position
from app.content.models import AndroidChannelNavigation, Status
import json

@login_required
def channel_navigation(request,):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(AndroidChannelNavigation, item_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    navigations = AndroidChannelNavigation.objects.filter(is_delete=0).order_by('-position')
    nav_types = AndroidChannelNavigation.NAV_TYPES
    return render(request, 'android/channel_navigation/channel_navi.html',
            {
                    'navigations':navigations,
                    'navi_state_hash':Status.STATUS_HASH,
                    'nav_types_hash': AndroidChannelNavigation.NAV_TYPES,
                    'nav_types': AndroidChannelNavigation.NAV_TYPES.items(),
            })


@login_required
def add_channel_navigation(request,):
    if request.method == 'POST':
        navi = AndroidChannelNavigation()
        set_position(navi, AndroidChannelNavigation)
        navi.title = request.POST.get('title')
        navi.save()
        return HttpResponseRedirect(reverse('android_channel_navigation'))



@login_required
def update_channel_navigation(request, navi_module_id):

    navigation = AndroidChannelNavigation.objects.get(id=navi_module_id)
    if request.method == "POST":
        title = request.POST.get('title')
        navigation.title = title
        navigation.nav_type = int(request.POST.get('nav_type','1'))
        navigation.save()
        navigations = AndroidChannelNavigation.objects.filter(is_delete=0).order_by('-state')
        return render(request, 'android/channel_navigation/channel_navi.html',
                      {
                          'navigations': navigations,
                          'nav_types_hash': AndroidChannelNavigation.NAV_TYPES,
                          'navi_state_hash': Status.STATUS_HASH
                      })
    else:
        nav_types = AndroidChannelNavigation.NAV_TYPES
        return render(request, 'android/channel_navigation/update_channel_navi.html',
                      {'navigation':navigation,
                       'nav_types': AndroidChannelNavigation.NAV_TYPES.items(), })


@login_required
def delete_channel_navigation(request, navi_module_id):
    navigation = AndroidChannelNavigation.objects.get(id=navi_module_id)
    navigation.is_delete  = 1
    navigation.save()
    navigations = AndroidChannelNavigation.objects.filter(is_delete=0).order_by('-state')
    return render(request, 'android/channel_navigation/channel_navi.html',
                  {
                      'navigations': navigations,
                      'nav_types_hash': AndroidChannelNavigation.NAV_TYPES,
                      'navi_state_hash': Status.STATUS_HASH
                  })

@login_required
def update_status_channel_navigation(request):
    if request.method == 'POST':
        module_ids = request.POST.get("module_ids")
        print "module_ids",module_ids
        value = request.POST.get("value")
        if module_ids and value:
            try:
                AndroidChannelNavigation.objects.extra(where=['id IN (%s)' % module_ids]).update(state=int(value))
                response = {'status': 'success', 'module_ids': module_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"模块不存在!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")

