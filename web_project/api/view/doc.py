#coding=utf-8
import tornado.web
import simplejson
from view.api_doc import *
import tornado



class ThirdPartLoginPage(tornado.web.RequestHandler):
    
    def get(self):
        self.render('templates/docs/websocket.html',**{})

        

class ApiDocHandler(tornado.web.RequestHandler):
    def get(self):

        api_type = self.get_argument('api_type', '1')
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None), api_type=api_type)
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            apis[api.module].append(api)

        App = type('App', (object,), {'name': "api",})
        app = App()

        self.render('templates/docs/api_docs.html', **{'tornado':tornado,'apis': apis, 'api_base': self.settings.get("api_base", ''),\
                                        'test_app_key': "", 'test_app': app,
                                        'test_user_name': self.settings.get("test_user_name", ''),"api_type":api_type})


class ApiMapHandler(tornado.web.RequestHandler):
    def get(self):
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None))
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            apis[api.module].append(api)
        self.render('templates/docs/api_map.html', **{'apis': apis, 'api_base': self.settings.get("api_base", ''), })


class ApiLoggingDataHandler(tornado.web.RequestHandler):

    def get(self):
        from api_doc import logging_data
        global logging_data
        data = logging_data[::-1]
        min_len = 15
        if len(data) < min_len:
            for i in xrange(min_len - len(data)):
                data.append("<p class='text-success'>...</p>")

        result = simplejson.dumps(data)
        self.write(result)
        

class ApiClearCacheHandler(tornado.web.RequestHandler):
    
    def get(self):
        from util import settings
        import pylibmc
        
        mc = pylibmc.Client(settings.cache_servers0)
        mc.flush_all()
        mc = pylibmc.Client(settings.cache_servers1)
        mc.flush_all()
        self.write({"status":"ok"})

class ApiAppKeyHandler(tornado.web.RequestHandler):
    def get(self):
        app_keys = {}
        self.write(simplejson.dumps(app_keys))


class ApiExampleHandler(tornado.web.RequestHandler):
    def get(self):
        id = self.get_argument('id')
        parts = id.split('.')
        data = {}
        try:
            for p in parts:
                data = (type(data) is dict) and data[p] or getattr(data, p)
        except Exception, e:
            data = ''
        if hasattr(data, 'val'):
            v = data.val()
        else:
            v = data
        if type(v) in (list, tuple, dict):
            if v:
                self.write(simplejson.dumps(v,indent=True))
            else:
                self.write('null')
        else:
            self.write(v)



class BenmarkUrl(tornado.web.RequestHandler):
    def get(self):

        api_type = self.get_argument('api_type', '1')
        all_apis = api_manager.get_apis(name=self.get_argument('name', None), module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None),
                                        api_type=api_type)
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            params = []
            api_uri = api.uri
            for p in api.params:
                if p.name in (":id",":uid",":xid",":keyword"):
                    api_uri = api_uri.replace(p.name,str(p.example or p.default))
                    continue
                if p.required or p.name =="_cookie":
                    if p.default:
                        params.append( "%s=%s" % (p.name,p.default))
                    elif str(p.example):
                        params.append( "%s=%s" % (p.name,p.example))
                    
            test_url = api_uri + "?" + '&'.join(params)
            setattr(api,"test_url",test_url)
            apis[api.module].append(api)

        self.render('templates/docs/api_test_docs.html', **{'tornado':tornado,'apis': apis})

#        import os
#        url_dir_name = os.path.dirname(__file__)
#
#        url_path = os.path.join(url_dir_name, "url.txt")
#
#        url_file = open(url_path, 'r')
#        url = url_file.read(1000000)
#        return self.write(url)
