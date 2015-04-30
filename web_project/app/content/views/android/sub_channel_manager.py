# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import AndroidSubChannel, AndroidChannel,Status,SubChannelType
from content.lib.filter_base import FilterBase
from content.views.common import redefine_item_pos, set_position
from content.lib.channel_page_publish_tool import ChannelPagePublishTool


@login_required
def subchannels(request):
    if request.method == 'POST':
        box_ids = request.POST.get('item_ids')
        if box_ids:
            try:
                redefine_item_pos(AndroidSubChannel, box_ids)
                response = {'status':'success'}
            except Exception,e:
                response = {'status':'error'}
        else:
            response = {'status':'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        channel_id = request.GET.get('select_channel')
        channels = AndroidChannel.objects.filter(is_delete=0).order_by("-position")
        channel = None
        subchannels = []
        if channels and len(channels) > 0:
            channel = AndroidChannel.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
        filter_params = {'cid':channel.cid, 'platform':'android', 'device':'phone', 'ver':'9.9'}
        filter_list = FilterBase.filter_of_channel(filter_params)
        navigation_list = ["频道管理", "Android频道",channel.title + '-子频道列表']
        subchannnel_type_hash = {item['id']:item['desc'] for item in SubChannelType.KEYS}
        subchannel_type_list = subchannnel_type_hash.items()
        return render(request, 'android/channel/sub_channel/subchannels.html', {'subchannels': subchannels, 'channels': channels,
                                                                       'this_channel': channel,'filter_list': filter_list ,
                                                                       'navigation_list': enumerate(navigation_list),
                                                                       'subchannel_state_hash': Status.STATUS_HASH,
                                                                       'subchannel_type_list': subchannel_type_list
        })


@login_required
def add_subchannel(request):
    if request.method == 'POST':
        post_dict = request.POST.dict()
        print post_dict
        channel_id = post_dict.get('channel_id', '')
        filter_collection = None
        # 如果是‘筛选条件’类型
        if post_dict['type']== '3':
            if post_dict['is_show_filters'] == '1': #露出筛选条件
                post_dict['is_show_filters'] = True
                filter_collection = ''
            else:
                filter_kinds = []
                post_dict['is_show_filters'] = False
                for k,v in post_dict.items():
                    if k.startswith('filter_'):
                        filter_kinds.append(k)
                filter_unit_list = [u'%s:%s' % (key.replace('filter_',''), post_dict[key]) for key in filter_kinds]
                filter_collection = u'|'.join(filter_unit_list)
        subchannel = AndroidSubChannel()
        set_position(subchannel, AndroidSubChannel, {'channel_id': channel_id})
        subchannel.filter_collection = filter_collection if filter_collection else ''
        for k, v in post_dict.iteritems():
            if hasattr(subchannel, k):
                setattr(subchannel, k, v)
        subchannel.save()
        return HttpResponseRedirect(
            reverse('android_sub_channel') + "?select_channel=" + channel_id)


@login_required
def query_subchannel(request):
    child_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel = get_object_or_404(AndroidSubChannel, pk=child_id)
    cid = AndroidChannel.objects.get(pk=channel_id).cid
    subchannel_type_hash = {item['id']:item['desc'] for item in SubChannelType.KEYS}
    subchannel_type_list = subchannel_type_hash.items()
    filter_params = {'cid':cid, 'platform':'android', 'device':'phone', 'ver':'9.9'}
    filter_list = FilterBase.filter_of_channel(filter_params)
    current_filter = subchannel.filter_collection_to_dict()
    for k,v in current_filter.items():
        filter_list[k]['current'] = v
    params_dic = {'subchannel': subchannel, 'channel_id': channel_id,
                  # 'areas': areas, 'video_types': video_types, 'years': years,
                  'cid': cid, 'filter_list': filter_list,'subchannel_type_list':subchannel_type_list,
                  'subchannel_type_hash':subchannel_type_hash}
    return render(request, 'android/channel/sub_channel/update_subchannel.html', params_dic)


@login_required
def update_subchannel(request):
    if request.method == 'POST':
        try:
            post_dict = request.POST.dict()
            subchannel = AndroidSubChannel.objects.get(pk=post_dict.pop('id'))
            filter_collection = None
            # 如果是‘筛选条件’类型
            if post_dict['type']== '3':
                if post_dict['is_show_filters'] == '1': #露出筛选条件
                    post_dict['is_show_filters'] = True
                    filter_collection = ''
                else:
                    filter_kinds = []
                    post_dict['is_show_filters'] = False
                    for k,v in post_dict.items():
                        if k.startswith('filter_'):
                            filter_kinds.append(k)
                    filter_unit_list = [u'%s:%s' % (key.replace('filter_',''), post_dict[key]) for key in filter_kinds]
                    filter_collection = u'|'.join(filter_unit_list)
            subchannel.filter_collection = filter_collection if filter_collection else ''
            for k, v in post_dict.iteritems():
                if hasattr(subchannel, k):
                    setattr(subchannel, k, v)
            subchannel.save()
            return HttpResponseRedirect(
                reverse('android_sub_channel') + "?select_channel=" + request.POST.get('channel_id'))
        except AndroidSubChannel.DoesNotExist:
            pass

    return render(request, 'android/channel/sub_channel/update_subchannel.html')


@login_required
def update_subchannel_status(request):
    if request.method == 'POST':
        channel_ids = request.POST.get("sub_channel_ids")
        value = request.POST.get("value")
        if channel_ids and value is not None:
            try:
                AndroidSubChannel.objects.filter(id__in=channel_ids.split(',')).update(state=int(value))
                response = {'status': 'success', 'channel_ids': channel_ids.split(",")}
            except Exception, e:
                response = {'status': 'error', 'msg': u"视频不存在!"}
        else:
            response = {'status': 'error', 'msg': u"视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def update_subchannel_highlight(request):
    if request.method == 'POST':
        try:
            post_dict = request.POST.dict()
            subchannel = AndroidSubChannel.objects.get(pk=post_dict.pop('pk'))
            value = post_dict.get('value')
            if value == '1':
                highlighted_channels = AndroidSubChannel.objects.filter(is_delete=0,highlight=1,channel_id=subchannel.channel_id)
                if not highlighted_channels:
                    subchannel.highlight = 1
                    subchannel.save()
                    response = {'status': 'success'}
                else:
                    highlighted_channel_ids = ','.join([str(channel.id) for channel in highlighted_channels])
                    response = {'status': 'error', 'msg':'已有子频道(id:%s)高亮,请先关闭' % highlighted_channel_ids}
            else:
                subchannel.highlight = 0
                subchannel.save()
                response = {'status': 'success'}
        except AndroidSubChannel.DoesNotExist:
            response = {'status': 'error', 'msg': u"子频道不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel(request, ):
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    try:
        AndroidSubChannel.objects.filter(pk=subchannel_id).update(is_delete=1)
    except AndroidSubChannel.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('android_sub_channel') + "?select_channel=" + channel_id)


@login_required
def sub_channel_publish(request):
    if request.method == 'POST':
        subchannel_ids = request.POST.get('subchannel_ids').split(',')
        ret = ChannelPagePublishTool.sub_channels_publish(sub_channel_ids=subchannel_ids, platform='android')
        if ret['status'] == 'publish_success':
            response = {'status': 'success'}
        else:
            response = {'status': 'error'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        pass