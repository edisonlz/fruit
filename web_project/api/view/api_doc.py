#coding=utf-8

import tornado.web
import tornado.locale
from tornado.web import HTTPError
from tornado.options import options

import hashlib, cgi
import tempfile
import datetime
import decimal
import functools
import logging
from UserDict import UserDict
import os, sys
from functools import wraps
#from view.base import CachedHandler, BaseHandler, CachedPlusHandler
try:
    import cProfile as profile
    import pstats
    import StringIO
except :
    pass

class ExampleParam(dict):
    def __init__(self, parent, name):
        self['_parent'] = parent
        self['_name'] = name

    def __getattr__(self, name):
        if not self.has_key(name):
            self[name] = ExampleParam(self, name)
        return self[name]

    def __str__(self):
        if self['_parent']:
            return '%s.%s' % (self['_parent'], self['_name'])
        else:
            return self['_name']

    def print_tree(self, pre=''):
        ps = ['%s%s%s' % (pre, k, (lambda vp: vp and ':\r\n%s' % vp or '')(v.print_tree(pre + '\t'))) for k, v in
              self.items() if k not in ('_parent', '_name')]
        if ps:
            return "%s" % '\r\n'.join(ps)
        else:
            return ""

ex = ExampleParam({}, 'ex')


API_TYPE_COMMON = 1        #通用API
API_TYPE_SDK = 2 #广告API
# API_TYPE_SEARCH = 3        #搜索API
# API_TYPE_USER = 4          #用户API
# API_TYPE_STATIS = 5        #统计API
# API_TYPE_OPENAPI = 6       #openapi
# API_TYPE_PLAYAPI = 7       #openapi
# API_TYPE_SDK = 8       #sdkapi


class ApiDefined(UserDict):
    def __init__(self, name, method, uri, params=[], result=None, need_login=False, need_appkey=False, handler=None,
                 module=None, filters=[], description='', api_type=1, wiki=''):
        UserDict.__init__(self)
        self['name'] = name
        self['method'] = method
        self['module'] = module
        self['uri'] = uri
        self['handler'] = handler
        self['params'] = params
        self['result'] = result
        self['need_login'] = need_login
        self['need_appkey'] = need_appkey
        self['filters'] = filters
        self['description'] = description
        self['api_type'] = api_type
        self['wiki'] = wiki
        #self['domain'] = 1

    def get_handler_name(self):
        return self['handler'].__name__

    def doc(self):
        d = '%s\n%s %s' % (self['name'], self['method'], self['uri'])
        d = d + '\nname\trequired\ttype\tdefault\texample\t\tdesc'
        d = d + '\n------------------------------------------------'
        for p in self['params']:
            d = d + '\n%s\t%s\t%s\t%s\t%s\t%s' % (
                p.name, p.required, p.param_type.__name__, p.default, p.display_example(), p.description)
        if self['result']:
            d = d + '\nResult:\n%s' % self['result']
        return d

    def __getattr__(self, name):
        try:
            return self[name]
        except Exception:
            return None


class Param(UserDict):
    def __init__(self, name, required=False, param_type=str, default=None, example=None, description="", hidden=False):
        UserDict.__init__(self)
        self['name'] = name
        self['required'] = required
        self['param_type'] = param_type
        self['default'] = default
        self['example'] = example
        self['description'] = description
        self['hidden'] = hidden

    def display_type(self, _t=None):
        _t = _t or self['param_type']
        if type(_t) in (list, tuple) and _t:
            return '[%s,..]' % self.display_type(_t[0])
        return _t.__name__

    def display_example(self):
        if self['hidden']: return ''
        if self['param_type'] is bool:
            return self['example'] and 'true' or 'false'
        else:
            return str(self['example'])

    def html_example(self):
        if self['hidden']: return ''
        if type(self['example']) is ExampleParam:
            return '<input  class="span2" type="text" class="example_input" name="%s" value=""><a class="example_value" val="%s">E</a>'\
            % (self['name'], str(self['example']))
        if self['param_type'] is file:
            return '<input class="span2" name="%s" type="file"/>' % self['name']
        if self['param_type'] is bool:
            return '<select name="%s"><option value="true"%s>True</option><option value="false"%s>False</option></select>' %\
                   (self['name'], self['example'] and ' selected' or '', (not self['example']) and ' selected' or '')
        elif self['param_type'] in (str, int, float):
            if type(self['example']) in (list, tuple):
                return '<select name="%s">%s</select>' % (
                    self['name'], ''.join(['<option value="%s">%s</option>' % (v, v) for v in self['example']]))
        return '<input  class="span2" type="text" name="%s" value="%s">' % (self['name'], str(self['example']))

    def __getattr__(self, name):
        try:
            return self[name]
        except Exception:
            return None


