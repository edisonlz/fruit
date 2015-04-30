# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),


    url(r'^$', 'content.views.index', name=u'首页'),

    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'signin.html'}, name="signin"),
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login',  name="signout"),

    url(r"^perm", include("app.permission.urls")),

    url(r'^content/', include('app.content.urls')),

    # 用户和权限
    url(r'', include('app.user.urls')),


    ###################################################################################################################
    #  定义静态文件处理函数
    ###################################################################################################################
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.STATIC_ROOT,}),

)
if settings.DEBUG is False:
   urlpatterns += patterns('',url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}))