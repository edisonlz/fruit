# coding: utf8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from content.models import Ranking, Platform
from content.views.common import redefine_item_pos
import json


def ranking(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        response = {'status': 'error'}
        if item_ids:
            try:
                redefine_item_pos(Ranking, item_ids)
                response = {'status': 'success'}
            except Ranking.DoesNotExist:
                pass
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        ver_diff = int(request.GET.get('ver_diff', '0'))
        if ver_diff not in Ranking.ver_diff_value_set():
            ver_diff = 0
        ranks = Ranking.objects.filter(platform=Platform.to_i('iphone'), ver_diff=ver_diff, is_delete=0)\
            .order_by('-position')
        return render(request, 'iphone/rank/ranking.html', {
            'ranks': ranks,
            'ver_diff': ver_diff
        })


def add_ranking(request):
    if request.method == 'GET':
        ver_diff = int(request.GET.get('ver_diff', '0'))
        return render(request, 'iphone/rank/add_rank.html', {
            'ver_diff': ver_diff
        })
    else:
        params = ['cid', 'title', 'ver_diff', 'platform']
        data_bucket = {k: request.POST.get(k, '') for k in params}

        Ranking.objects.create(**data_bucket)
        return HttpResponseRedirect(reverse('iphone_ranking') + '?ver_diff=' + data_bucket['ver_diff'])


def query_ranking(request, query_id):
    ver_diff = int(request.GET.get('ver_diff', '0'))
    try:
        rank = Ranking.objects.get(pk=query_id)
    except Ranking.DoesNotExist:
        return HttpResponseRedirect(reverse('iphone_ranking'))

    return render(request, 'iphone/rank/update_rank.html', {
        'rank': rank,
        'ver_diff': ver_diff
    })


def update_ranking(request, obj_id):
    if request.method == 'POST':
        params = ['cid', 'title', 'ver_diff', 'platform']
        data_bucket = {k: request.POST.get(k, '') for k in params}
        Ranking.objects.filter(pk=obj_id).update(**data_bucket)
        return HttpResponseRedirect(reverse('iphone_ranking') + '?ver_diff=' + data_bucket['ver_diff'])


def update_ranking_state(request, obj_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        value = request.POST.get('value')
        response = {'status': 'error', 'msg': '出现错误，刷新后重试'}
        try:
            target = Ranking.objects.get(pk=obj_id)
            if hasattr(target, name):
                setattr(target, name, value)
                target.save()
            response = {'status': 'success'}
        except Ranking.DoesNotExist:
            pass
        return HttpResponse(json.dumps(response), content_type="application/json")


def delete_ranking(request, obj_id):
    ver_diff = request.GET.get('ver_diff', '0')
    try:
        Ranking.objects.filter(pk=obj_id).update(is_delete=1)
    except Ranking.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('iphone_ranking') + '?ver_diff=' + ver_diff)
