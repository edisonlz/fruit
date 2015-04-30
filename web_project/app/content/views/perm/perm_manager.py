# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from content.models import IpadChannel
from content.views.common import redefine_item_pos, set_position


def perm_index(request):
    return render(request, 'permission/perm_index.html', {})