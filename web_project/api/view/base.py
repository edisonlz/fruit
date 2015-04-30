#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The base handlers"""
import os,sys
import time
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../../../')))

from tornado.web import RequestHandler as _RequestHandler
import re
import hashlib
import functools
from urllib2 import URLError
import urllib
from api.util import escape, render
from django.conf import settings
from tornado.escape import utf8, _unicode
from django.core.exceptions import *
import hmac
from wi_cache import PyPoolMemcache , get_plus_json
import logging
from tornado.web import HTTPError
import copy
import json

def signature_required(method=None, cross_app=False):
    def appkey_filter(api):
        api['need_appkey'] = True

    if method:
        api_filters = getattr(method, 'api_filters', [])
        api_filters.append(appkey_filter)
        setattr(method, 'api_filters', api_filters)

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            if not self.app:
                raise HTTPError(403)

            if self.request.method != 'GET' and hasattr(self, 'cross_app'):
                raise HTTPError(403)

            return method(self, *args, **kwargs)
        return wrapper

    else:
        def app_required_wrap(_method):
            api_filters = getattr(_method, 'api_filters', [])
            api_filters.append(appkey_filter)
            setattr(_method, 'api_filters', api_filters)

            @functools.wraps(_method)
            def wrapper(self, *args, **kwargs):
                if not self.app:
                    raise HTTPError(403)

                if not cross_app and hasattr(self, 'cross_app'):
                    raise HTTPError(403)

                return _method(self, *args, **kwargs)

            return wrapper

        return app_required_wrap


def login_required(method):
    def auth_filter(api):
        api['need_login'] = True

    api_filters = getattr(method, 'api_filters', [])
    api_filters.append(auth_filter)
    setattr(method, 'api_filters', api_filters)

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user_id:
            raise HTTPError(401)
        return method(self, *args, **kwargs)

    return wrapper

class DeprecatedAttributes(object):
    u"""deprecated attributes, self.client.XXXX instead"""

    @property
    def username(self):
        return self.user_name

    @property
    def userid(self):
        return self.user_id

    @property
    def userauth(self):
        return self.user_auth

    @property
    def islogin(self):
        return self.user_login

    @property
    def device_type(self):
        return self.user_device_type

    @property
    def real_ip(self):
        return self.user_ip

    @property
    def user_name(self):
        ucookie = self.user_cookie
        return ucookie.username

    @property
    def user_ip(self):
        if not hasattr(self, '_real_ip'):
            self._real_ip = self.request.headers.get('X-Real-Ip',
                                                     self.request.remote_ip)
        return self._real_ip

    @property
    def user_cookie(self):
        if not hasattr(self, '_user_cookie'):
            # 优先取参数中传的cookie，解决js传cookie的问题
            cookie_data = self.get_argument('_cookie', '').encode('utf-8')
            cookie_data = cookie_data or self.request.headers.get('Cookie', '')
        return cookie_data


    @property
    def userid(self):
        user_token = self.get_cookie("user_token", '')
        if not user_token:
            return None
        else:
            token = user_token.split(":")
            if len(token) != 2:
                return None
            else:
                return token[0]

    @property
    def is_login(self):
        return bool(self.userid)


    def get_error_html(self, status_code, **kwargs):
        """ error html """
        if status_code == 500:
            status_code = 400
            self.set_status(400)

        ext = kwargs.get('exception')
        http_status_code = status_code
        if ext:
            http_status_code = ext.__dict__.get("http_status_code", status_code)

        desc = {
            400: '未知错误，请稍候尝试。',
            405: 'method not allowed',
            401: 'login first',
            }

        result = {
            'status': 'failed',
            'code': kwargs.get('code', status_code),
            'desc': kwargs.get('desc', desc.get(http_status_code, '')),
            }
        return result

#与统计平台代码一直
YOUKU_PRODUCT_TYPE_ID = 2
TUDOU_PRODUCT_TYPE_ID = 7

DEVICE_PHONE = 1
DEVICE_PAD = 2

ANDROID_PLATFORM_ID = 61
IOS_PLATFORM_ID = 52
WP_PLATFORM_ID = 59

PRODUCT_MAP = {
    'Youku': (YOUKU_PRODUCT_TYPE_ID, DEVICE_PHONE),
    'Youku HD': (YOUKU_PRODUCT_TYPE_ID, DEVICE_PAD),
    'Tudou': (TUDOU_PRODUCT_TYPE_ID, DEVICE_PHONE),
    'Tudou HD': (TUDOU_PRODUCT_TYPE_ID, DEVICE_PAD),
    }

PLATFORM_MAP = {
    'Android': ANDROID_PLATFORM_ID,
    'iPhone OS': IOS_PLATFORM_ID,
    'WindowsPhone': WP_PLATFORM_ID,
    }

