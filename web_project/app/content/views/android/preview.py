# coding: utf8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from content.models import Platform, HomeBox, AndroidBoxVideo
from content.views.common import generate_preview_videos


@login_required
def preview(request):
    modules = HomeBox.objects.filter(platform=Platform.to_i('android'), is_delete=0, state=1).order_by('-position')
    slider = None  # 存储5个轮播图
    slider_down = None  # 存储下方的4个轮播图
    normal_list = []  # 存储普通频道里的图
    recommend, rec_flag = None, False  # 单独处理为我推荐，将其放在最后显示
    for module in modules:
        item = {'title': module.title, 'module_id': module.pk, 'video_count': module.video_count_for_phone}
        videos = AndroidBoxVideo.objects.filter(state=1, is_delete=0, box_id=module.id).order_by('-position')
        if module.box_type_to_s in ['normal', 'game']:
            normal_list.append(generate_preview_videos(item, videos, module.video_count_for_phone, 'h_image'))
        elif module.box_type_to_s == 'recommend':
            recommend = generate_preview_videos(item, videos, module.video_count_for_phone, 'h_image')
        elif module.box_type_to_s == 'slider':
            slider = generate_preview_videos(item, videos, module.video_count_for_phone, 'h_image')
        elif module.box_type_to_s == 'under_slider':
            slider_down = generate_preview_videos(item, videos, module.video_count_for_phone, 'h_image')

    if recommend:
        normal_list.append(recommend)
        rec_flag = True

    blank_flag = True
    if slider or slider_down or normal_list:
        blank_flag = False
    return render(request, 'android/preview/preview_index.html', {
        'blank': blank_flag,
        'slider': slider,
        'slider_down': slider_down,
        'normal_list': normal_list,
        'rec_flag': rec_flag
    })


def preview_example(request):
    return render(request, 'android/preview/preview_example.html')