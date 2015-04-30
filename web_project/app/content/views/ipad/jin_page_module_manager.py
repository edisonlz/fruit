#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import json
from app.content.models import Platform, Status
from app.content.models import IpadChannel, IpadSubChannel, IpadSubChannelModule, JinPage


@login_required
def jinpage_modules(request):
     platform = Platform.get_platform(request.path)

     if request.method == 'POST':
         channel_id = request.POST.get('this_channel_id')
         item_ids = request.POST.get('item_ids')
         position = 1
         for item_id in item_ids.split(','):
             item = IpadSubChannelModule.objects.get(id=item_id)
             item.position = position
             position += 1
             item.save()

     # if request.method == 'POST':
     #    item_ids = request.POST.get('item_ids')
     #    channel_id = request.POST.get('this_channel_id')
     #    subchannel_id = request.POST.get('this_subchannel_id')
     #    position = 1
     #    for item_id in item_ids.split(','):
     #        item = IpadSubChannelModule.objects.get(id=item_id)
     #        item.position = position
     #        position += 1
     #        item.save()

        # return HttpResponseRedirect(reverse('ipad_sub_channel_modules') + "?select_channel=" + channel_id + "&select_subchannel=" + subchannel_id)
     else:
        #GET Come here
        channel_id = request.GET.get('select_channel', '')
        # subchannel_id = request.GET.get('select_subchannel', '')
        # channels = IpadChannel.objects.filter(platform=platform, switch_jin=1).order_by("position")
        channels = IpadChannel.objects.filter(platform=platform).order_by("position")
        channel = None
        modules = []

        if channels and len(channels) > 0:
            channel = IpadChannel.objects.get(pk=channel_id) if channel_id else channels[0]
            print channel.__dict__
            # subchannels = channel.subchannel.filter(type=1).order_by('position')
            modules = channel.jin_module.order_by('position')
            # modules = JinPage.objects.get(pk=channel.id)

        # if subchannels and len(subchannels) > 0:
        #     subchannel = IpadSubChannel.objects.get(pk=subchannel_id) if subchannel_id else subchannels[0]
        #     modules = subchannel.module.order_by('position')



        return render(request, 'jinpage_module/jinpage_modules.html',
                      {'channels': channels, 'this_channel': channel,
                    'modules': modules})


@login_required
def add_jinpage_modules(request):

    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        # subchannel_id = request.POST.get('subchannel_id', '')
        title = request.POST.get('title', '')
        num = request.POST.get('count', 10)
        cid = request.POST.get('cid')
        jinpageModule = JinPage()
        jinpageModule.title = title
        jinpageModule.channel_id = channel_id
        jinpageModule.nums = num
        jinpageModule.cid = cid
        jinpageModule.save()
        return HttpResponseRedirect(reverse('ipad_jin_page_module') + "?select_channel=" +channel_id)


@login_required
def query_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    channel_id = request.GET.get("channel_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    module = get_object_or_404(IpadSubChannelModule, pk=module_id)
    return render(request, 'subchannel_module/ipad_update_subchannel_module.html', {'module': module, 'channel_id': channel_id, 'subchannel_id': subchannel_id})


@login_required
def update_subchannel_module(request):
    if request.method == 'POST':
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        module_id = request.POST.get('module_id', '')
        title = request.POST.get('title', '')
        num = request.POST.get('count', '')
        print num
        # IpadSubChannelModule.objects.filter(id=module_id).update(
        #     title=title, video_count=num
        # )

        return HttpResponseRedirect(reverse('ipad_sub_channel_modules') + "?select_channel=" +channel_id + "&select_subchannel=" +subchannel_id)

    return render(request, 'subchannel_module/ipad_update_subchannel_module.html')


@login_required
def update_jinpage_module_status(request):
    if request.method == 'POST':
        pk = request.POST.get("pk")
        if pk:
            mi = JinPage.objects.get(id=int(pk))
            mi.state = int(request.POST.get("value"))
            mi.save()

            response = {'status': 'success'}
        else:
            response = {'status': 'error', 'msg': u"精选页模块不存在!"}
    else:
        response = {'status': 'error', 'msg': u"仅支持POST!"}

    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def delete_subchannel_module(request):
    module_id = request.GET.get("module_id", '')
    subchannel_id = request.GET.get("subchannel_id", '')
    channel_id = request.GET.get("channel_id", '')
    IpadSubChannelModule.objects.get(pk=module_id).delete()
    return HttpResponseRedirect(reverse('ipad_sub_channel_modules') + "?select_channel=" + channel_id +"&select_subchannel="+subchannel_id)
