#encoding=utf8

from django.http import HttpResponse
from django.shortcuts import HttpResponse, render_to_response, render
from models import Perm, UserGroupPerms, UserPerms
from django.core.exceptions import *

from django.core import urlresolvers
from django import forms
from django.contrib.auth.models import User, Group
from app.content.urls import CUSTOMIZED_URL_INFO


def initialize(request):
    patterns = _get_named_patterns()
    r = HttpResponse("initialized", content_type='text/plain')
    for i1, i2, i3 in patterns:
        #Perm.objects.create(name = i1,code = i3,url_regex = i3,action = i1)
        try:
            Perm.objects.get(code=i3)

        except ObjectDoesNotExist:
            p = Perm()
            p.name = i1
            p.code = i3
            p.url_regex = i3
            p.action = i1
            ch_name = CUSTOMIZED_URL_INFO.get(i3, {}).get('cust_ch_name', {})
            p.platform = ch_name.get('platform', '')
            p.area = ch_name.get('area', '')
            p.family = ch_name.get('family', '')
            p.operation = ch_name.get('operation', '')
            p.save()
    return r


def _get_named_patterns():
    "Returns list of (pattern-name, pattern) tuples"
    resolver = urlresolvers.get_resolver(None)

    for url_ptn in resolver.url_patterns:
        print url_ptn

    for key, value in resolver.reverse_dict.items():
        if isinstance(key, basestring):
            print key, value
    patterns = [
        (key, value[0][0][0], value[1])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ]
    return patterns


def edit(request):
    if request.method == "GET":
        perms = Perm.objects.all().order_by('platform', 'area', 'family', 'operation')
        uids = request.GET.get("uids", "")
        gids = request.GET.get("gids", "")
        if uids:
            member = User.objects.get(id=uids)
            _user_perms = UserPerms.objects.filter(user=member)
            given_perm_ids = [up.perm_id for up in _user_perms]
        elif gids:
            member = Group.objects.get(id=gids)
            _usergroup_perms = UserGroupPerms.objects.filter(group=member.id)
            given_perm_ids = [up.perm_id for up in _usergroup_perms]
        for index, perm in enumerate(perms):
            perms[index].ch_platform = Perm.ch_url_name(perm.platform)
            perms[index].ch_area = Perm.ch_url_name(perm.area)
            perms[index].ch_family = Perm.ch_url_name(perm.family)
            perms[index].ch_operation = Perm.ch_url_name(perm.operation)

        return render_to_response("admin/edit_perms.html", locals())
    else:
        uids = request.POST.get("uids")
        gids = request.POST.get("gids")

        chosen_perms = map(int, request.POST.getlist("chosen_perms"))

        if uids:
            former_perms = UserPerms.objects.filter(user__id=uids)
            former_perm_ids = [up.perm_id for up in former_perms]
            to_delete_perms = set(former_perm_ids) - set(chosen_perms)
            to_add_perms = set(chosen_perms) - set(former_perm_ids)

            UserPerms.change_perm(uids, to_delete_perms, to_add_perms)

        if gids:
            former_perms = UserGroupPerms.objects.filter(group__id=gids)
            former_perm_ids = [ugp.perm_id for ugp in former_perms]
            to_delete_perms = set(former_perm_ids) - set(chosen_perms)
            to_add_perms = set(chosen_perms) - set(former_perm_ids)

            UserGroupPerms.change_perm(gids, to_delete_perms, to_add_perms)

        return HttpResponse("EDIT PERMS")