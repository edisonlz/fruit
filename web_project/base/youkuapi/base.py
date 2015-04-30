#coding=utf-8

import httplib
import urllib, urllib2
import json
import settings
import base64
import functools
import random
import logging
import time, socket


class BaseApi(object):
    """
    API 基类
    """
    TimeOut = settings.TimeOut
    DEBUG_LEVEL = settings.DEBUG_LEVEL

    AppKey = settings.OpenApiAppKey
    AppSecret = settings.OpenApiAppSecret

    @classmethod
    def request(cls, host, method, path, params, headers={}):
        _headers = {'Accept-Language': 'zh-cn', 'User-Agent': 'Youku API', "Accept-Charset": "utf-8"}
        _headers.update(headers)

        conn = httplib.HTTPConnection(host, timeout=cls.TimeOut)

        params["client_id"] = cls.AppKey

        for k, v in params.items():
            if v == '' or v == None:
                del params[k]

        params = urllib.urlencode(params)
        if method == "GET":
            path = "%s?%s" % (path, params)
            params = ''

        logging.debug("*[Youku OpenAPI]* %s %s %s" % (method, host + path, params))
        conn.request(method, path, params, _headers)
        conn.set_debuglevel(cls.DEBUG_LEVEL)
        try:
            r = conn.getresponse()
            return r.read()
        except socket.timeout:
            #retry one times
            logging.debug("[timeout] retry!")
            r = conn.getresponse()
            return r.read()
        finally:
            conn.close()

    @classmethod
    def https_request(cls, host, method, path, params, headers={}):
        _headers = {'Accept-Language': 'zh-cn', 'User-Agent': 'Youku API', "Accept-Charset": "utf-8"}
        _headers.update(headers)

        conn = httplib.HTTPConnection(host, timeout=cls.TimeOut)

        params["client_id"] = cls.AppKey
        params["client_secret"] = cls.AppSecret

        for k, v in params.items():
            if v == '' or v == None:
                del params[k]

        params = urllib.urlencode(params)
        if method == "GET":
            path = "%s?%s" % (path, params)
            params = ''

        logging.debug("*[Youku OpenAPI]* %s %s %s" % (method, host + path, params))
        conn.request(method, path, params, _headers)
        conn.set_debuglevel(cls.DEBUG_LEVEL)

        try:
            r = conn.getresponse()
            return r.read()
        except socket.timeout:
            #retry one times
            logging.debug("[timeout] retry!")
            r = conn.getresponse()
            return r.read()
        finally:
            conn.close()


    @classmethod
    def get(cls, host, path, params, headers={}):
        return cls.request(host, "GET", path, params, headers)

    @classmethod
    def get_json(cls, host, path, params, headers={}):
        return json.loads(cls.request(host, "GET", path, params, headers))

    @classmethod
    def post(cls, host, path, params, headers={}):
        return cls.request(host, "POST", path, params, headers)

    @classmethod
    def https_post_json(cls, host, path, params, headers={}):
        return json.loads(cls.https_request(host, "POST", path, params, headers))

    @classmethod
    def https_get(cls, host, path, params, headers={}):
        return cls.https_request(host, "GET", path, params, headers)

    @classmethod
    def https_get_json(cls, host, path, params, headers={}):
        return json.loads(cls.https_request(host, "GET", path, params, headers))

    @classmethod
    def https_post(cls, host, path, params, headers={}):
        return cls.https_request(host, "POST", path, params, headers)

    @classmethod
    def https_post_json(cls, host, path, params, headers={}):
        return json.loads(cls.https_request(host, "POST", path, params, headers))