class BaseHandler(_RequestHandler, DeprecatedAttributes):
    """The base handler of all other handlers"""


    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.get = self._deco_method(self.get)
        self.post = self._deco_method(self.post)
        self.put = self._deco_method(self.put)
        self.delete = self._deco_method(self.delete)
        self.rt = None
        self.args = Arguments(self)
        self._request_client = None
        self._is_profile = None
        self.NoCached = False
        self.user_agent = self.request.headers.get('User-Agent', '')

        ua_items = self._parse_ua(self.user_agent)
        self.product = ua_items[0]
        self.product_ver = ua_items[1]
        self.os = ua_items[2]
        self.os_ver = ua_items[3]
        self.device_model = ua_items[4]

    def _parse_ua(self, ua):
        items = ua.split(';', 5)
        if len(items) == 5:
            return tuple(items)
        else:
            return tuple([''] * 5)

    def get_product(self):
        product = PRODUCT_MAP.get(self.product, (0, 0))
        platform = PLATFORM_MAP.get(self.os, 0)

        product_type = Product.objects.filter(
            platform__platform_id=platform,
            product_type__product_id=product[0], device_type=product[1])[0:1]

        if product_type:
            #如果产品类型存在
            try:
                #查是不是被替换为同步数据的产品类型
                ds = DataSync.objects.get(src=product_type[0])
                dest = ds.des
            except Exception:
                dest = None

            #如果有目标产品类型 返回目标产品类型
            if dest:
                return dest
            else:
                return product_type[0]
        else:
            return None

    @property
    def is_pad(self):
        arg_product = self.get_argument('_product_', '')
        if arg_product:
            return arg_product.replace("+", " ") == "Youku HD"
        return self.product == "Youku HD"

    @property
    def is_phone(self):
        arg_product = self.get_argument('_product_', '')
        if arg_product:
            return arg_product.replace("+", " ") == "Youku"
        return self.product == "Youku"

    @property
    def product_id(self):
        product = self.get_product()
        if product:
            return product.id or self.get_argument('product_id', 0)
        else:
            return self.get_argument('product_id', 0) or 0

    @property
    def product_name(self):
        product = self.get_product()
        if product:
            return product.name
        else:
            return ''

    def on_connection_close(self):
        self._write_buffer = []

    def has_arg(self, name):
        return self.request.arguments.has_key(name)

    def arg(self, name, default=_RequestHandler._ARG_DEFAULT, strip=True):
        return self.get_argument(name, default, strip)

    def arg_int(self, name, default=_RequestHandler._ARG_DEFAULT, strip=True):
        return int(self.get_argument(name, default, strip))

    def arg_bool(self, name):
        return self.arg(name, 'false') == 'true'

    @property
    def is_profile(self):
        if self._is_profile is None:
            value = self.request.headers.get('Is-Profile', '').upper()
            self._is_profile = value == 'YES'
        return self._is_profile


    def get_varnish_expire(self):
        #默认有一分钟的缓存
        return 60

    def set_varnish_cache(self):
        if self.request.method not in ("GET"):
            return

        if self.settings.get("debug", False):
            return
        
        varnish_timeout =  self.get_varnish_expire()
        r = None
        if varnish_timeout:
            if type(varnish_timeout) == int:
                #no more than 10m
                if varnish_timeout > 60 * 10:
                    varnish_timeout = 60 * 10
                r = "max-age=%s" % varnish_timeout
        else:
            r = 'max-age=0'

        if r:
            self.set_header("Cache-Control", r)
            
    def write(self, chunk):
        self.set_varnish_cache()
        super(BaseHandler, self).write(self._format_result(chunk))

        
    def flush(self, include_footers=False):
        self._set_content_type()
        super(BaseHandler, self).flush(include_footers)

    def _format_result(self, chunk):
        if not isinstance(chunk, (bool, int, long, float, basestring)):
            if self.rt == 'xml':
                chunk = render.xml(chunk)
            else:
                chunk = render.json(chunk)
                if self.rt == 'text':
                    chunk = self.render_string('templates/json_format.html',
                                               json_content=chunk)
                else:
                    # jsonp supported
                    callback_func = self.get_argument('callback', '')
                    if callback_func:
                        chunk = '{}({})'.format(callback_func, chunk)
        return chunk

    def _set_content_type(self):
        if self.rt == 'xml':
            self.set_header('Content-Type', 'text/xml; charset=UTF-8')
        elif self.rt == 'json':
            self.set_header('Content-Type', 'application/json; charset=UTF-8')

    def _fix_rt(self, args):
        if not self.rt:
            self.rt = args[-1] or 'json'
            args = args[:-1]
        return args

    def _deco_method(self, fn):
        def _func(*args, **kwargs):
            args = self._fix_rt(args)
            setattr(self, '{}_args'.format(self.request.method), (args, kwargs))

            return fn(*args, **kwargs)

        return _func

    def auth_login(self, user_id, expires_days=30):
        self.user_key = self.create_signed_value("user_token", str(user_id))
        self.set_cookie("user_token", self.user_key, expires_days=expires_days)
        self._current_user_id = user_id

    def auth_logout(self):
        self.clear_cookie("user_token")
        self._current_user = None

    def prepare(self):
        pass

    def get_cookie(self, name, default=None):
        if name == 'user_token' and self.has_arg('session_key'):
            return self.arg('session_key')
        return super(BaseHandler, self).get_cookie(name, default)

    @property
    def current_user(self):
        if not hasattr(self, "_current_user"):
            user_id = self.get_current_user()
            if user_id:
                try:
                    user = User.objects.get(id=user_id)
                except:
                    raise USER_NOT_EXISTED
                setattr(self, "_current_user", user)
        return getattr(self, "_current_user", None)
    
    @property
    def current_user_id(self):
        if not hasattr(self, "_current_user_id"):
            user_id = self.get_current_user()
            if user_id:
                setattr(self, "_current_user_id", user_id)
        return getattr(self, "_current_user_id", None)

    def get_current_user(self):
        return self.get_secure_cookie("user_token", max_age_days=40)


    @property
    def is_login(self):
        return self.current_user_id != None

    @property
    def app(self):
        if not hasattr(self, "_current_app"):
            app = self.get_current_app()
            if app:
                setattr(self, "_current_app", app)
        return getattr(self, "_current_app", None)

    def get_sig(self):

        arguments = self.request.arguments
        arguments = sorted([(key, value[0]) for key, value in arguments.iteritems()], key=lambda x: x[0])
        sig_content = '&'.join(['='.join(x) for x in arguments if x[0] != "sign"])

        #用AppSecretKey计算hmac签名
        app = App.objects.get(appkey=self.arg('appkey'))
        if app:
            secretKey = app.appsecret
            app_sign = hmac.new(str(secretKey), sig_content).hexdigest()
            # logging.error('*'*50)
            # logging.error(sig_content)
            # logging.error(secretKey)
            # logging.error(app_sign)
            # logging.error(self.get_argument('sign'))
            # logging.error('*'*50)
            return app_sign, app
        else:
            return None, None

    def get_current_app(self):
        app_sign, app = self.get_sig()
        if app_sign:
            if self.settings.get("debug", False) or self.arg('sign', None) == app_sign:
                return app
        return None


