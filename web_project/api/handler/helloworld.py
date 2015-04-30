__author__ = 'ldd'
# -*- coding: utf-8 -*-

from view.api_doc import handler_define, api_define, Param
from view.base import BaseHandler,CachedPlusHandler

@handler_define
class HelloWorld(BaseHandler):
    @api_define("HelloWorld", r'/', [
        ], description="HelloWorld")
    def get(self):
        self.write({'status':"HelloWorld"})