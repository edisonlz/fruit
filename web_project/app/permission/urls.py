#encoding=utf-8
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
                       # Examples:
                       url(r'initialize' ,'permission.views.initialize',name='test_permission'),
                       url(r'edit' ,'permission.views.edit',name=u'编辑权限'),


)