class CachedHandler(BaseHandler):
    u"""
        利用_result_buffer来缓存输出结果对象
        并将这些对象存到缓存中
        flush时，根据rt的值将对象序列化再输出给客户端

        注意：有些子类在使用_result_buffer，需要重构
    """
    P_PATH = re.compile(r'^(/.+?)(\.(json|xml|text))?$')
    enable_cache = not settings.is_debug

    def __init__(self, *args, **kwargs):
        self.get = self._deco_get(self.get)

        super(CachedHandler, self).__init__(*args, **kwargs)

        self._result_buffer = []
        self.get_cache_key = self._deco_get_cache_key(self.get_cache_key)
        self._cache_key = None
        self._default_cache_expire = settings.cache_expire_1H
        self._is_update_cache = None
        logging.debug("*[enable cache] :%s" %  self.enable_cache)


    @property
    def is_update_cache(self):
        if self._is_update_cache is None:
            value = self.request.headers.get('Is-Update-Cache', '').upper()
            self._is_update_cache = value == 'YES'
        return self._is_update_cache


    def write(self, chunk):
        if chunk is not None:
            self._result_buffer.append(chunk)

    def flush(self, include_footers=False):
        self._flush_result_buffer()
        super(CachedHandler, self).flush(include_footers)

    def finish(self, chunk=None):
        if chunk is not None:
            self.write(chunk)
        self._flush_result_buffer()
        super(CachedHandler, self).finish()

    def _flush_result_buffer(self):
        for r in self._result_buffer:
            super(CachedHandler, self).write(r)
        self._result_buffer = []

    def _deco_get(self, fn):
        def _func(*args):
            args = self._fix_rt(args)

            if not self.enable_cache:
                fn(*args)
            else:
                # check cache
                ckey = self.get_cache_key()
                value = None if self.is_update_cache else PyPoolMemcache.get(ckey)
                if value is None:
                    fn(*args)
                    if self.get_status() in (200, 304) and self._result_buffer:
                        PyPoolMemcache.set(ckey, self._result_buffer,
                                       self.get_cache_expire())
                else:
                    self._result_buffer = value

        return _func

    def get_cache_expire(self):
        return self._default_cache_expire

    def get_cache_key(self):
        args_map = self.request.arguments.copy()
        # ignore pid uid guid
        args_map.pop('pid', None)
        args_map.pop('guid', None)
        args_map.pop('s', None)
        args_map.pop('t', None)
        args_map.pop('e', None)
        args_map.pop('_s_', None)
        args_map.pop('_t_', None)
        return args_map


    def _deco_get_cache_key(self, fn):
        def _func(*args, **kwargs):
            if not self._cache_key:
                path = self.request.path
                _mo = CachedHandler.P_PATH.match(path)
                if _mo:
                    path = _mo.group(1)

                _k = fn(*args, **kwargs)
                #sort by key
                sorted_keys = sorted(_k.items(), key=lambda x: x[0])

                params = []
                for i in sorted_keys:
                    params.append(i[0] + "=" + i[1])

                _k = '{}?{}'.format(path, "&".join(params))
                _k = hashlib.md5(_k).hexdigest()[8:24]
                self._cache_key = _k
            return self._cache_key

        return _func


