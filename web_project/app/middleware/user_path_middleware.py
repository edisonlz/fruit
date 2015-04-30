# coding=utf-8
# profile_middleware - a middleware that profiles views
#
# Inspired by udfalkso's http://www.djangosnippets.org/snippets/186/
# and the Shwagroo Team's http://www.djangosnippets.org/snippets/605/
#
# Install this by adding it to your MIDDLEWARE_CLASSES.  It is active
# if you are logged in as a superuser, or always when settings.DEBUG
# is True.
#
# To use it, pass 'profile=1' as a GET or POST parameter to any HTTP
# request.

from base64 import b64decode, b64encode
import cPickle
from cStringIO import StringIO
from decimal import Decimal
import hotshot, hotshot.stats
import pprint
import sys
import tempfile

from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.db import connection, reset_queries
from django.http import HttpResponse
from django.utils import html
from django.utils.http import urlencode
import time
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
import re
from app.content.models.log import UserActionLog
from app.content.urls import CUSTOMIZED_URL_INFO
import json
from app.user.models import UserBoxPerm
from app.content.models import HomeBox, Platform, IpadBoxVideo, IphoneBoxVideo, AndroidBoxVideo, WinPhoneBoxVideo, \
    HomeCommonBox


class UserPathMiddleware(object):
    def process_response(self, request, response):
        # # only write POST request's log
        # if request.method == "GET":
        # return response
        # only write login-user's log
        if not (hasattr(request, "user") and request.user.id):
            return response

        # only write app.content.urls.has_cust_ch_name_attribute's log
        current_url_info = {}
        for url_regex, url_info in CUSTOMIZED_URL_INFO.items():
            if re.compile("^" + url_regex).search(request.path[1:]):
                current_url_info = url_info.get('cust_ch_name', {})
        if not current_url_info:
            return response

        platform = current_url_info.get('platform', '')
        area = current_url_info.get('area', '')
        family = current_url_info.get('family', '')
        operation = current_url_info.get('operation', '')
        if request.method == "POST":
            # TODO: 1 过滤掉没用的参数; 2 能够显示中文
            #TODO: 区分开启、关闭
            params = request.POST.dict()
        else:
            # Don't write log for GET request, but '删除'
            if not operation == 'delete':
                return response
            params = request.GET.dict()
            # 猜测被删除的对象的id: url最后面的数字
            if 'id' not in params:
                deleted_id = request.path[1:].split('/')[-1]
                if deleted_id:
                    params['id'] = deleted_id

        params = json.dumps(params, sort_keys=True, indent=4, ensure_ascii=False)
        log = UserActionLog()
        log.method = request.method
        log.path = request.path
        log.user = request.user
        log.platform = platform
        log.area = area
        log.family = family
        log.operation = operation
        log.params = params
        log.save()
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print "***view function", view_func.func_name

    def process_request(self, request):
        path = request.path.lower()

        # avoid some views are not decorated with login_required
        if not request.user.is_authenticated():
            if path == reverse('signin') or path.startswith('/admin'):
                return
            else:
                return HttpResponseRedirect(reverse('signin'))

        # temporarily not allow editor to access user control backend
        if not request.user.is_super and path.startswith('/user'):
            return render(request, 'permission_deny.html')

        if request.user.is_super or request.user.is_super_editor:
            return

        for func in [check_box_perm, check_video_perm, check_recommend_pool, check_recommend_video, check_channel,
                     check_manage_access, check_brand]:
            match_flag, perm_flag = func(request)
            if match_flag:
                if not perm_flag:
                    return render(request, 'permission_deny.html')
                else:
                    return

        return


def get_request_params(request):
    path, meth = request.path, request.method
    req = request.POST if meth == 'POST' else request.GET
    return path, meth, req


def check_brand(request):
    path, meth, req = get_request_params(request)
    pat_list = [
        re.compile(r'^/content/brand/brand_module/(?P<action>\w+(_\w+)*)(/(?P<del_id>\d+))?$'),
        re.compile(r'^/content/brand/brand_video/(?P<action>\w+(_\w+)?)(/(?P<del_id>\d+))?$')
    ]
    for index, pat in enumerate(pat_list):
        res = pat.match(path)
        if res:
            action, del_id = res.groupdict()['action'], res.groupdict()['del_id']
            if index == 0:
                for key in ['add', 'delete']:
                    if key in action:
                        return True, False
                if 'update' in action:
                    return _acquire_perm(request, del_id, 5)
            else:
                for key in ['add_video', 'delete', 'update']:
                    if key in action:
                        return _acquire_perm(request, request.GET.get('module_id'), 5)

    return False, False


