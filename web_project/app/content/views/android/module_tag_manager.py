#coding=utf-8

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson

import json
from content.models import HomeBox, HomeBoxTag, AndroidHomeBoxTag, IphoneHomeBoxTag, AndroidSubChannel, AndroidChannel, \
    TagType, IosGame, AndroidGame, Platform

#@login_required
#def box_tags(request,box_id):

@login_required
def add_module_tag(request):
    print "in request.POST", request.POST
    box_id = request.POST.get("box_id", 0)
    title = request.POST.get('title', "标题")
    jump_type = request.POST.get("jump_type", 1)
    cid = request.POST.get("cid", 0) if TagType.to_s(int(jump_type)) == 'jump_to_channel' else 0
    sub_channel_id = request.POST.get("tag_sub_channel_id", 0)
    hot_word = request.POST.get("tag_hotword", "")
    box_tag = AndroidHomeBoxTag()
    old_tags = AndroidHomeBoxTag.objects.filter(box_id=box_id, tag_type="normal", is_delete=0)
    if old_tags and len(old_tags) >= 3:
        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=1.txt'
        response.write('count_err')
        return response
    if  TagType.to_s(int(jump_type)) == 'jump_to_game':
        game = AndroidGame.create_or_update(request.POST, game_id_field='original_game_id')
    else:
        game = None
    box_tag.title = title
    box_tag.box_id = box_id
    box_tag.tag_type = "normal"
    box_tag.jump_type = int(jump_type)
    box_tag.cid = cid
    box_tag.sub_channel_id = sub_channel_id
    box_tag.hot_word = hot_word
    box_tag.game_id = (game and game.id) or 0
    box_tag.state = 1
    box_tag.save()
    return render(request, "android/main_page/module_manage/module_tag/tag.html", {"tag": box_tag})


@login_required
def delete_module_tag(request):
    tag_id = request.POST.get("id") or 0
    if tag_id:
        box_tag = AndroidHomeBoxTag.objects.get(pk=tag_id)
        box_tag.is_delete = True
        box_tag.save()
    result = simplejson.dumps({'status': 'ok'})
    return HttpResponse(result)


@login_required
def query_module_tag(request, tag_id):
    tag_id = int(tag_id)
    tag = AndroidHomeBoxTag.objects.get(pk=tag_id)
    box_id = tag.box_id
    module = HomeBox.objects.get(pk=box_id)
    tag_type_info = module.tag_type_info(tag.tag_type)
    game = AndroidGame()
    if int(tag.jump_type) == TagType.to_i("jump_to_game"):
        game = AndroidGame.objects.filter(pk=tag.game_id).first()
    tag_type_hash = {item['id']: item['desc'] for item in tag_type_info}
    tag_type_list = tag_type_hash.items()
    original_channel = AndroidChannel.objects.filter(cid=int(tag.cid))
    channels = AndroidChannel.objects.filter(is_delete=False).exclude(cid=0).order_by('position')
    return render(request, 'android/main_page/module_manage/module_tag/update_tag.html',
                  {
                   "tag_type_list": tag_type_list,
                   "tag_type_hash": tag_type_hash,
                   "tag": tag,
                   "module": module,
                   "channels": channels,
                   "original_channel": original_channel,
                   "game": game
                  })

@login_required
def update_module_tag(request):
    tag_id = request.POST.get("id", 0)
    title = request.POST.get('title', "标题")
    jump_type = request.POST.get("jump_type", 1)
    cid = request.POST.get("cid", 0) if TagType.to_s(int(jump_type)) == 'jump_to_channel' else 0
    sub_channel_id = request.POST.get("tag_sub_channel_id", 0)
    hot_word = request.POST.get("tag_hotword", "")
    box_tag = AndroidHomeBoxTag.objects.get(pk=tag_id)
    if TagType.to_s(int(jump_type)) == 'jump_to_game':
        game = AndroidGame.create_or_update(request.POST, game_id_field='original_game_id')
    else:
        game = None
    box_tag.title = title
    box_tag.jump_type = int(jump_type)
    box_tag.cid = cid
    box_tag.sub_channel_id = sub_channel_id
    box_tag.hot_word = hot_word
    box_tag.game_id = (game and game.id) or 0
    box_tag.save()
    result = {
        'status': 'ok',
        'tag': {
            "title": box_tag.title,
            "jump_type": box_tag.jump_type_to_s
        }

    }
    result = simplejson.dumps(result)
    return HttpResponse(result)


@login_required
def tag_sub_channel_options(request):
    sub_channel_id = request.POST.get('sub_channel_id','')
    channel_id = request.POST.get('channel_entity_id','')
    if (len(sub_channel_id) == 0 or int(sub_channel_id) == 0) and len(channel_id) == 0:
        result = {}
    else:
        sub_channel = ""
        if sub_channel_id and len(sub_channel_id) > 0 and int(sub_channel_id) > 0:
            sub_channel = AndroidSubChannel.objects.get(pk=sub_channel_id)
        if sub_channel:
            channel = sub_channel.channel
        else:
            channel = AndroidChannel.objects.get(pk=request.POST.get("channel_entity_id"))
        sub_channels = AndroidSubChannel.objects.filter(channel_id=channel.id, is_delete=0).order_by("position")
        options = ""
        for item in sub_channels:
            if sub_channel_id and item.id == int(sub_channel_id):
                options += "<option value=\"%d\" selected=\"selected\">%s</option>\n" % (item.id, item.title)
            else:
                options += "<option value=\"%d\">%s</option>\n" % (item.id, item.title)
        result = {
            "channel_id": channel.id,
            "options": options
        }
    result = simplejson.dumps(result)
    return HttpResponse(result)




