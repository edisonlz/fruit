# coding=utf-8
import urllib, urllib2, json, logging
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.content.models import *
from django.shortcuts import render
from django.db.models import get_model

def get_game_info(request):
    if request.method == 'GET':
        game_info = {}
        product = request.GET.get('product')
        if product == 'iPad':
            game_id = request.GET.get('game_id')
            print game_id
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error':e.code}
                else:
                    data = {'error':e}
        elif product == 'iphone':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error':e.code}
                else:
                    data = {'error':e}
        elif product == 'android':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.ANDROID_GAME_HOST,
                                                         path=settings.ANDROID_GAME_PATH, game_id=game_id)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error': e.code}
                else:
                    data = {'error': e}
    return HttpResponse(json.dumps(data))


def get_paged_dict(item_list, page_pos=1, one_page_count=20):
    p = Paginator(item_list, one_page_count)
    display_pages = []
    try:
        items = p.page(page_pos)
        now_page = int(page_pos)
    except (PageNotAnInteger, EmptyPage, ValueError):
        items = p.page(1)
        now_page = 1
    if p.num_pages <= 5:
        display_pages = map(str, range(1, p.num_pages+1))
    else:
        if now_page - 4 > 1:
            display_pages += ['1', '...', ] + map(str, range(now_page-2, now_page+1))
        else:
            display_pages += map(str, range(1, now_page+1))
        if now_page + 4 < p.num_pages:
            display_pages += map(str, range(now_page+1, now_page+3)) + ['...', str(p.num_pages)]
        else:
            display_pages += map(str, range(now_page+1, p.num_pages+1))
    page_info_dict = {'items': items, 'page_range': p.page_range, 'num_pages': str(p.num_pages), 'now_page': str(now_page),
                      'display_pages': display_pages, 'previous_page': now_page-1, 'next_page': now_page+1}
    return page_info_dict


def update_items_state(request):
    if request.method == 'POST':
        item_ids = request.POST.get("item_ids")
        value = request.POST.get("value")
        target_model = request.POST.get('target_model')
        if item_ids and value is not None and target_model:
            try:
                get_model('content', target_model).objects.filter(id__in=item_ids.split(',')).update(state=int(value))
                response = {'status': 'success', 'item_ids': item_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"更新状态失败!"}
        else:
            response = {'status': 'error', 'msg': u"目标不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


def new_tag_jump_type_info(request):
    box_id = request.GET.get('box_id')
    box = HomeBox.objects.get(pk=box_id)
    tag_type_info = box.tag_type_info('tag')
    tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
    tag_type_list = tag_type_hash.items()
    return render(request,'common_module/new_tag_jump_type.html',{"tag_type_list": tag_type_list})
