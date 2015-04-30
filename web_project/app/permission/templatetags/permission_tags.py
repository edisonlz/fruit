#encoding=utf8

from django import template
from django.conf import settings
import copy
import re
from app.permission.models import Perm, UserPerms, UserGroupPerms

register = template.Library()
from django.template import Context, loader
from app.content.models import VideoType

last_perm = {}


def has_perm(perm_codes, path):
    if path.startswith("/"):
        path = path[1:]
    for perm_code in perm_codes:
        if re.compile("^" + perm_code).search(path):
            return True
    return False


def get_user_perm_codes(user):
    gids = [g.id for g in user.groups.all()]
    gups = UserGroupPerms.objects.filter(group_id__in=gids)
    ups = UserPerms.objects.filter(user=user)

    perm_ids = set([up.perm_id for up in ups] + [gup.perm_id for gup in gups])
    perm_codes = [perm.code for perm in Perm.objects.filter(id__in=perm_ids)]
    return perm_codes


def gen_menu_tree(user):
    if user.is_superuser:
        return settings.MENU_CONFIG
    perm_codes = get_user_perm_codes(user)

    user_menu = []
    for root in settings.MENU_CONFIG:
        if root.has_key("path"):
            if has_perm(perm_codes, root["path"]):
                user_menu.append(root)
        else:
            valid_children = []
            if len(root.get("children", [])) > 0:
                for child in root.get("children"):
                    if child.has_key("path"):
                        has_perm(perm_codes, child["path"])
                        if has_perm(perm_codes, child["path"]):
                            valid_children.append(child)

            if valid_children:
                _root = copy.deepcopy(root)
                _root["children"] = valid_children
                user_menu.append(_root)
    return user_menu


@register.simple_tag(takes_context=True)
def show_user_top_menu(context):
    li_html = u''
    user = context["request"].user
    user_menu = gen_menu_tree(user)

    for m in user_menu:
        if m.get("divider"):
            li_html += m.get("html")
        elif m.has_key("path"):
            li_html += u'<li><a id="%s" href="%s" target="%s">%s</a></li>' % (
                m["id"], m["path"], m.get("target", ''), m["name"])
        else:
            _sub_ul_html = u""
            for c in m.get("children", []):

                if c.get("divider"):
                    _sub_ul_html += c.get("html")
                else:
                    _sub_ul_html += u'<li><a href="%s">%s</a></li>' % (c["path"], c["name"])

            li_html += u'<li class="dropdown"><a id="%s" href="#" class="dropdown-toggle" data-toggle="dropdown">%s<b class="caret"></b></a><ul class="dropdown-menu" role="menu" aria-labelledby="%s">%s</ul></li>' % (
                m["id"], m["name"], m["id"], _sub_ul_html)

    return li_html


@register.simple_tag(takes_context=True)
def show_user_left_navi(context):
    """
    <li class="nav-header">Sidebar</li>
                      <li class="active"><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
                      <li><a href="#">Link</a></li>

                      <li class="nav-header">Sidebar</li>
                      <li><a href="#">Link</a></li>
    """
    global last_perm
    #li_html = u''
    user = context["request"].user
    cur_path = context["request"].path
    user_menu = gen_menu_tree(user)
    #active_css = u'class="active" '

    parent_menu = ''

    def _get_m(cpath):
        for m in user_menu:
            for c in m.get("children", []):
                if c.has_key("path"):
                    if c["path"].startswith(cpath):
                        return m, m.get("children", [])
                    else:
                        for n in c.get("children", []):
                            if n["path"].startswith(cpath):
                                return m, m.get("children", [])
        return None, None

    parent, menus = _get_m(cur_path)
    menus = menus or user_menu or []
    t = loader.get_template('menu_left.html')
    has_active = False
    for m in menus:
        selected = False
        if m.has_key("children"):
            m["has_child"] = True
            for n in m.get("children", []):
                if n.get("path") == cur_path:
                    n["active"] = True
                    selected = True
                    last_perm[user.id] = n
                    has_active = True
                else:
                    n["active"] = False

        if m.get('path') == cur_path:
            m["active"] = True
            last_perm[user.id] = m
            has_active = True
        else:
            m["active"] = False

        m["selected"] = selected
    #set last menu to be no config menu
    if not has_active and last_perm.get(user.id, {}).get("path"):
        cur_path = last_perm[user.id].get("path")
        parent, menus = _get_m(cur_path)
        menus = menus or user_menu or []

        for m in menus:
            if m.has_key("children"):
                m["has_child"] = True
                for n in m.get("children", []):
                    if n.get("path") == cur_path:
                        n["active"] = True
            if m.get('path') == cur_path:
                m["active"] = True

    c = Context({"menus": menus, "parent": parent})
    data = t.render(c)
    return data


