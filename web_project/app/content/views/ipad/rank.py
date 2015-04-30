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
        ranks = Ranking.objects.filter(platform=Platform.to_i('ipad'), is_delete=0).order_by('-position')
        return render(request, 'ipad/rank/ranking.html', {
            'ranks': ranks,
        })


def add_ranking(request):
    if request.method == 'GET':
        return render(request, 'ipad/rank/add_rank.html', )
    else:
        params = ['cid', 'title', 'platform']
        data_bucket = {k: request.POST.get(k, '') for k in params}
        Ranking.objects.create(**data_bucket)
        return HttpResponseRedirect(reverse('ipad_ranking'))


def query_ranking(request, query_id):
    try:
        rank = Ranking.objects.get(pk=query_id)
    except Ranking.DoesNotExist:
        return HttpResponseRedirect(reverse('ipad_ranking'))
    return render(request, 'ipad/rank/update_rank.html', {
        'rank': rank,
    })


def update_ranking(request, obj_id):
    if request.method == 'POST':
        params = ['cid', 'title', 'platform']
        data_bucket = {k: request.POST.get(k, '') for k in params}
        Ranking.objects.filter(pk=obj_id).update(**data_bucket)
        return HttpResponseRedirect(reverse('ipad_ranking'))


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
    try:
        Ranking.objects.filter(pk=obj_id).update(is_delete=1)
    except Ranking.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('ipad_ranking'))
