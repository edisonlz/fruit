# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import IpadSubChannel, IpadChannel, SubChannelType, Status
from app.content.lib.filter_base import FilterBase
from app.content.views.common import redefine_item_pos, set_position
from app.content.lib.channel_page_publish_tool import ChannelPagePublishTool


@login_required
def subchannels(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            try:
                redefine_item_pos(IpadSubChannel, box_ids)
                response = {'status': 'success'}
            except Exception, e:
                response = {'status': 'error'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel')
        channels = IpadChannel.objects.filter(is_delete=0).order_by("-position")
        channel, subchannels = None, []
        if channels and len(channels) > 0:
            channel = IpadChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
        filter_params = {'cid': channel.cid, 'platform': 'ios', 'device': 'pad', 'ver': '9.9'}
        filter_list = FilterBase.filter_of_channel(filter_params)
        subchannel_type_hash = {item['id']: item['desc'] for item in SubChannelType.KEYS}
        subchannel_type_list = subchannel_type_hash.items()
        return render(request, 'subchannel/ipad_subchannels.html', {
            'subchannels': subchannels, 'channels': channels,
            'this_channel': channel, 'filter_list': filter_list,
            'subchannel_state_hash': Status.STATUS_HASH,
            'subchannel_type_list': subchannel_type_list
        })


@require_POST
@login_required
def add_subchannel(request):
    post_dict = request.POST.dict()
    channel_id = post_dict.get('channel_id', '')
    filter_collection = None
    #精选子频道只能是抽屉类型
    if post_dict['is_choiceness'] == '1':
        post_dict['type'] = '1'
    # 如果是‘筛选条件’类型'
    if post_dict['type'] == '3':
        filter_kinds = []
        for k, v in post_dict.items():
            if k.startswith('filter_'):
                filter_kinds.append(k)
        filter_unit_list = [u'%s:%s' % (key.replace('filter_', ''), post_dict[key]) for key in filter_kinds]
        filter_collection = u'|'.join(filter_unit_list)
    sub_channel = IpadSubChannel()
    set_position(sub_channel, IpadSubChannel, {'channel_id': channel_id})
    sub_channel.filter_collection = filter_collection if filter_collection else ''
    for k, v in post_dict.iteritems():
        if hasattr(sub_channel, k):
            setattr(sub_channel, k, v)
    sub_channel.save()
    return HttpResponseRedirect(reverse('ipad_sub_channels') + "?select_channel=" + channel_id)


@login_required
def query_subchannel(request):
    child_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel = get_object_or_404(IpadSubChannel, pk=child_id)
    cid = IpadChannel.objects.get(pk=channel_id).cid
    filter_params = {'cid': cid, 'platform': 'ios', 'device': 'pad', 'ver': '9.9'}
    filter_list = FilterBase.filter_of_channel(filter_params)
    current_filter = subchannel.filter_collection_to_dict()
    for k, v in current_filter.items():
        filter_list[k]['current'] = v
    params_dic = {'subchannel': subchannel, 'channel_id': channel_id,
                  # 'areas': areas, 'video_types': video_types, 'years': years,
                  'cid': cid, 'filter_list': filter_list}
    return render(request, 'subchannel/ipad_update_subchannel.html', params_dic)


@require_POST
@login_required
def update_subchannel(request):
    if request.method == 'POST':
        try:
            post_dict = request.POST.dict()
            subchannel = IpadSubChannel.objects.get(pk=post_dict.pop('id'))
            filter_collection = None
            # 如果是‘筛选条件’类型
            if subchannel.type == 3:
                filter_kinds = []
                for k, v in post_dict.items():
                    if k.startswith('filter_'):
                        filter_kinds.append(k)
                filter_unit_list = [u'%s:%s' % (key.replace('filter_', ''), post_dict[key]) for key in filter_kinds]
                filter_collection = u'|'.join(filter_unit_list)
            subchannel.filter_collection = filter_collection if filter_collection else ''
            for k, v in post_dict.iteritems():
                if hasattr(subchannel, k):
                    setattr(subchannel, k, v)
            subchannel.save()
            return HttpResponseRedirect(reverse('ipad_sub_channels') + "?select_channel=" +
                                        request.POST.get('channel_id'))
        except IpadSubChannel.DoesNotExist:
            pass

    return render(request, 'subchannel/ipad_update_subchannel.html')


@login_required
def update_subchannel_status(request):
    if request.method == 'POST':
        channel_ids = request.POST.get("sub_channel_ids")
        channel_ids_list = channel_ids.split(",")
        value = request.POST.get("value")
        current_channel = get_object_or_404(IpadChannel, pk=int(request.POST.get('current_channel_id'),0))
        subchannels = IpadSubChannel.objects.filter(is_delete=0, state=1, channel_id = current_channel.id)
        print "current_channel:---",
        if current_channel.for_sale == 1 and int(value) == 1:#是营销频道,并且是“开启”
            if len(channel_ids_list) > 1:#同时开启多个
                response = {"status": 'error', 'msg': '营销频道的子频道只能开启一个！'}
                return HttpResponse(json.dumps(response), content_type="application/json")
            elif len(channel_ids_list) == 1 and len(subchannels) > 0 and subchannels[0].id != int(channel_ids):#逐个开启
                response = {"status": 'error', 'msg': '营销频道的子频道只能开启一个！'}
                return HttpResponse(json.dumps(response), content_type="application/json")

        try:
            if channel_ids and value:
                id_list = channel_ids.split(',')
                obj_set = IpadSubChannel.objects.filter(id__in=id_list)
                if obj_set:
                    obj_set.update(state=value)
                    response = {'status': 'success', 'channel_ids': id_list}
                else:
                    raise IpadSubChannel.DoesNotExist
            else:
                raise ValueError('subchannel_ids or value is invalid!')
        except (IpadSubChannel.DoesNotExist, ValueError):
                response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel(request, ):
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        IpadSubChannel.objects.filter(pk=subchannel_id).update(is_delete=1)
    except IpadChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('ipad_sub_channels') + "?select_channel=" + channel_id)


@login_required
def sub_channel_publish(request):
    if request.method == 'POST':
        subchannel_ids = request.POST.get('subchannel_ids').split(',')
        ret = ChannelPagePublishTool.sub_channels_publish(sub_channel_ids=subchannel_ids, platform='ipad')
        if ret['status'] == 'publish_success':
            response = {'status': 'success'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pass

