# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'web.info.views',
    url(regex='^index$', view='module.index', name=u'index'),
    url(regex='^items/(?P<item_id>\d+)/$', view='item.item_detail', name=u'item detail'),
)


