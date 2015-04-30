# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from content.models import IpadChannel, IpadSubChannel,IpadSubChannelItem,IpadSubChannelModule, VideoType, SyncJob, Status,IpadFixedPositionVideo,SubChannelType,IpadSubChannelModuleItem
from content.views.common import redefine_item_pos, set_position


@login_required
def fixed_position_videos(request):
        channel_id = request.GET.get('channel_id', '')
        subchannel_id = request.GET.get('subchannel_id', '')
        module_id = request.GET.get('module_id', '')
        channel, subchannel, module = (None,) * 3
        videos = []
        try:
            if subchannel_id and channel_id:
                channel = IpadChannel.objects.get(pk=int(channel_id),is_delete=0)
                subchannel = IpadSubChannel.objects.get(pk=int(subchannel_id),is_delete=0)
                if module_id :
                    module = IpadSubChannelModule.objects.get(pk=int(module_id),is_delete=0)
                    videos = IpadFixedPositionVideo.objects.filter(is_delete=0,module_id=int(module_id)).order_by('-updated_at')
                else:
                    videos = IpadFixedPositionVideo.objects.filter(is_delete=0,subchannel_id=int(subchannel_id)).order_by('-updated_at')

        except (IpadChannel.DoesNotExist, IpadSubChannel.DoesNotExist,):
            pass
        for index, video in enumerate(videos):
            videos[index].copyright_for_view = video.copyright_for_view()
            videos[index].pay_type_for_view = video.pay_type_for_view()
            videos[index].video_type_for_view = video.video_type_for_view()
        commit_dict = {'channel': channel,
                       'subchannel': subchannel, 'module': module,
                       'video_state_hash': Status.STATUS_HASH,
                       'videos': videos}
        return render(request, 'ipad/channel/fixed_position_videos/videos.html', commit_dict)


@login_required
def add_fixed_position_video(request, platform='ipad'):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        video = IpadFixedPositionVideo()
        if module_id:
            video.module_id = module_id
            video.subchannel_type = SubChannelType.to_i('editable_box')
        else:
            video.subchannel_type = SubChannelType.to_i('editable_video_list')
        video.subchannel_id = subchannel_id
        video.video_type = VideoType.to_i(request.POST.get("video_type") or 0)
        video_type_name = request.POST.get('video_type', '')
        video.fixed_position = request.POST.get('fixed_position',0)

        if video_type_name == 'url':
            video.add_url_type_fields(request.POST)
        else:
            video.add_video_type_fields(request.POST)
        video.channel_id = channel_id
        video.state = 0
        video.save()
        return HttpResponseRedirect(reverse('ipad_query_fixed_position_video') + "?module_id=" + module_id +
                                    "&channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&video_id=" + str(
            video.id))
    else:
        current_channel_id = request.GET.get('channel_id')
        current_subchannel_id = request.GET.get('subchannel_id')
        current_module_id = request.GET.get('module_id')
        channel, subchannel, module = (None,) * 3
        channel = IpadChannel.objects.get(pk=current_channel_id,is_delete=0)
        subchannel = IpadSubChannel.objects.get(pk=current_subchannel_id,is_delete=0)
        if current_module_id:
            module = IpadSubChannelModule.objects.get(pk=current_module_id,is_delete=0)
            video_type_list = IpadSubChannelModuleItem.video_types(mock=True)
            videos = IpadFixedPositionVideo.objects.filter(is_delete=0,module_id=int(current_module_id))
        else:
            videos = IpadFixedPositionVideo.objects.filter(is_delete=0,subchannel_id=int(current_subchannel_id)).order_by('-updated_at')
            video_type_list = IpadSubChannelItem.video_types(mock=True)
        fixed_positions = [video.fixed_position for video in videos]
        fixed_position_list = list(set(range(1,17)) - set(fixed_positions))
        return render(request, 'ipad/channel/fixed_position_videos/add_video.html', {'platform': platform,
                                                                                             'video_type_list': video_type_list,
                                                                                             'current_channel_id': current_channel_id,
                                                                                             'current_subchannel_id': current_subchannel_id,
                                                                                             'current_module_id': current_module_id,
                                                                                              'module':module,'channel':channel,'subchannel':subchannel,
                                                                                              'fixed_position_list':fixed_position_list
                                                                                              })




