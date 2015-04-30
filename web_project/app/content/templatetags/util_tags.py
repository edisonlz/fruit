# coding=utf-8
from django import template
import datetime, time
from app.content.models import VideoType, BrandVideo
from app.user.models import UserBoxPerm, HomeBox, HomeCommonBox, IphoneChannel, IpadChannel, AndroidChannel, BrandModule
from app.permission.models import Perm
import re
from django.shortcuts import get_object_or_404

register = template.Library()

"""
Requirement:
{%load util_tags%}

System build in https://docs.djangoproject.com/en/dev/ref/templates/builtins/
"""

#针对state
@register.filter
def dict_get(dict, key):
    """How to Use

    {{ dict|dict_get:key }}

    """

    return dict.get(key, '')


#针对视频类型
@register.filter
def dic_get_readable_type(video_type):
    for key in VideoType.KEYS:
        if key.get("id") == video_type:
            return key.get("name")


@register.filter
def get_id_url_or_game_title(video_pk):
    video = get_object_or_404(BrandVideo, pk=video_pk)
    if video.video_type == VideoType.to_i("video"):
        return video.video_id
    elif video.video_type == VideoType.to_i("url"):
        return video.url
    elif video.video_type == VideoType.to_i("user"):
        return video.video_id
    elif video.video_type in [VideoType.to_i("game_list"), VideoType.to_i("game_download"),
                              VideoType.to_i("game_details")]:
        return video.title
    else:
        return "unknown type"


@register.filter
def lower(value):  # Only one argument.
    """Converts a string into all lowercase
        How to Use
        {{ value|lower|lower|.... }}
    """
    return value.lower()


@register.filter
def upper(value):  # Only one argument.
    """Converts a string into all lowercase
        How to Use
        {{ value|lower|lower|.... }}
    """
    return value.upper()


@register.filter(name='times')
def times_1(number, arg):
    """numeric for loop, start from 1"""
    pattern = re.compile(r'\s+')
    arg = pattern.sub(' ', arg)
    len_arg = len(arg.split(' '))
    step, start = 1, 1
    try:
        if len_arg == 2:
            step, start = map(int, arg.split(' '))
        elif len_arg == 1:
            step = int(arg)
    except ValueError:
        raise template.TemplateSyntaxError('the arg must be a number or two number divided by blank')

    if isinstance(number, (int, long)):
        return range(start, number, step)
    else:
        raise template.TemplateSyntaxError('the param must be a positive num')


@register.filter
def to_int(value):  # Only one argument.
    if value and len(value) > 0:
        result = int(value)
    else:
        result = 0
    return result


@register.filter
def type_of(value):  # Only one argument.
    return type(value)


@register.assignment_tag
def get_current_time(format_string):
    """
    How to Use
    You may then store the result in a template variable using the as argument followed by the variable name, and output it yourself where you see fit:
    {% get_current_time "%Y-%m-%d %I:%M %p" as the_time %}
    <p>The time is {{ the_time }}.</p>
    """
    return datetime.datetime.now().strftime(format_string)


#将int 类型的video_type 转换成人类可读的类型
@register.simple_tag(takes_context=True)
def show_video_type_human_readable(context, video_type_number):
    for type in VideoType.KEYS:
        if video_type_number == type['id']:
            return type['name']
    return 'unknown'


@register.simple_tag()
def translate_url_location(value):
    return Perm.ch_url_name(value)


@register.simple_tag()
def translate_url_params(value):
    return Perm.ch_url_params(value)


@register.simple_tag
def transform_state_hunmanreadable(state):
    if state == 1:
        return "开启"
    elif state == 0:
        return "关闭"
    else:
        return "unknown"


@register.assignment_tag
def box_btns_show_perm(box_id, user, src=0):
    return UserBoxPerm.has_perm(box_id, user, src)


@register.simple_tag
def get_perm_platform_desc(district):
    for index, value in UserBoxPerm.SOURCE_CHOICE:
        if index == district:
            return value

    raise template.TemplateSyntaxError('the src value is not correct!')


@register.assignment_tag
def catch_all_box():
    query = {
        'is_delete': 0
    }
    fields = ['id', 'title']
    name_cls_tab = {
        'common_box': HomeCommonBox,
        'home_box': HomeBox,
        'iphone_channel': IphoneChannel,
        'ipad_channel': IpadChannel,
        'android_channel': AndroidChannel,
        'brand_module': BrandModule,
    }
    return {name: spe_cls.objects.filter(**query).only(*fields) for name, spe_cls in name_cls_tab.iteritems()}
