#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from app.sdk.models import *

#def login_required(func):
#    @functools.wraps(func)
#    def _wrap(handler, *args, **kwargs):
#        user_token = handler.get_cookie("user_token", '')
#        appkey = handler.get_argument('appkey')
#
#        if not user_token:
#            return handler.send_error(401, desc="login required")
#
#        uid, client_md5sum = user_token.split(":")
#
#        if not (uid and client_md5sum):
#            return handler.send_error(401, desc="login required")
#
#        else:
#            is_verify = User.verify_user_token(appkey=appkey, userid=uid, client_md5sum=client_md5sum)
#            if is_verify:
#                return func(handler, *args, **kwargs)
#            else:
#                return handler.send_error(401, desc="login required")
#    return _wrap
#
#
