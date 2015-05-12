# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'content.views',
    url(regex='^index$', view='module.index', name=u'cms_index'),
    url(regex='^box$', view='module.cms_box', name=u'cms_box_index'),
    url(regex='^box/create$', view='module.cms_box_create', name=u'cms_box_create'),
    url(regex='^status$', view='module.status', name=u'cms_status'),
    url(regex='^update_status$', view='module.update_status', name=u'cms_update_status'),
    url(regex='^update_position$', view='module.update_position', name=u'cms_update_position'),
    url(regex='^item/edit$', view='item.item_edit', name=u'item edit'),
    url(regex='^upload/img$', view='item.upload_img', name=u'item edit'),

)
