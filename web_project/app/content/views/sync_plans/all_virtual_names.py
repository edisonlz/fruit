# coding: utf8
from app.content.models import Platform, VirtualNameFetch
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from operator import itemgetter
import json


def show_all_virtual_name(request):
    v_name = VirtualNameFetch().v_name_list()
    resort_names = sorted(v_name, cmp=lambda x, y: cmp(x['id'], y['id']))
    return render(request, "syncjob/show_all_virtual_names.html", {'v_names': resort_names})