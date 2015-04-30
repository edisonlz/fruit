#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
from app.content.models import UserActionLog, Platform
from app.content.urls import CUSTOMIZED_URL_INFO, CUSTOMIZED_URL_TYPES
from app.permission.models import Perm
# from django.contrib.auth.models import User
from app.user.models import User


@login_required
def user_action_index(request):
    email = request.GET.get("email", "")
    platform_list = CUSTOMIZED_URL_TYPES['platforms']
    platform = request.GET.get("platform", '')
    if not platform:
        area_list = []
        family_list = []
        operation_list = []
        area = ''
        family = ''
        operation = ''
    else:
        # platform = request.GET.get("platform", platform_list[0])
        area_list = CUSTOMIZED_URL_TYPES['areas'].get(platform, [])
        area = request.GET.get("area", '')
        # area = request.GET.get("area", area_list[0])
        if not area:
            family_list = []
            operation_list = []
            family = ''
            operation = ''
        else:
            family_list = CUSTOMIZED_URL_TYPES['families'][platform].get(area, [])
            # family = request.GET.get("family", family_list[0])
            family = request.GET.get("family", '')
            if not family:
                operation_list = []
                operation = ''
            else:
                operation_list = CUSTOMIZED_URL_TYPES['operations'][platform][area].get(family, [])
                operation = request.GET.get("operation", '')
    logs = UserActionLog.objects.all()
    if email and len(email) > 0:
        user_ids = [u.id for u in User.objects.filter(email__icontains=email)]
        logs = UserActionLog.objects.filter(user__in=user_ids)
    if platform:
        logs = logs.filter(platform=platform)
    if area:
        logs = logs.filter(area=area)
    if family:
        logs = logs.filter(family=family)
    if operation:
        logs = logs.filter(operation=operation)


    logs = logs.order_by("-id")[0:30]
    users = User.objects.all()
    return render(request, "log/index.html", {"logs": logs,
                                              "users": users,
                                              "platform_list": platform_list,
                                              "area_list": area_list,
                                              "family_list": family_list,
                                              "operation_list": operation_list,
                                              "platform": platform,
                                              "area": area,
                                              "family": family,
                                              'operation': operation,
                                              "email": email})

def log_form_selectors(request):

    platform_list = CUSTOMIZED_URL_TYPES['platforms']
    platform = request.GET.get("platform", '')
    area = request.GET.get("area", '')
    family = request.GET.get("family", '')
    on_change = request.GET.get('on_change', '')
    if platform:
        area_list = CUSTOMIZED_URL_TYPES['areas'][platform]
        if on_change == 'platform':
            area_info_list = [[ar, Perm.ch_url_name(ar)] for ar in area_list]
            response = {'area_info_list': area_info_list}
            return HttpResponse(json.dumps(response), content_type="application/json")
    # else:
    #     platform = platform_list[0] # default
    #     area_list = CUSTOMIZED_URL_TYPES['areas'][platform]

    if area:
        family_list = CUSTOMIZED_URL_TYPES['families'][platform][area]
        if on_change == 'area':
            family_info_list = [[fa, Perm.ch_url_name(fa)] for fa in family_list]
            response = {'family_info_list': family_info_list}
            return HttpResponse(json.dumps(response), content_type="application/json")
    # else:
    #     area = area_list[0]
    #     # family_list = CUSTOMIZED_URL_TYPES['families'][platform][area]

    if family:
        operation_list = CUSTOMIZED_URL_TYPES['operations'][platform][area][family]
        if on_change == 'family':
            operation_info_list = [[op, Perm.ch_url_name(op)] for op in operation_list]
            response = {'operation_info_list': operation_info_list}
            return HttpResponse(json.dumps(response), content_type="application/json")
    # else:
    #     family = family_list[0]
    #     operation_list = CUSTOMIZED_URL_TYPES['operations'][platform][area][family]

    response = {}
    return HttpResponse(json.dumps(response), content_type="application/json")

