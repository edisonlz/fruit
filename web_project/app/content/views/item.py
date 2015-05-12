# coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

from django.utils import simplejson
from django.conf import settings
import os
import json
from app.content.models.item import *

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'

def response_mimetype(request):
    """response_mimetype -- Return a proper response mimetype, accordingly to
    what the client accepts, as available in the `HTTP_ACCEPT` header.

    request -- a HttpRequest instance.

    """
    can_json = MIMEJSON in request.META['HTTP_ACCEPT']
    can_json |= MIMEANY in request.META['HTTP_ACCEPT']
    return MIMEJSON if can_json else MIMETEXT


class JSONResponse(HttpResponse):
    """JSONResponse -- Extends HTTPResponse to handle JSON format response.

    This response can be used in any view that should return a json stream of
    data.

    Usage:

        def a_iew(request):
            content = {'key': 'value'}
            return JSONResponse(content, mimetype=response_mimetype(request))

    """
    def __init__(self, obj='', json_opts=None, mimetype=MIMEJSON, *args, **kwargs):
        json_opts = json_opts if isinstance(json_opts, dict) else {}
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def item_edit(request):
    if request.method == "GET":
        #item id
        item_id = request.GET.get("item_id")

        try:
            item = Item.objects.get(pk=item_id)
            print item.categroy_id
        except:
            pass

        #select data
        categories = ItemCategory.objects.all()
        promotes = ItemPromote.objects.all()

        return render(request, 'item/edit.html', locals())

    elif request.method == "POST":
        #get post data
        data = json.loads(
            request.POST.get('result')
        )

        item_id = data.get('item_id', '')

        if item_id:
            item = Item.objects.get(id=item_id)
        else:
            item = Item()

        #base infomation
        item.price = data.get('price', 0)
        item.title = data.get('title', '')
        item.desc = data.get('desc', '')
        item.short_desc = data.get('short_desc', '')
        item.show_image = data.get('show_image', '')
        item.adv_image = data.get('scroller', '')
        item.stock_price = data.get('stock_price', 0.1)

        #screenshots
        screenshots = data.get('screenshot_urls', [])
        if screenshots:
            item.screen_shot_1 = screenshots[0]
            item.screen_shot_2 = screenshots[1]
            item.screen_shot_3 = screenshots[2]
            item.screen_shot_4 = screenshots[3]

        #foreign key
        catagory_id = data.get("category", 1)
        promote_id = data.get('promote', 1)
        item.categroy = ItemCategory.objects.get(
            id=catagory_id
        )
        item.promote = ItemPromote.objects.get(
            id=promote_id
        )

        #save item
        item.save()
        response_data = {
            "status": "success",
            "item_id": item.id
        }
        response = JSONResponse(
            response_data,
            mimetype=response_mimetype(request)
        )
        response['Content-Disposition'] = 'inline; filename=files.json'
        return HttpResponse(response, content_type="application/json")


def upload_img(request):

    if request.method == 'POST':

        file_obj = request.FILES[u'files[]']
        data = file_obj.read()
        path_name = '%s/tmp_img/%s' % (
            os.path.join(settings.STATICFILES_DIRS[0]),
            file_obj.name)

        fp = open(path_name, 'w')
        fp.write(data)

        response_data = {
            "files": [
                {
                    "name": file_obj.name,
                    "type": file_obj.content_type,
                    "size": file_obj.size,
                    "url": '/static/tmp_img/%s' % file_obj.name
                }
            ]
        }

        response = JSONResponse(response_data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')