class ApiHolder(object):
    apis = []

    def __init__(self):
        pass

    def addapi(self, api):
        api['id'] = len(self.apis) + 1
        self.apis.append(api)

    def get_apis(self, name=None, module=None, handler=None, api_type=None):
        all_apis = self.apis
        if name:
            name = name.replace(' ', '_').lower()
            all_apis = filter(lambda api: api.name.lower().replace(' ', '_') == name, all_apis)

        if api_type:
            api_type = int(api_type)
            if api_type == API_TYPE_COMMON:
                all_apis = filter(lambda api: api.api_type==API_TYPE_COMMON, all_apis)
            elif api_type == API_TYPE_SDK:
                all_apis = filter(lambda api: api.api_type==API_TYPE_SDK, all_apis)

            #elif api_type == API_TYPE_STATIS:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_STATIS, all_apis)
            # elif api_type == API_TYPE_SEARCH:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_SEARCH, all_apis)
            # elif api_type == API_TYPE_USER:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_USER, all_apis)
            # elif api_type == API_TYPE_OPENAPI:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_OPENAPI, all_apis)
            # elif api_type == API_TYPE_PLAYAPI:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_PLAYAPI, all_apis)
            # elif api_type == API_TYPE_SDK:
            #     all_apis = filter(lambda api: api.api_type==API_TYPE_SDK, all_apis)

        if module:
            all_apis = filter(lambda api: api['module'] == module, all_apis)
        if handler:
            handler = handler.lower()
            all_apis = filter(lambda api: api['handler'].__name__.lower() == handler or api[
                                                                                        'handler'].__name__.lower() == '%shandler' % handler
                              , all_apis)
        return all_apis

    def get_urls(self):
        urls = {}
        for api in self.apis:
            if not urls.has_key(api['uri']):
                urls[api['uri']] = api['handler']
        return [(r'%s' % uri, handler) for uri, handler in urls.items()]

api_manager = ApiHolder()

def api_define(name, uri, params=[], result=None, filters=[], description='', add_user=False, api_type=1, wiki=''):
    def wrap(method):
        if not hasattr(method, 'apis'):
            setattr(method, 'apis', [])

        if add_user:
            params.append(Param('_cookie', False, str, '',
                                '_l_lgi%3D70994840%3B%20k%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20logintime%3D1348481501%3B%20u%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20v%3DUMjgzOTc5MzYw__1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1____dd316050b67516220971eff7%3B%20ykss%3Ddd316050b67516220971eff7%3B%20yktk%3D1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1%3B%20_1%3D1'
                                , u'cookie for test'))

        params.append(
            Param('guid', True, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'guid'))
        params.append(Param('_os_', False, str, "", ["Android", "iPhone OS"], u'os这个字段出自header，这里for test'))
        params.append(Param('_product_', False, str, "", ["Youku", "Youku HD", "Youku SmartTV"],
                            u'product这个字段出自header，这里for test'))
        params.append(Param('ver', False, str, "", "3.0", u'版本'))

        getattr(method, 'apis').append(
            ApiDefined(name, method.__name__.upper(), uri, params, result, module=method.__module__, filters=filters,
                       description=description, api_type=api_type, wiki=wiki))
        return method

    return wrap


def handler_define(cls):
    for m in [getattr(cls, i) for i in dir(cls) if callable(getattr(cls, i)) and hasattr(getattr(cls, i), 'apis')]:
        method_filters = getattr(m, 'api_filters', None)

        for api in m.apis:
            #api['cached'] = issubclass(cls, CachedHandler) or issubclass(cls, CachedPlusHandler)
            api['handler'] = cls
            if method_filters:
                for f in method_filters:
                    f(api)
            if api['filters']:
                for f in api['filters']:
                    f(api)
            api_manager.addapi(api)
    return cls


