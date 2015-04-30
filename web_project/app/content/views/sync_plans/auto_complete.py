# coding: utf8
from app.content.models import Platform, VirtualNameFetch
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
import json


def get_candidates(request):
    query = request.POST.get('q', '')
    v_name = VirtualNameFetch()
    results = [item['name'] for item in v_name.v_name_list() if query in item['name']]
    results = results[:12]
    return HttpResponse(json.dumps(results), content_type="application/json")