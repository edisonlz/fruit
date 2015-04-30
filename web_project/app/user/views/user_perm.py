# coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from app.user.models import UserBoxPerm, User, HomeBox
from app.content.models import Platform
import json


def get_src_info(src_name):
    """
    获取来源数据
    """
    if not src_name:
        src_name = 'main_page_device'
    src_name = str(src_name)
    src_num = UserBoxPerm.get_src_id(src_name)
    src_cls = UserBoxPerm.get_src_cls(src_num)
    return {
        'src_str': src_name,
        'src_num': src_num,
        'src_cls': src_cls
    }


def get_box_and_src_info(src_name, box_id, platform=None):
    src_dict = get_src_info(src_name)
    if src_dict['src_str'] == 'main_page_device':
        box = src_dict['src_cls'].objects.filter(id=int(box_id), platform=Platform.to_i(platform)).first()
    elif src_dict['src_str'] == 'main_page_recommend':
        box = src_dict['src_cls'].objects.filter(id=int(box_id)).first()
    else:
        box = src_dict['src_cls'].objects.filter(id=int(box_id)).first()
        # box = None
    src_dict.update({'box': box})
    return src_dict


def show_box_perm(request):
    if request.user.is_super or request.user.is_super_editor:
        box_id = request.GET.get('box_id')
        platform = request.GET.get('platform', '')
        src = UserBoxPerm.get_src_id(request.GET.get('src'))
        perm_list = UserBoxPerm.objects.filter(drawer_id=box_id, source=src)
        info = get_box_and_src_info(request.GET.get('src'), box_id, platform)
        for perm in perm_list:
            user = User.objects.get(id=perm.user_id)
            perm.user = user

        return render(request, 'show_box_perm.html', {
            'perm_list': perm_list,
            'box': info['box'],
            'platform': platform,
            'src': info['src_str']
        })
    else:
        return HttpResponseRedirect(reverse('cms_index'))


@login_required
def add_box_perm(request):
    if request.method == 'POST':
        post = request.POST
        user_id_list = post.get('user_id_list', '').split(';')
        box_id = post.get('box_id')
        platform = post.get('platform', '')
        src_name = post.get('src', '')
        for user_id in user_id_list:
            try:
                UserBoxPerm.objects.get_or_create(**{
                    'drawer_id': box_id,
                    'user_id': user_id,
                    'source': UserBoxPerm.get_src_id(src_name)
                })
            except Exception, e:
                pass
        return HttpResponseRedirect(reverse("show_main_box_perm") + '?platform=' + platform + '&box_id=' + box_id
                                    + '&src=' + src_name)
    else:
        box_id = request.GET.get('box_id')
        platform = request.GET.get('platform', '')
        info = get_box_and_src_info(request.GET.get('src'), box_id, platform)
        box = info['box']
        user_id_list = [perm.user_id for perm in
                        UserBoxPerm.objects.filter(drawer_id=info['box'].id, source=info['src_num'])] if box else []
        user_list = [user for user in User.objects.all() if user.id not in user_id_list and user.is_normal_user]
        return render(request, 'add_box_perm.html', {
            'user_list': user_list,
            'box': info['box'],
            'src': info['src_str'],
            'platform': platform
        })


@login_required
def del_box_perm(request):
    if request.method == 'POST':
        post = request.POST
        user_id = post.get('user_id')
        drawer_src_list = post.get('drawer_and_src').split('|')
        for item in drawer_src_list:
            drawer_id, src = item.split(',')
            try:
                UserBoxPerm.objects.filter(drawer_id=drawer_id, source=src, user_id=user_id).delete()
            except UserBoxPerm.DoesNotExist:
                pass
        return HttpResponseRedirect(reverse('personal_perm') + '?uid=' + user_id)


def sync_user_perm(request):
    if request.method == 'POST':
        user_id_list = request.POST.get('user_id_list', '').split(';')
        box_src_tup = request.POST.get('box_id_list', '').split('|')
        for user_id in user_id_list:
            for tup in box_src_tup:
                box_id, src = tup.split(',')
                UserBoxPerm.objects.get_or_create(**{'user_id': user_id, 'drawer_id': box_id, 'source': src})
        return HttpResponseRedirect(reverse("user_list"))
    else:
        normal_user_list = User.objects.filter(role=1)
        return render(request, 'user_sync_perm.html', {
            'user_list': normal_user_list
        })


def show_personal_perm(request):
    if request.method == 'GET':
        uid = request.GET.get('uid')
        local_user = User.objects.filter(id=uid).first()
        now_user_perms = UserBoxPerm.objects.filter(user_id=uid).order_by('source')
        user_perm_tag = False
        for user_perm in now_user_perms:
            src_cls = UserBoxPerm.get_src_cls(user_perm.source)
            try:
                user_perm.box = src_cls.objects.get(id=user_perm.drawer_id, is_delete=0)
                user_perm_tag = True
            except src_cls.DoesNotExist:
                UserBoxPerm.objects.filter(user_id=uid, drawer_id=user_perm.drawer_id, source=user_perm.source).delete()
                user_perm.box = None
        return render(request, 'show_personal_perm.html', {
            'now_user_perms': now_user_perms,
            'local_user': local_user,
            'user_perm_tag': user_perm_tag,
        })