@register.simple_tag(takes_context=True)
def show_user_left_navi_temp2(context):
    user = context["request"].user
    cur_path = context["request"].path
    import copy

    #目前只支持三级菜单，如果要支持更多层级，这里也需要修改
    menu = copy.deepcopy(settings.FRESH_MENU_CONFIG)
    t = loader.get_template('user_menu.html')
    for item in menu:
        if 'children' in item:
            for child in item['children']:
                # 如果当前菜单被命中
                if check_if_node_active(child, cur_path):
                    child['active'] = True
                # 如果下级子菜单被命中，则子菜单和当前菜单同时命中
                if 'children' in child:
                    for low_child in child['children']:
                        if check_if_node_active(low_child, cur_path):
                            low_child['active'] = True
                            child['active'] = True

    context = Context({"menu": menu, 'user': user})
    data = t.render(context)
    return data


@register.simple_tag(takes_context=True)
def show_user_left_navi_temp(context):
    user = context["request"].user
    cur_path = context["request"].path
    try:
        platform = cur_path.split("/")[2]
        if not platform in ['iphone', 'android', 'ipad', 'win_phone']:
            platform = 'iphone'
    except Exception, e:
        platform = 'iphone'
    menus = settings.NEW_MENU_CONFIG.get(platform)

    t = loader.get_template('new_menu_left.html')
    has_active = False
    for m in menus:
        selected = False
        if m.has_key("children"):
            m["has_child"] = True
            for n in m.get("children", []):
                sub_selected = False
                if n.get("path") == cur_path:
                    n["active"] = True
                    selected = True
                    last_perm[user.id] = n
                    has_active = True
                elif n.has_key("children"):
                    n['has_child'] = True
                    for base_child in n.get("children", []):
                        if base_child.get("path") == cur_path:
                            base_child['active'] = True
                            selected = True
                            sub_selected = True
                            last_perm[user.id] = base_child
                            has_active = True
                        else:
                            base_child['active'] = False
                else:
                    n["active"] = False
                n["selected"] = sub_selected
        if m.get('path') == cur_path:
            m["active"] = True
            last_perm[user.id] = m
            has_active = True
        else:
            m["active"] = False
        m["selected"] = selected

    #set last menu to be no config menu
    if not has_active and last_perm.get(user.id, {}).get("path"):
        cur_path = last_perm[user.id].get("real_path")
        for m in menus:
            if m.has_key("children"):
                m["has_child"] = True
                for n in m.get("children", []):
                    if n.get("path") == cur_path:
                        n["active"] = True
            if m.get('path') == cur_path:
                m["active"] = True
    c = Context({"menus": menus, "STATIC_URL": settings.STATIC_URL})
    data = t.render(c)
    return data


#    if m:
#        if m.has_key("path"):
#            li_html += u'<li class="nav-header" %s><a href="%s" >%s</a></li>' % (active_css,m['path'],m["name"])
#
#        else:
#            _sub_html = u'<li class="nav-header">%s</li>' % m['name']
#            for c in m.get("children",[]):
#                if c.has_key("path"):
#                    if c["path"].startswith(cur_path):
#                        if cur_path == "/":
#                            if c['path'] == cur_path:
#                                _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css,c['path'],c['name'])
#                            else:
#                                _sub_html += u'<li ><a href="%s" >%s</a></li>' % (c['path'],c['name'])
#                        else:
#                            _sub_html += u'<li %s><a href="%s" >%s</a></li>' % (active_css,c['path'],c['name'])
#                    else:
#                        _sub_html += u'<li><a href="%s"  >%s</a></li>' % (c['path'],c['name'])
#            li_html += _sub_html

#    return li_html

def show_video_type_human_readable(video_type_number):
    for type in VideoType.KEYS:
        if video_type_number == type['id']:
            return type['name']
        else:
            return 'unknown'


def check_if_node_active(child, path):
    # 如果当前菜单被直接命中
    if child.get('path') == path:
        return True
    # 如果当前菜单的路径集被命中
    elif child.get('path_candidates') and \
            path_match_candidates(path, child.get('path_candidates')):
        return True
    return False


def path_match_candidates(path, candidates):
    for regex in candidates:
        if path_match_regex(path, regex):
            return True
    return False


def path_match_regex(path, regex):
    if not regex:
        return False
    return True if re.match(regex, path) else False