def suburls(prefix=ur'/', suburl=[]):
    _urls = []
    for u, h in suburl:
        _urls.append((prefix + u, h))
    return _urls

from functools import wraps
log_formatter = logging.Formatter(fmt="[%(levelname)s:%(asctime)s:%(filename)s:%(lineno)d] %(message)s")


logging_data = []
max_logging_size = 300
import re
url_extractor = re.compile(r"(GET|POST) ([^\s]+) ")

def hook_logging(f):

    @wraps(f)
    def wrap(*args,**kwargs):

        rv = f(*args,**kwargs)
        try:
            if rv:
                global logging_data
                if len(logging_data) >= max_logging_size:
                    logging_data = logging[(max_logging_size/2):]

                def url_repl(matchobj):
                    try:
                        uri =  matchobj.group(2)
                        repl = "%s <a href='%s' title='%s' target='blank'>%s</a>" % (matchobj.group(1),uri,uri,uri)
                        return repl
                    except IndexError:
                        pass

                css_dict = {
                    logging.DEBUG:"text-info",
                    logging.INFO:"text-success",
                    logging.WARNING:"text-warning",
                    logging.ERROR:"text-error",
                    logging.CRITICAL:"text-error",
                }

                _log = log_formatter.format(rv)
                _log = url_extractor.sub(url_repl,_log)
                _log = ("<p class='%s'>" % css_dict.get(rv.levelno,"muted")) + _log + "</p>"
                logging_data.append(_log)

        except Exception,e:
            pass
        return rv

    return wrap



def profile_patch(execute):
    def _(self, transforms, *args, **kwargs):
        #if options.is_debug and options.is_profile:
        if hasattr(self,"is_profile") and self.is_profile:
            self.profiler = profile.Profile()
            io = StringIO.StringIO()
            result = self.profiler.runcall(execute, self,transforms,*args, **kwargs)
            self.profiler.create_stats()
            stats = pstats.Stats(self.profiler, stream=io)
            stats.strip_dirs().sort_stats('cum')
            stats.print_stats(60)
            r = '<pre>%s</pre>' % io.getvalue()
            logging.debug(r)
            return result
        else:
            return execute(self, transforms, *args, **kwargs)
    return _



def load_api_doc(path, debug=False):
    from view import doc
    from api.handler import helloworld #service, ipad, iphone, helloworld, brand, rank

    apiurls = api_manager.get_urls()
    apiurls = [(r'{0}\.?(json|xml|text)?'.format(i), j) for (i, j) in apiurls]

    apiurls = suburls(ur'(?:/openapi-wireless)?', apiurls)

    #rest set
    resturls = []
    for uri in apiurls:
        ruri = uri[0]
        name = uri[1].__module__
        #api_handler = name.split(".")[1]
        ruri = ruri.replace(":id", "([^/]+?)")
        ruri = ruri.replace(":xid", "(X[^/]+?|\d+?)")
        ruri = ruri.replace(":uid", "(U.+?)")
        ruri = ruri.replace(":keyword", "([^/]+?)$")

        resturls.append((ruri, uri[1],))

    apiurls = resturls
    app_settings = {}

    if debug:
        apiurls = apiurls + [
                (r"/test/websocket$", doc.ThirdPartLoginPage),
                (r"/doc$", doc.ApiDocHandler),

                (r"/doc/apps$", doc.ApiAppKeyHandler),
                (r"/doc/example$", doc.ApiExampleHandler),
                (r"/debug/clear_cache$", doc.ApiClearCacheHandler),
                (r"/doc/logging/data", doc.ApiLoggingDataHandler),
                (r"/map$", doc.ApiMapHandler),
                (r'/test_url$', doc.BenmarkUrl),
           ]

        app_settings = {
            "template_path": os.path.join(path, "view"),
            "static_path": os.path.join(path, "view", "templates", "docs"),
            "static_url_prefix": '/doc/static/',
        }
        #hook logging
        from logging import root
        root.makeRecord = hook_logging(root.makeRecord)
#        logging.info = hook_logging(logging.info)
#        logging.error = hook_logging(logging.error)
#        logging.warning = hook_logging(logging.warning)
#        logging.fatal = hook_logging(logging.fatal)

        from tornado import web
        old_execute = web.RequestHandler._execute
        web.RequestHandler._execute = profile_patch(old_execute)

    return apiurls, app_settings

