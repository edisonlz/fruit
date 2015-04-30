# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns(
    '',
    # 用户和权限
    url(regex='^user/list/$', view='user.views.user_list', name=u'user_list'),
    url(regex='^user/edit/$', view='user.views.user_edit', name=u'user_add'),
    url(regex='^user/create/$', view='user.views.user_create', name=u'user_create'),
    url(regex='^user/delete/$', view='user.views.user_delete', name=u'user_delete'),
    url(regex='^find/user$', view='user.views.find_user', name=u'find_user'),
    url(regex='^search/user$', view='user.views.user_search', name=u'search_user'),
    url(regex='^user/sync_perm$', view='user.views.sync_user_perm', name=u'sync_user_perm'),
    url(regex='^user/personal_perm$', view='user.views.show_personal_perm', name=u'personal_perm'),

    url(regex='^user_perm/show$', view='user.views.show_box_perm', name='show_main_box_perm'),
    url(regex='^user_perm/add$', view='user.views.add_box_perm', name='add_main_box_perm'),
    url(regex='^user_perm/del$', view='user.views.del_box_perm', name='del_main_box_perm'),
)