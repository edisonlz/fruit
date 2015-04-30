#coding=utf-8
from django.contrib.auth.decorators import login_required
import json
from django.shortcuts import HttpResponse
from django.views.decorators.http import require_POST
from app.content.models import HomeBox, IphoneBoxVideo
from django.template.loader import get_template
from django.template import Context
from content.models import Platform


@login_required
@require_POST
def iphone_preview(request):
    box_id = int(request.POST.get('box_id'))
    block_item_nums = 6
    content_list = []
    slider_list = []
    modules = HomeBox.objects.filter(platform=Platform.to_i('iphone'), is_delete=0, state=1).order_by('position')
    for module in modules:
        if module.box_type == 2:
            display_item = {'title': module.title, 'module_id': module.pk}
            videos = module.iphoneboxvideo_set.filter(state=1, is_delete=0).order_by('-position')
            display_item['videos'] = videos[:5]
            display_item['len'] = 5 - len(display_item['videos'])
            slider_list = display_item
        elif module.box_type == 1:
            display_item = {'title': module.title, 'module_id': module.pk}
            videos = module.iphoneboxvideo_set.filter(state=1, is_delete=0).order_by('-position')
            display_item['videos'] = videos[:block_item_nums]
            display_item['len'] = block_item_nums - len(display_item['videos'])
            content_list.append(display_item)

    t = get_template('popup/iphone_pop_item.html')
    html = t.render(Context({'contents': content_list, 'block_item_nums': block_item_nums, 'box_id': box_id,
                             'slider_list': slider_list }))
    return HttpResponse(html)


@login_required
def iphone_preview_box(request):
    box_id = request.GET.get('box_id')
    box = HomeBox.objects.get(pk=int(box_id), platform=3, is_delete=0, state=1)
    videos = box.iphoneboxvideo_set.filter(state=1, is_delete=0).order_by('-position')
    context = {'box_id': box.pk, 'box_title': box.title, 'videos': videos}
    t = get_template('popup/preview_box_videos.html')
    html = t.render(Context(context))
    return HttpResponse(html)


@login_required
@require_POST
def iphone_preview_save(request):
    try:
        packed_ids = request.POST.get("packed_ids")
        module_id, video_ids = packed_ids.split(':')
        video_list = map(int, video_ids.split(','))
        item_list = [IphoneBoxVideo.objects.get(id=item_id) for item_id in video_list]
        position_list = sorted([item.position for item in item_list])
        for item in item_list:
            item.position = position_list.pop()
            item.save()
        IphoneBoxVideo.objects.filter(box_id=module_id).exclude(pk__in=video_list).update(state=0)
        boxes = IphoneBoxVideo.objects.filter(box_id=module_id)
        boxes.exclude(pk__in=video_list).update(state=0)
        boxes.filter(pk__in=video_list).update(state=1)
        response = {"save_status": "success"}
    except ValueError, IphoneBoxVideo.DoesNotExist:
        response = {"save_status": "failed"}

    return HttpResponse(json.dumps(response), content_type="application/json")

