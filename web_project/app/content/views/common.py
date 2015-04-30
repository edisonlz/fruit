#coding=utf-8
from content.models import IpadSubChannelItem, IpadSubChannelModuleItem, AndroidSubChannelModuleVideo, \
    AndroidSubChannelVideo, IphoneSubChannelModuleV4Item, IphoneSubChannelModuleVideo, IphoneSubChannelVideo, IphoneBoxVideo
import urllib, urllib2, json, logging
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.core.exceptions import FieldError
from content.lib.image_helper import ImageHelper
from app.content.models import IpadSubChannel, IphoneSubChannel, AndroidSubChannel


def get_game_info(request):
    if request.method == 'GET':
        game_info = {}
        product = request.GET.get('product')
        if product == 'ipad':
            game_id = request.GET.get('game_id')
            print game_id
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error':e.code}
                else:
                    data = {'error':e}
        elif product == 'iphone':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.IOS_GAME_HOST, path=settings.IOS_GAME_PATH,
                                                         game_id=game_id)
            print(url)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error':e.code}
                else:
                    data = {'error':e}
        elif product == 'android':
            game_id = request.GET.get('game_id')
            url = '{host}{path}?app_id={game_id}'.format(host=settings.ANDROID_GAME_HOST,
                                                         path=settings.ANDROID_GAME_PATH, game_id=game_id)
            try:
                response = urllib2.urlopen(url, timeout=5).read()
                data = json.loads(response)
            except Exception, e:
                if e.code == 400:
                    data = {'error': e.code}
                else:
                    data = {'error': e}
    return HttpResponse(json.dumps(data))


def handle_batch_items(model_name, get_dict, post_dict):
    """
    for del and use the multiple items when checking 批量删除 and 批量启用
    :param model_name:
    :param get_dict:
    :param post_dict:
    :return:
    """
    #TODO: replace the model_name with the class, it's not a good idea to use eval function
    pk_list = post_dict.get('pack_ids').split(',') if post_dict.get('pack_ids') else []
    if post_dict.get('use') == '1':
        eval(model_name).objects.filter(pk__in=pk_list).update(state=1)
    elif post_dict.get('del') == '1':
        eval(model_name).objects.filter(pk__in=pk_list).update(is_delete=1)

    param_str = '?'
    key_dict = {'channel_id': 'select_channel', 'subchannel_id': 'select_subchannel', 'module_id': 'select_module',
                'box_id': 'box_id'}
    for key, value in key_dict.iteritems():
        if key in get_dict:
            param_str += value + '=' + get_dict.get(key, '') + '&'
    param_str += 'page=' + get_dict.get('page', '1')
    return param_str


def redefine_item_pos(model, item_ids):
    """
    make the item save the new position after change position
    :param model:
    :param item_ids:
    :return:
    """
    try:
        item_ids = map(int, item_ids.split(','))
        position = 1
        for item_id in reversed(item_ids):
            item = model.objects.get(id=item_id)
            item.position = position
            item.save()
            position += 1
    except ValueError:
        return
    except ObjectDoesNotExist, e:
        # logger.exception(e)
        print e


def set_position(instance, model, query_dict=None):
    if query_dict:
        try:
            position = model.objects.filter(**query_dict).aggregate(Max('position'))['position__max']
        except (FieldError, TypeError):
            position = 0
    else:
        position = model.objects.all().aggregate(Max('position'))['position__max']
    if position is None:
        position = 0
    setattr(instance, 'position', position+1)


def generate_preview_videos(item, videos, limit, *arg):
    item['videos'] = videos[:limit]
    if len(item['videos']) < limit:
        item['videos'] = list(item['videos']) + [False] * (limit - len(item['videos']))
    for video in item['videos']:
        if video:
            for img_pat in arg:
                if img_pat:
                    video.__dict__[img_pat] = ImageHelper.convert_to_448_252(video.h_image)

    return item


#在创建精选子频道之前检查该频道下是否已有精选子频道
def check_if_has_selected_subchannel(request,):
    channel_pk = int(request.POST.get("current_channel_id", 0))
    platform = request.POST.get('platform')
    print "platform:===", platform
    if platform == 'iphone':
        sub_channels = IphoneSubChannel.objects.filter(is_delete=0, channel_id=channel_pk)
    elif platform == 'ipad':
        sub_channels = IpadSubChannel.objects.filter(is_delete=0, channel_id=channel_pk)
    elif platform == 'android':
        sub_channels = AndroidSubChannel.objects.filter(is_delete=0, channel_id=channel_pk)
    else:
        raise ValueError('params-platform wrong')
    response = {'status':'continue'}
    for sub_channel in sub_channels:
        if sub_channel.is_choiceness == 1:
            response = {'status':'discontinue', 'desc':'该频道下已经有了精选子频道---频道标题:'+sub_channel.title}
            break

    return HttpResponse(json.dumps(response), content_type="application/json")