class CachedPlusHandler(CachedHandler):
    """支持容错"""

    
    def _deco_get(self, fn):
        def _func(*args):
            args = self._fix_rt(args)

            if not self.enable_cache:
                fn(*args)
            else:
                def real_get():
                    fn(*args)
                    if self.get_status() == 200:
                        return self._result_buffer
                    else:
                        return None

                key = self.get_cache_key()
                expire_m = self.get_cache_expire()
                expire_s = None
                cached_result = get_plus_json(key, real_get, expire_m,
                                              expire_s, self.is_update_cache)
                self._result_buffer = cached_result or self._result_buffer

        return _func


class Arguments(object):
    """The request arguments handler"""

    def __init__(self, req_handler):
        self._req_handler = req_handler
        self._args_define_list = []
        self._args_map = {}
        self._parsed = False

    def define(self, arg_name, cover_func=None, default=None):
        assert isinstance(arg_name, str)
        self._args_define_list.append((arg_name, cover_func, default))
        self._parsed = False

    def to_dict(self):
        return self._args_map.copy()

    def _do_parse(self):
        for arg_name, cover_func, default in self._args_define_list:
            arg_value = self._req_handler.get_argument(arg_name, None)
            if arg_value is None:
                arg_value = default
            elif cover_func is not None:
                arg_value = cover_func(arg_value)
            self._args_map[arg_name] = arg_value

    def __getattr__(self, name):
        if not self._parsed:
            self._do_parse()
            self._parsed = True
        return self._args_map.get(name, None)

    def __setattr(self, name, value):
        raise RuntimeError('__setattr__ not allowed')


class RequestClient(object):
    u"""当前请求的客户端"""

    def __init__(self, handler):
        self.handler = handler
        self.request = handler.request
        self.headers = self.request.headers
        self.user_agent = self.headers.get('User-Agent', '')

        ua_items = self._parse_ua(self.user_agent)
        self.product = ua_items[0]
        self.product_ver = ua_items[1]
        self.os = ua_items[2]
        self.os_ver = ua_items[3]
        self.device_model = ua_items[4]

        self._user_cookie = None
        self._device_type = None
        self._real_ip = None

    @property
    def user_cookie_raw(self):
        # 优先取参数中传的cookie，解决js传cookie的问题
        cookie_data = self.handler.get_argument('_cookie', '')
        cookie_data = cookie_data.encode('utf-8')
        cookie_data = cookie_data or self.headers.get('Cookie', '')
        return cookie_data

    @property
    def user_cookie(self):
        if self._user_cookie is None:
            self._user_cookie = service_cookie.UserCookie()
            self._user_cookie.client_load(self.user_cookie_raw)
        return self._user_cookie

    @property
    def user_name(self):
        ucookie = self.user_cookie
        return ucookie.username

    @property
    def user_id(self):
        ucookie = self.user_cookie
        return ucookie.userid

    @property
    def user_auth(self):
        ucookie = self.user_cookie
        return ucookie.auth

    @property
    def user_login(self):
        ucookie = self.user_cookie
        return ucookie.is_login()


    @property
    def user_ip(self):
        if self._real_ip is None:
            self._real_ip = self.request.headers.get('X-Real-Ip',
                                                     self.request.remote_ip)
        return self._real_ip

    def _parse_ua(self, ua):
        items = ua.split(';', 5)
        if len(items) == 5:
            return tuple(items)
        else:
            return tuple([''] * 5)



def varnish_cache(timeout=60):
    
    def func(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            r = method(self, *args, **kwargs)
            if self.get_status() == 200:
                
                if type(timeout) == int:
                    r = "max-age=%s" % timeout
                else:
                    r = timeout #no cache
                    
                self.set_header("Cache-Control", r)
            return r
