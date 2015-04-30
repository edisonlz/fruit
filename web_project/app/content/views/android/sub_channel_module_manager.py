# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import AndroidChannel, AndroidSubChannel, AndroidSubChannelModule, Status
from content.lib.filter_base import FilterBase
from content.views.common import redefine_item_pos, set_position
from app.content.models import AndroidSubChannelModuleTag, LINK_TO_TYPE_DICT


def get_filterinfo(cid):
    filter_info = FilterBase.order_array(
        {'cid': cid, 'platform': 'android', 'device': 'phone', 'ver': '3.7'})
    type_name = FilterBase.cid_category_value(cid)
    areas = filter(lambda x: x['cat'] == 'area', filter_info)
    years = filter(lambda x: x['cat'] == 'releaseyear', filter_info)
    video_types = filter(lambda x: x['cat'] == type_name, filter_info)
    pay_kinds = filter(lambda x: x['cat'] == 'pay_kind', filter_info)
    return map(FilterBase.list_to_dict, [areas, years, video_types, pay_kinds])


@login_required
def subchannel_modules(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            try:
                redefine_item_pos(AndroidSubChannelModule, box_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel', '')
        subchannel_id = request.GET.get('select_subchannel', '')
        channels = AndroidChannel.objects.filter(is_delete=0).order_by("-position")
        areas, years, video_types, pay_kinds, channel, subchannel = (None,) * 6
        subchannels, modules = ([],) * 2
        try:
            if channels and len(channels) > 0:
                channel = AndroidChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
                subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = AndroidSubChannel.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id else \
                    subchannels[0]
                modules = subchannel.module.filter(is_delete=0).order_by('-position')
            areas, years, video_types, pay_kinds = get_filterinfo(channel.cid)

        except (AndroidChannel.DoesNotExist, AndroidSubChannel.DoesNotExist):
            pass
        exist_subchannels = AndroidSubChannel.objects.filter(is_delete=False,channel_id=channel_id).defer('id', 'title')
        subchannel_box_types_hash = AndroidSubChannelModule.get_subchannel_box_types(channel)
        subchannel_box_types = subchannel_box_types_hash.items()
        return render(request, 'android/channel/sub_channel_box/subchannel_boxes.html', {
            'subchannels': subchannels, 'channels': channels, 'this_channel': channel,
            'this_subchannel': subchannel, 'modules': modules, 'jump_channels': exist_subchannels,
            'areas': areas, 'video_types': video_types, 'years': years, 'pay_kinds': pay_kinds,
            'box_types': subchannel_box_types,
            'subchannel_box_types_hash': subchannel_box_types_hash, 'module_state_hash': Status.STATUS_HASH,
        })


@require_POST
@login_required
def add_subchannel_module(request):
    post_dict = request.POST.dict()
    channel_id = post_dict.pop('channel_id')
    subchannel_id = post_dict.get('subchannel_id', '')
    unit_count = post_dict.pop('count')
    unit_list = []
    for i in xrange(1, int(unit_count) + 1):
        unit_list.append(post_dict.get('unit_type_div_%s' % i))
    add_dict = {'unit_type_collection': ','.join(unit_list)}
    type_name = FilterBase.cid_category_value(int(post_dict.get('cid')))
    if post_dict.get('jump_type') == 'by_filter':
        tmp_str = ''
        for key in ['area', type_name, 'releaseyear', 'pay_kind']:
            tmp_str += '%s:%s;' % (key, post_dict.get(key))
        add_dict['filter_for_link'] = tmp_str[:-1]
    elif post_dict.get('jump_type') == 'by_sub_channel':
        add_dict['sub_channel_id_for_link'] = post_dict.get('sub_channel_id_for_link')

    for k in ['module_type', 'title', 'jump_type', 'subchannel_id']:
        add_dict[k] = post_dict.get(k)
    module = AndroidSubChannelModule()
    set_position(module, AndroidSubChannelModule, {'subchannel_id': subchannel_id})
    for k, v in add_dict.iteritems():
        if hasattr(module, k):
            setattr(module, k, v)
    module.save()
    return HttpResponseRedirect(reverse('android_sub_channel_modules') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id)


@login_required
def query_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    subchannel_module_types_hash = AndroidSubChannelModule.MODULE_TYPES
    module = get_object_or_404(AndroidSubChannelModule, pk=module_id)
    module.unit_type_divs = module.unit_type_collection.split(',')
    module.unit_count = len(module.unit_type_divs)
    exist_subchannels = AndroidSubChannel.objects.defer('id', 'title')
    channel = AndroidChannel.objects.get(pk=channel_id)
    areas, years, video_types, pay_kinds = get_filterinfo(channel.cid)
    filter_dict = {}
    has_tag = 0
    if channel.is_game_channel:
        if not module.is_headline_module:
            has_tag = 1
    if module.filter_for_link:
        sections = module.filter_for_link.split(';')
        filter_list = []
        for section in sections:
            k, v = section.split(':')
            filter_list.append((k, v))
        filter_dict = {'filter': filter_list}
    origin_dict = {'module': module, 'channel_id': channel_id, 'subchannel_id': subchannel_id,
                   'jump_channels': exist_subchannels, 'areas': areas, 'video_types': video_types, 'years': years,
                   'pay_kinds': pay_kinds, 'module_type_hash': subchannel_module_types_hash,'has_tag':has_tag}
    if filter_dict:
        origin_dict.update(filter_dict)
    origin_dict['link_types'] = LINK_TO_TYPE_DICT
    origin_dict['link_tags'] = module.tag.filter(is_delete=False).order_by('-position')
    return render(request, 'android/channel/sub_channel_box/update_subchannel_box.html', origin_dict)


@login_required
def update_subchannel_module(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        channel_id = post_dict.pop('channel_id')
        unit_count = post_dict.pop('count')
        module = AndroidSubChannelModule.objects.get(pk=post_dict.pop('module_id'))
        unit_list = []
        for i in xrange(1, int(unit_count) + 1):
            unit_list.append(post_dict.get('unit_select_%s' % i))
        add_dict = {'unit_type_collection': ','.join(unit_list)}
        channel = AndroidChannel.objects.get(pk=channel_id)
        type_name = FilterBase.cid_category_value(channel.cid)
        jump_type = add_dict['jump_type'] = post_dict['jump_type']
        if jump_type == 'by_filter':
            filter_list = [u'area', unicode(type_name), u'releaseyear', u'pay_kind']
            unit_list = [u'%s:%s' % (key, post_dict[key]) for key in filter_list]
            add_dict['filter_for_link'] = u';'.join(unit_list)
        elif jump_type == 'by_sub_channel':
            add_dict['sub_channel_id_for_link'] = post_dict.get('sub_channel_id_for_link')
        add_dict['title'] = post_dict.get('title')
        add_dict['slider_video_count'] = post_dict.get('slider_video_count',5)

        for k, v in add_dict.iteritems():
            if hasattr(module, k):
                setattr(module, k, v)
        module.save()
        return HttpResponseRedirect(reverse('android_sub_channel_modules') + "?select_channel=" + channel_id +
                                    "&select_subchannel=" + post_dict.get('subchannel_id', ''))


@login_required
def update_subchannel_module_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            module = get_object_or_404(AndroidSubChannelModule, pk=pk)
            name = request.POST.get('name')
            value = request.POST.get('value')
            if hasattr(module, name):
                setattr(module, name, value)
            module.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        AndroidSubChannelModule.objects.filter(pk=module_id).update(is_delete=1)
    except AndroidSubChannelModule.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('android_sub_channel_modules') + "?select_channel=" + channel_id +
                                "&select_subchannel=" + subchannel_id)


@login_required
def android_add_tag(request):
    module_id = request.POST.get('module_id')
    tag_title = request.POST.get('tag_title')
    link_to_select = request.POST.get('link_to_select')
    try:
        tag = AndroidSubChannelModuleTag.objects.create(module_id=module_id, jump_type='game_page', link_to=link_to_select,
                                                        title=tag_title, is_delete=False)
        ret = {
            'id': tag.id,
            'status': 'success',
            'module_id': tag.module_id,
            'tag_title': tag.title,
            'link_to_select': tag.link_to
        }
    except:
        ret = {'status': 'failed'}
    return HttpResponse(json.dumps(ret), content_type='application/json')


@login_required
def android_delete_tag(request):
    pk = request.POST.get('pk')
    try:
        AndroidSubChannelModuleTag.objects.filter(pk=pk).update(is_delete=True)
        ret = {'status': 'success'}
    except:
        ret = {'status': 'failed'}
    return HttpResponse(json.dumps(ret), content_type='application/json')


@login_required
def android_sort_tag(request):
    tag_ids = request.POST.get('tag_ids')
    ret = {}
    if tag_ids:
        try:
            redefine_item_pos(AndroidSubChannelModuleTag, tag_ids)
            ret = {'status': 'success'}
        except Exception, e:
            ret = {'status': 'error'}
    return HttpResponse(json.dumps(ret), content_type='application/json')

