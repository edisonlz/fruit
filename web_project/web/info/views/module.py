# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import Box, BoxType,BoxItem ,City ,ShoppingAddress, BoxType
from django.db import transaction
from app.content.models import Status



def index(request):

    boxes = Box.getBoxes()
    return render(request, 'web/index.html', {"boxes":boxes,"BoxType":BoxType})



