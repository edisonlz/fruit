# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'content.views',
    url(regex='^index$', view='module.index', name=u'cms_index'),
    url(regex='^box$', view='module.cms_box', name=u'cms_box_index'),
)
