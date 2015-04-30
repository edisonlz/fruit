#encoding=utf8
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest
from django.core import urlresolvers
from django.contrib.auth.views import redirect_to_login
import re
from django.utils.encoding import iri_to_uri, force_unicode, smart_str
from models import Perm,UserPerms,UserGroupPerms

resolver = urlresolvers.get_resolver(None)
url_patterns = resolver.url_patterns
initial_regex = re.compile("^/", re.UNICODE)

from django.conf import settings

def get_path_perm_code(path,pattern = resolver):


    perm_code = ""

    for sub_pattern in pattern.url_patterns:
        try:
            sub_match = sub_pattern.regex.search(path)
        except urlresolvers.Resolver404, e:
            pass
        else:
            if sub_match:
                _perm_code = sub_pattern.regex.pattern
                if _perm_code.startswith("^"):
                    _perm_code = _perm_code[1:]
                perm_code += _perm_code
                if type(sub_pattern) == urlresolvers.RegexURLResolver:
                    new_path = path[sub_match.end():]
                    perm_code += get_path_perm_code(new_path,sub_pattern)

    return perm_code



class PermMiddleware(object):


    def process_request(self,request):

        #如果用户未登录
        if not request.user.is_authenticated():
            return

        #超级用户拥有所有权限
        if request.user.is_superuser:
            return
        
        path = request.path
        #初始化path
        match = initial_regex.search(path)
        path = path[match.end():]

        perm_code = get_path_perm_code(path)


        if perm_code in settings.ALWAYS_ALLOWED_PERMS:
            return

        #如果用户登录
        user_obj = request.user
        try:
            perm = Perm.objects.get(code = perm_code)
        except Perm.DoesNotExist,e:
            raise PermissionDenied
        else:
            try:
                UserPerms.objects.get(user = user_obj,perm = perm)

            except UserPerms.DoesNotExist:
                #查看组权限
                groups = user_obj.groups.all()
                group_ids = [g.id for g in groups]
                ugps = UserGroupPerms.objects.filter(perm = perm,group_id__in=group_ids)[:1]
                if len(ugps) > 0:
                    return
            else:
                #用户有权限，直接返回
                return

            raise PermissionDenied