def check_manage_access(request):
    if request.path.startswith('/user'):
        return True, False
    return False, False


INDEX_PLAT_CLS = {
    'iphone': IphoneBoxVideo,
    'ipad': IpadBoxVideo,
    'android': AndroidBoxVideo,
    # 'win_phone': WinPhoneBoxVideo
}


def check_box_perm(request):
    box_pat = re.compile(r'^/content/(?P<platform>iphone|ipad|android|win_phone)/main_page/' +
                         '(?P<func>[\w_]+)/module(?:_tag)?(/\d+)?$')
    res = box_pat.match(request.path)
    if res:
        if request.user.is_normal_user:
            func = str(res.groupdict()['func'])
            perm_flag = False
            if func in ['query', 'update']:
                perm_flag = True
            return True, perm_flag
    if request.method == 'POST':
        platforms = INDEX_PLAT_CLS.keys()
        for platform in platforms:
            if reverse(platform + '_uniq_modules') == request.path and request.user.is_normal_user:
                return True, False

    return False, False


def get_boxid_from_video(video_id, platform):
    video_id = int(video_id)
    video = INDEX_PLAT_CLS[platform].objects.filter(id=video_id).first()
    return video.box_id if video else None


def check_video_perm(request):
    video_pat = re.compile(r'^/content/(?P<platform>iphone|ipad|android|win_phone)/main_page/' +
                           '(?!uniq_modules|preview)(?P<func>[\w_]+)(/video(/(?P<del>\d+))?)?$')
    res = video_pat.match(request.path)
    if res:
        platform, func = str(res.groupdict()['platform']), str(res.groupdict()['func'])
        box_id, pass_flag = None, False
        if request.method == 'POST':
            post_d = request.POST.dict()
            if func == 'add':
                box_id = post_d.get('box_id')
            elif func == 'update':
                box_id = get_boxid_from_video(post_d.get('id'), platform)
            elif func == 'update_video_status' or func == 'update_status':
                video_id = post_d.get('video_ids', '').split(',')[0]
                box_id = get_boxid_from_video(video_id, platform)
            elif func == 'update_video_value':
                box_id = get_boxid_from_video(post_d.get('video_id'), platform)
            elif func == 'videos':
                video_id = post_d.get('item_ids', '').split(',')[0]
                box_id = get_boxid_from_video(video_id, platform)
            else:
                pass_flag = True
            if not pass_flag:
                return True, UserBoxPerm.has_perm(box_id, request.user)
        else:
            if func == 'delete':
                del_num = res.groupdict()['del']
                box_id = get_boxid_from_video(del_num, platform)
                return True, UserBoxPerm.has_perm(box_id, request.user)

    return False, False


def check_recommend_pool(request):
    pattern = re.compile(r'^/content/common_content/(current_box_page/(\d+)/box/' +
                         '((?P<box_id>\d+)/videos)|(add_box|box(es)?)(?P<func>/[\w/_\d]+)?)$')
    res = pattern.match(request.path)
    perm_flag = True
    if request.method == 'POST' and request.path == reverse('home_common_boxes_update_box_title'):
        return True, UserBoxPerm.has_perm(request.POST.get('box_id'), request.user, 1)

    if res:
        box_id = res.groupdict()['box_id']
        func = res.groupdict()['func']
        if request.method == 'POST':
            if not func and box_id:
                perm_flag = UserBoxPerm.has_perm(box_id, request.user, 1)
        else:
            if func and 'delete' in func:
                perm_flag = False
        return True, perm_flag

    return False, perm_flag