@login_required
def query_fixed_position_video(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    video_id = request.GET.get('video_id', '')
    video = get_object_or_404(IpadFixedPositionVideo, pk=video_id)
    video_type_name = VideoType.to_s(video.video_type)
    if module_id:
        fixed_position_videos = IpadFixedPositionVideo.objects.filter(is_delete=0,module_id=int(module_id)).exclude(id=video.id)
        module = IpadSubChannelModule.objects.get(pk=module_id, is_delete=0)
        s_image_tag = int(module.is_headline_module)
    else:
        s_image_tag = 0
        fixed_position_videos = IpadFixedPositionVideo.objects.filter(is_delete=0,subchannel_id=int(subchannel_id)).exclude(id=video.id)
    h_image_desc = '448x252'
    v_image_desc = '200x300'
    s_image_desc = '720x194'
    fixed_positions = [fixed_position_video.fixed_position for fixed_position_video in fixed_position_videos]
    fixed_position_list = list(set(range(1,17)) - set(fixed_positions))
    args = {
        's_image_tag':s_image_tag,
        'h_image_desc':h_image_desc,
        'v_image_desc':v_image_desc,
        's_image_desc':s_image_desc,
        'channel_id':channel_id,
        'subchannel_id':subchannel_id,
        'module_id':module_id,
        'video':video,
        'fixed_position_list':fixed_position_list
    }
    if (video_type_name == "url"):
            return render(request, 'ipad/channel/fixed_position_videos/update_url_form_fields.html', args)
    elif video_type_name in ('video', 'show', 'playlist'):
            return render(request, 'ipad/channel/fixed_position_videos/update_video.html',args)
        # return render(request, 'subchannel_and_module_items/ipad_update_item.html',
        #               {'item': item, 'channel_id': channel_id, 'subchannel_id': subchannel_id, 'module_id': module_id})


@login_required
def update_fixed_position_video(request):
    if request.method == 'POST':
        channel_id, subchannel_id, module_id = ('',) * 3
        try:
            post_dict = request.POST.dict()
            print post_dict
            channel_id = post_dict.pop('channel_id')
            subchannel_id = post_dict.pop('subchannel_id')
            video_id = post_dict.pop('id')
            module_id = post_dict.get('module_id')
            if video_id:
                video = IpadFixedPositionVideo.objects.get(pk=video_id)
                if not module_id:
                    del post_dict['module_id']#如果传过来module_id为''数据保存报错
                for k, v in post_dict.iteritems():
                    if hasattr(video, k):
                        setattr(video, k, v)
                video.save()
        except Exception, e:
            print e
        return HttpResponseRedirect(reverse(
            'ipad_fixed_position_videos') + "?channel_id=" + channel_id + "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)


@login_required
def update_fixed_position_video_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        subchannel_id = request.GET.get('subchannel_id')
        module_id = request.GET.get('module_id')
        item = None
        if pk:
            if module_id:
                item = IpadSubChannelModuleItem.objects.get(id=int(pk))
            elif subchannel_id:
                item = IpadSubChannelItem.objects.get(id=int(pk))
            name = request.POST.get('name')
            value = request.POST.get('value')
            if hasattr(item, name):
                setattr(item, name, value)
            item.save()
            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"子频道视频不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
#从视频列表页直接修改视频的title subtitle intro 属性
#注：页面上td的id属性不要改
def update_fixed_position_video_value(request):
    if request.method == 'POST':
        video_id = request.POST.get("video_id")
        attribute = request.POST.get("attribute")
        value = request.POST.get("value")
        module_id = request.POST.get('module_id')
        if video_id and value and attribute:
            try:
                video = IpadFixedPositionVideo.objects.get(id=int(video_id))
                setattr(video, attribute, value)
                video.save()
                response = {'status': 'success', 'value': getattr(video, attribute)}
            except Exception, e:
                response = {'status': 'error', 'msg': u"修改视频失败!"}
        else:
            response = {'status': 'error', 'msg': u"模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")

@login_required
def check_fixed_position(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    value = request.GET.get("value",'')
    method = request.GET.get("method","")
    video_id = request.GET.get("video_id",'')
    if module_id:
        fixed_position_video = IpadFixedPositionVideo.objects.filter(module_id=int(module_id),is_delete=0,state=1,fixed_position=int(value))
    else:
        fixed_position_video = IpadFixedPositionVideo.objects.filter(subchannel_id=int(subchannel_id),is_delete=0,state=1,fixed_position=int(value))
    if method == 'update':
        fixed_position_video = fixed_position_video.exclude(id=video_id)
    if fixed_position_video:
        return HttpResponse('false')
    else:
        return HttpResponse('true')


@login_required
def delete_fixed_position_video(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    video_id = request.GET.get('video_id', '')
    try:
        IpadFixedPositionVideo.objects.filter(pk=video_id).update(is_delete=1)
    except (IpadSubChannelModuleItem.DoesNotExist, IpadSubChannelItem.DoesNotExist):
        pass
    return HttpResponseRedirect(reverse('ipad_fixed_position_videos') + "?channel_id=" + channel_id +
                                "&subchannel_id=" + subchannel_id + "&module_id=" + module_id)


