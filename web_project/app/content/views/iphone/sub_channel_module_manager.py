# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import IphoneChannel, IphoneSubChannel, IphoneSubChannelModuleV4, IphoneSubChannelModule
from content.views.common import redefine_item_pos, set_position


@login_required
def subchannel_modules_v4(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        channel_id = request.POST.get('this_channel_id')
        subchannel_id = request.POST.get('this_subchannel_id')
        if item_ids:
            redefine_item_pos(IphoneSubChannelModuleV4, item_ids)
        return HttpResponseRedirect(reverse(
            'iphone_sub_channel_modules_v4') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id)
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        channels = IphoneChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel = (None,) * 2
        modules, subchannels = ([],) * 2
        try:
            if channels and len(channels) > 0:
                channel = IphoneChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
                subchannels = channel.subchannel.filter(type=1, is_choiceness=1, is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = IphoneSubChannel.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id else subchannels[0]
                modules = subchannel.module_v4.filter(is_delete=0).order_by('-position')
        except:
            pass
        return render(request, 'subchannel_module/iphone_subchannel_modules_v4.html',
                      {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules})


@login_required
def add_subchannel_module_v4(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        unit_list = []
        channel_id = ''
        subchannel_id = request.POST.get('subchannel_id', '')
        try:
            channel_id = post_dict.pop('channel_id', '')
            for i in xrange(1, int(post_dict.pop('count')) + 1):
                unit_list.append(request.POST.get("unit_type_div_%s" % i, ''))
                post_dict.pop("unit_type_div_%s" % i)
            module = IphoneSubChannelModuleV4()
            set_position(module, IphoneSubChannelModuleV4, {'subchannel_id': subchannel_id})
            module.unit_type_collection = ','.join(unit_list)
            for k, v in post_dict.iteritems():
                if hasattr(module, k):
                    setattr(module, k, v)
            module.save()
        except KeyError:
            pass
        finally:
            return HttpResponseRedirect(reverse('iphone_sub_channel_modules_v4') + "?select_channel=" + channel_id +
                                        "&select_subchannel=" + subchannel_id)


@login_required
def query_subchannel_module_v4(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    module = get_object_or_404(IphoneSubChannelModuleV4, pk=module_id)
    if module.module_type == 0:
        module.unit_type_divs = module.unit_type_collection.split(',')
        module.unit_count = len(module.unit_type_divs)
        while len(module.unit_type_divs) < 6:
            module.unit_type_divs.append(u'')
    return render(request, 'subchannel_module/iphone_update_subchannel_module_v4.html',
                  {'module': module, 'channel_id': channel_id, 'subchannel_id': subchannel_id})


@login_required
def update_subchannel_module_v4(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        module_type = request.POST.get('module_type')
        add_dict = {'title': request.POST.get('title' '')}
        if module_type == '1':
            add_dict['slider_video_count'] = request.POST.get('slider_video_count', '')
        else:
            count = request.POST.get('count', 0)
            unit_list = []
            for i in xrange(1, int(count) + 1):
                unit_list.append(request.POST.get("unit_select_%s" % i, ''))
            add_dict['unit_type_collection'] = ','.join(unit_list)
        IphoneSubChannelModuleV4.objects.filter(id=module_id).update(**add_dict)
        return HttpResponseRedirect(reverse('iphone_sub_channel_modules_v4') + "?select_channel=" + channel_id +
                                    "&select_subchannel=" + subchannel_id)

    return render(request, 'subchannel_module/iphone_update_subchannel_module_v4.html')


@login_required
def update_subchannel_module_status_v4(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            mi = IphoneSubChannelModuleV4.objects.get(id=int(pk))
            mi.state = int(request.POST.get("value"))
            mi.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module_v4(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        IphoneSubChannelModuleV4.objects.filter(pk=module_id).update(is_delete=1)
    except IphoneSubChannelModuleV4.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('iphone_sub_channel_modules_v4') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id)


@login_required
def subchannel_modules(request):
    if request.method == 'POST':
        item_ids = request.POST.get('item_ids')
        if item_ids:
            try:
                redefine_item_pos(IphoneSubChannelModule, item_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        channels = IphoneChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannel = (None,) * 2
        subchannels, modules = ([],) * 2
        try:
            if channels and len(channels) > 0:
                channel = IphoneChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
                subchannels = channel.subchannel.filter(type=1, is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = IphoneSubChannel.objects.get(type=1, is_delete=0, pk=subchannel_id) if subchannel_id else subchannels[0]
                modules = subchannel.module.filter(is_delete=0).order_by('-position')
        except IphoneChannel.DoesNotExist, IphoneSubChannel.DoesNotExist:
            pass

        return render(request, 'subchannel_module/iphone_subchannel_modules.html',
                      {'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
                       'this_subchannel': subchannel, 'modules': modules, 'alpha': ['a', 'c', 'b']})


@require_POST
@login_required
def add_subchannel_module(request):
    post_dict = request.POST.dict()
    module = IphoneSubChannelModule()
    set_position(module, IphoneSubChannelModule)
    channel_id = post_dict.pop('channel_id')
    for k, v in post_dict.iteritems():
        if hasattr(module, k):
            setattr(module, k, v)
    module.save()
    return HttpResponseRedirect(reverse('iphone_sub_channel_modules') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + post_dict.get('subchannel_id', ''))


@login_required
def delete_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        IphoneSubChannelModule.objects.filter(pk=module_id).update(is_delete=1)
    except IphoneSubChannelModule.DoesNotExist:
        pass
    return HttpResponseRedirect(
        reverse('iphone_sub_channel_modules') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id)


@login_required
def query_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    module = get_object_or_404(IphoneSubChannelModule, pk=module_id)
    return render(request, 'subchannel_module/iphone_update_subchannel_module.html',
                  {'module': module, 'channel_id': channel_id, 'subchannel_id': subchannel_id})


@login_required
def update_subchannel_module(request):
    if request.method == 'POST':
        try:
            post_dict = request.POST.dict()
            channel_id = post_dict.pop('channel_id')
            module = IphoneSubChannelModule.objects.get(pk=post_dict.pop('id'))
            for k, v in post_dict.iteritems():
                if hasattr(module, k):
                    setattr(module, k, v)
            module.save()
            return HttpResponseRedirect(reverse('iphone_sub_channel_modules') + "?select_channel=" + channel_id +
                                        "&select_subchannel=" + post_dict.get('subchannel_id'))
        except KeyError, IphoneSubChannelModule.DoesNotExist:
            pass

    return render(request, 'subchannel_module/iphone_update_subchannel_module.html')


@login_required
def update_subchannel_module_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            mi = get_object_or_404(IphoneSubChannelModule, pk=pk)
            name = request.POST.get('name')
            value = request.POST.get('value')
            if hasattr(mi, name):
                setattr(mi, name, value)
            mi.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")