def check_recommend_video(request):
    '''not handle url name "home_common_videos_update_status" '''
    pattern = re.compile(r'^/content/common_content/current_box_page/' +
                         '(\d+)/box/(?P<box_id>\d+)/videos?(/\w+_?\w+|/\d+/[_\w]+)$')
    path = request.path
    res = pattern.match(path)
    perm_flag, match_flag = True, False

    def _check_perm(videoid):
        boxid = HomeCommonBox.objects.filter(id=video_id).first() if videoid else None
        if boxid:
            return UserBoxPerm.has_perm(boxid, request.user, 1)

    if res:
        match_flag = True
        box_id = res.groupdict()['box_id']
        if request.method == 'POST':
            perm_flag = UserBoxPerm.has_perm(box_id, request.user, 1)

    if path == reverse('home_common_videos_update_video_value'):
        video_id = request.POST.get('video_id')
        perm_flag = _check_perm(video_id)
        match_flag = True
    elif path == reverse('home_common_videos_sync_box_videos'):
        match_flag = True
        box_id = request.POST.get("current_box_id")
        if box_id:
            perm_flag = UserBoxPerm.has_perm(box_id, request.user, 1)

    return match_flag, perm_flag


def _acquire_perm(request, box_id, src):
    try:
        return True, UserBoxPerm.has_perm(box_id, request.user, src)
    except TypeError:
        return True, False


def check_channel(request):
    level_box = {
        'channel': '%s_%s_new_channel',
        'subchannel': '%s_%s_sub_channel',
        'module': '%s_%s_sub_channel_module',
        'item': '%s_%s_sub_channel_module_item'
    }
    action_arr = ['add', 'update', 'delete']
    path, meth, req = get_request_params(request)

    for platform in ['iphone', 'ipad', 'android']:
        for action in action_arr:
            src_number = UserBoxPerm.get_src_name_from_platform(platform)
            for k, v in level_box.iteritems():
                full_name = v % (platform, action)

                if k == 'channel':
                    if action == 'delete':
                        pat = re.compile(r'/content/{}/delete/new_channel/(?P<del_id>\d+)$'.format(platform))
                        res = pat.match(path)
                        if res:
                            return True, False
                        continue

                    if reverse(full_name) == path:
                        if action == 'add':
                            return True, False
                        elif action == 'update':
                            return _acquire_perm(request, req.get('id'), src_number)
                else:
                    if reverse(full_name) == path:
                        return _acquire_perm(request, req.get('channel_id'), src_number)

            if reverse('%s_update_item_value_sub_channel_module_item' % platform) == path:
                return _acquire_perm(request, req.get('channel_id'), src_number)

    if meth == 'POST':
        pat_list = [
            re.compile(r'^/content/android/update_channel_navigation/\d+$'),
            re.compile(r'^/content/android_update_channel_video_value$'),
        ]
        for pat in pat_list:
            # normal user cannot modify android navigation
            res = pat.match(path)
            if res:
                return True, False

    # below pattern is used to stop updating title in channel_video
    pat = re.compile(r'^/content/android/(?P<action>\w+(_\w+)*)/channel_videos?(/(?P<del_id>\d+))?$')
    res = pat.match(path)
    if res:
        action, del_id = res.groupdict()['action'], res.groupdict()['del_id']
        if action in ['update_video_value', 'add', 'delete', 'update']:
            return _acquire_perm(request, req.get('channel_id'), 4)

    return False, False


# def check_channel(request):
# check_iphone_channel(request)
# for func in (check_iphone_channel,):
#         is_match, is_perm = func(request)
#         if is_match:
#             return is_match, is_perm
#
#     return False, False


# def check_fragment(request):
#     chip_pat = re.compile(r'^/content/android/(?P<func>\w+/?\w+/)?video_list(s)?(/(?P<del>\d+))?$')
#     match_flag, forbid_flag = check_pattern(chip_pat, request.path)
#     if not match_flag:
#         chip_pat_2 = re.compile(r'^/content/android/video_list/(\d+/)?(\w+)(/\d+)?$')
#         match_flag, forbid_flag = check_pattern(chip_pat_2, request.path)
#
#     return match_flag, not forbid_flag
#
#
# def check_pattern(pat, path):
#     forbid_arr = ['update', 'add', 'delete']
#     forbid_flag = False
#     res = pat.match(path)
#     if res:
#         func = str(res.groupdict()['func'])
#         for key in forbid_arr:
#             if key in func:
#                 forbid_flag = True
#                 break
#         return True, forbid_flag
#     else:
#         return False, False
