# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponse, render_to_response, render, HttpResponseRedirect
from content.lib.apkinfo import *
from content.lib.res_service import Res2Service
from django.shortcuts import render
#from content.lib.uploadfile import save_to_local
from django.utils import simplejson
# import json
# from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# from content.lib.china_cache import ChinaCache
# from content.models import Platform, Status

MIMEANY = '*/*'
MIMEJSON = 'application/json'
MIMETEXT = 'text/plain'


@login_required
def index(request):
    return render(request, 'cms_main.html', {})


@login_required
def upload_img(request):
    if request.method == 'POST':
        file_obj = request.FILES[u'files[]']
        screenshot_type = request.POST.get("type")
        if screenshot_type:
            screenshot_size = "480x270" if screenshot_type == "0" else "270x480"
            ret = Res2Service.send(file_obj, resize=True, size=screenshot_size)
        else:
            ret = Res2Service.send(file_obj)

        if ret.get("e") and ret["e"].get("code") < 0:
            ret["e"]["desc"] = Res2Service.get_error_desc(ret["e"]["code"])
            data = ret
        else:
            data = {
                "files": [
                    {
                        "name": file_obj.name,
                        "type": file_obj.content_type,
                        "size": file_obj.size,
                        "url": ret.get('data', {}).get('url')
                    }
                ]
            }

        response = JSONResponse(data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')


def upload_apk(request):
    if request.method == 'POST':
        file_obj = request.FILES[u'files[]']
        path, source_url, download_url, md5_sum = save_to_local(request.FILES[u'files[]'])
        try:
            apk_info = get_apk_info(path)
            data = {
                "files": [
                    {
                        "name": file_obj.name,
                        "type": file_obj.content_type,
                        "size": file_obj.size,
                        "apk_info": apk_info,
                        "url": download_url,
                        "source": source_url,
                        "md5": md5_sum
                    },
                ]
            }
        except Exception, e:
            print e
            data = {
                "files": [
                    {
                        "error": -1,
                        "desc": e,
                    },
                ]
            }
            response = JSONResponse(data, status=400, mimetype=response_mimetype(request))
            response['Content-Disposition'] = 'inline; filename=files.json'
            return response

        response = JSONResponse(data, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response
    else:
        return HttpResponse('OK')


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
