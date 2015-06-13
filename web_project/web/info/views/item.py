__author__ = 'yinxing'
# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models.item import Item
from django.db import transaction
from app.content.models import Status


def item_detail(request, item_id):
    print item_id
    return render(request, 'web/item_detail.html')
