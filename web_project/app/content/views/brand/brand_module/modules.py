# coding=utf-8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from app.content.views.common import redefine_item_pos, set_position
from app.content.models import Status
from app.content.models import AndroidChannel, IphoneChannel, IpadChannel
from app.content.models import AndroidSubChannel, IphoneSubChannel, IpadSubChannel
from app.content.models import BrandModule
import json
from django.shortcuts import render
from wi_model_util.imodel import get_object_or_none


def modules(request):
    android_sub_channels = []
    iphone_sub_channels = []
    ipad_sub_channels = []
    android_channels = AndroidChannel.objects.filter(is_delete=0)
    iphone_channels = IphoneChannel.objects.filter(is_delete=0)
    ipad_channels = IpadChannel.objects.filter(is_delete=0)
    initial_android_channel_id = 0
    initial_android_sub_channel_id = 0
    initial_iphone_channel_id = 0
    initial_iphone_sub_channel_id = 0
    initial_ipad_channel_id = 0
    initial_ipad_sub_channel_id = 0
    if android_channels:
        initial_android_channel = android_channels[0]
        android_sub_channels = AndroidSubChannel.objects.filter(is_delete=0, channel_id=initial_android_channel.id)
        initial_android_channel_id = initial_android_channel.id
        if android_sub_channels:
            initial_android_sub_channel_id = android_sub_channels[0].id
    else:
        android_sub_channels = []
    if iphone_channels:
        initial_iphone_channel = iphone_channels[0]
        iphone_sub_channels = IphoneSubChannel.objects.filter(is_delete=0, channel_id=initial_iphone_channel.id)
        initial_iphone_channel_id = initial_iphone_channel.id
        if iphone_sub_channels:
            initial_iphone_sub_channel_id = iphone_sub_channels[0].id
    else:
        iphone_sub_channels = []
    if ipad_channels:
        initial_ipad_channel = ipad_channels[0]
        ipad_sub_channels = IpadSubChannel.objects.filter(is_delete=0, channel_id=initial_ipad_channel.id)
        initial_ipad_channel_id = initial_ipad_channel.id
        if ipad_sub_channels:
            initial_ipad_sub_channel_id = ipad_sub_channels[0]
    else:
        ipad_sub_channels = []
    state_dict = Status.STATUS_HASH
    modules = BrandModule.objects.filter(is_delete=0)
    #临时添加一个属性,投放到各平台的各个位置
    modules = add_placement_position_for_modules(modules)

    return render(request, "brand/modules/modules.html", {
        "android_channels": android_channels,
        "iphone_channels": iphone_channels,
        "ipad_channels": ipad_channels,
        "android_sub_channels": android_sub_channels,
        "iphone_sub_channels": iphone_sub_channels,
        "ipad_sub_channels": ipad_sub_channels,
        "state_dict": state_dict,
        "modules": modules,
        "initial_android_channel_id": initial_android_channel_id,
        "initial_android_sub_channel_id": initial_android_sub_channel_id,
        "initial_iphone_channel_id": initial_iphone_channel_id,
        "initial_iphone_sub_channel_id": initial_iphone_sub_channel_id,
        "initial_ipad_channel_id": initial_ipad_channel_id,
        "initial_ipad_sub_channel_id": initial_ipad_sub_channel_id
    })


def add_module(request, ):
    if request.method == 'POST':
        module = BrandModule()
        module.title = request.POST.get("title", "")
        module.link_to_url = request.POST.get("link_to_url", "")
        module.state_for_android = int(request.POST.get("state_for_android", 0))
        module.state_for_iphone = int(request.POST.get("state_for_iphone", 0))
        module.state_for_ipad = int(request.POST.get("state_for_ipad", 0))
        module.subchannel_id_of_android = int(request.POST.get("subchannel_id_of_android", 0))
        module.subchannel_id_of_iphone = int(request.POST.get("subchannel_id_of_iphone", 0))
        module.subchannel_id_of_ipad = int(request.POST.get("subchannel_id_of_ipad", 0))
        module.save()
        return HttpResponseRedirect(reverse("brand_modules"))
    else:
        return render(request, "brand/modules/add_module.html")


def select_channel(request, ):
    platform = request.POST.get("platform")
    channel_pk = request.POST.get("selected_channel_id")
    sub_channels = []
    if platform == "android":
        sub_channels = AndroidSubChannel.objects.filter(channel_id=channel_pk)
    elif platform == "iphone":
        sub_channels = IphoneSubChannel.objects.filter(channel_id=channel_pk)
    elif platform == "ipad":
        sub_channels = IpadSubChannel.objects.filter(channel_id=channel_pk)
    options = ""
    for sub_channel in sub_channels:
        options += "<option value=\"" + str(
            sub_channel.id) + "\">" + sub_channel.title + "(" + transform_state_number_to_Chinese(
            sub_channel.state) + ")</option>"
    response = {"replace_options": options}
    return HttpResponse(json.dumps(response), content_type="application/json")


