# coding=utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns(
    'content.views',
    url(regex='^index$', view='module.index', name=u'cms_index'),

    #home box
    url(regex='^box$', view='module.cms_box', name=u'cms_box_index'),
    url(regex='^box/create$', view='module.cms_box_create', name=u'cms_box_create'),
    url(regex='^box/update$', view='module.cms_box_update', name=u'cms_box_update'),
    url(regex='^box/delete$', view='module.cms_box_delete', name=u'cms_box_delete'),
    url(regex='^box/child$', view='module.box_item_list', name=u'box_item_list'),
    url(regex='^box/child/create$', view='module.add_item_to_box', name=u'add_item_to_box'),
    url(regex='^box/child/delete$', view='module.delete_item_to_box', name=u'delete_item_to_box'),
    url(regex='^box/child/update_position$', view='module.box_item_update_position', name=u'box_item_update_position'),
    url(regex='^status$', view='module.status', name=u'cms_status'),
    url(regex='^update_status$', view='module.update_status', name=u'cms_update_status'),
    url(regex='^update_position$', view='module.update_position', name=u'cms_update_position'),



    #address
    url(regex='^address$', view='address.cms_address', name=u'cms_address_index'),
    url(regex='^address/create$', view='address.cms_address_create', name=u'cms_address_create'),
    url(regex='^address/update_status$', view='address.update_status', name=u'cms_address_update_status'),
    url(regex='^address/update_position$', view='address.update_position', name=u'cms_address_update_position'),
    url(regex='^address/del$', view='address.delete', name=u'cms_address_del'),
    url(regex='^address/update$', view='address.cms_address_update', name=u'cms_address_update'),
    url(regex='^address/map$', view='address.map', name=u'cms_address_map'),

)