def update_module(request, module_pk):
    module = get_object_or_none(BrandModule, pk=module_pk)
    if request.method == "POST":
        module.title = request.POST.get("title", "")
        module.link_to_url = request.POST.get("link_to_url", "")
        module.state_for_android = int(request.POST.get("state_for_android", 0))
        module.state_for_iphone = int(request.POST.get("state_for_iphone", 0))
        module.state_for_ipad = int(request.POST.get("state_for_ipad", 0))
        module.subchannel_id_of_android = int(request.POST.get("subchannel_id_of_android", 0))
        module.subchannel_id_of_iphone = int(request.POST.get("subchannel_id_of_iphone", 0))
        module.subchannel_id_of_ipad = int(request.POST.get("subchannel_id_of_ipad", 0))
        module.save()
        return HttpResponseRedirect(reverse("brand_modules"))
    else:
        selected_android_sub_channel = None
        selected_iphone_sub_channel = None
        selected_ipad_sub_channel = None
        selected_android_channel = None
        selected_iphone_channel = None
        selected_ipad_channel = None
        android_channels = AndroidChannel.objects.filter(is_delete=0)
        iphone_channels = IphoneChannel.objects.filter(is_delete=0)
        ipad_channels = IpadChannel.objects.filter(is_delete=0)
        android_sub_channels_of_selected_channel = None
        iphone_sub_channels_of_selected_channel = None
        ipad_sub_channels_of_selected_channel = None

        if module.subchannel_id_of_android:
            selected_android_sub_channel = get_object_or_none(AndroidSubChannel, pk=module.subchannel_id_of_android)
            selected_android_channel = get_object_or_none(AndroidChannel, pk=selected_android_sub_channel.channel_id)
            android_sub_channels_of_selected_channel = AndroidSubChannel.objects.filter(
                channel_id=selected_android_channel.id)

        if module.subchannel_id_of_iphone:
            selected_iphone_sub_channel = get_object_or_none(IphoneSubChannel, pk=module.subchannel_id_of_iphone)
            selected_iphone_channel = get_object_or_none(IphoneChannel, pk=selected_iphone_sub_channel.channel_id)
            iphone_sub_channels_of_selected_channel = IphoneSubChannel.objects.filter(
                channel_id=selected_iphone_channel.id)

        if module.subchannel_id_of_ipad:
            selected_ipad_sub_channel = get_object_or_none(IpadSubChannel, pk=module.subchannel_id_of_ipad)
            selected_ipad_channel = get_object_or_none(IpadChannel, pk=selected_ipad_sub_channel.channel_id)
            ipad_sub_channels_of_selected_channel = IpadSubChannel.objects.filter(channel_id=selected_ipad_channel.id)

        return render(request, "brand/modules/update_module.html", {
            "module": module,
            "android_channels": android_channels,
            "iphone_channels": iphone_channels,
            "ipad_channels": ipad_channels,
            "selected_android_sub_channel": selected_android_sub_channel,
            "selected_iphone_sub_channel": selected_iphone_sub_channel,
            "selected_ipad_sub_channel": selected_ipad_sub_channel,
            "selected_android_channel": selected_android_channel,
            "selected_iphone_channel": selected_iphone_channel,
            "selected_ipad_channel": selected_ipad_channel,
            "android_sub_channels_of_selected_channel": android_sub_channels_of_selected_channel,
            "iphone_sub_channels_of_selected_channel": iphone_sub_channels_of_selected_channel,
            "ipad_sub_channels_of_selected_channel": ipad_sub_channels_of_selected_channel,
            "state_dict": Status.STATUS_HASH
        })


def delete_module(request, module_pk):
    module = get_object_or_none(BrandModule, pk=module_pk)
    module.is_delete = 1
    module.save()
    return HttpResponseRedirect(reverse("brand_modules"))


def transform_state_number_to_Chinese(state):
    if state == 0:
        return "关闭"
    elif state == 1:
        return "开启"
    else:
        return "unknown"


def add_placement_position_for_modules(modules):
    for module in modules:
        module.android_place_position = module.placement_position_for_view('android', AndroidChannel, AndroidSubChannel)
        module.iphone_place_position = module.placement_position_for_view('iphone', IphoneChannel, IphoneSubChannel)
        module.ipad_place_position = module.placement_position_for_view('ipad', IpadChannel, IpadSubChannel)
    return modules

