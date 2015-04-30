# coding=utf-8
from django.conf.urls import patterns, url


class CustChNameParser(str):
    def parse(self):
        """
          cust_ch_name_parser(u'android main_page module tag-update').parse:
            {platform: 'android', area: 'main_page', family: 'module tag', operation:'update'}
        """
        if not self:
            return {}
        location, op = self.split('-')
        location_array = location.split(' ')
        platform = location_array[0]
        area = location_array[1]
        family = ' '.join(location_array[2:])
        return {'platform': platform, 'area': area, 'family': family, 'operation': op, }


CUSTOMIZED_URL_TRANS_DICT = {
    # area
    'main_page': '首页',
    'channel_page': '频道页',
    # family
    'channel': '频道',
    'new_channel': '频道',
    'subchannel': '子频道',
    'module': '模块',
    'modulev4': '模块v4',
    'video': '视频',
    'tag': '标签',
    'brand': '品牌',
    'fetch': '抓取',
    'video_list': '专题',
    'fixed_position_video': '固定视频',
    # operation - write log(post & delete)
    'add': '添加',
    'update': '修改',
    'sort': '排序',
    'delete': '删除',
    'sync': '同步',
    'run': '执行',
    'publish': '发布',
    'switch': '开关',
    # operation - not write log(get)
    'list': '列表',
    'query': '展示',
}
CUSTOMIZED_URL_INFO = {}
CUSTOMIZED_URL_TYPES = {'platforms': [], 'areas': {}, 'families': {}, 'operations': {}}


def customized_url(regex, view, kwargs=None, name=None, prefix=''):
    if kwargs:
        cust_ch_name = kwargs.get('cust_ch_name', '')
    else:
        cust_ch_name = ''
    if cust_ch_name:
        kwargs.pop('cust_ch_name')
    url_info = CustChNameParser(cust_ch_name).parse()
    CUSTOMIZED_URL_INFO['content/' + regex.replace('^','')] = {'cust_ch_name': url_info}
    if url_info:
        try:
            CUSTOMIZED_URL_TYPES['platforms'].append(url_info['platform'])
            CUSTOMIZED_URL_TYPES['platforms'] = list(set(CUSTOMIZED_URL_TYPES['platforms']))
            if CUSTOMIZED_URL_TYPES['areas'].has_key(url_info['platform']):
                CUSTOMIZED_URL_TYPES['areas'][url_info['platform']].append(url_info['area'])
                CUSTOMIZED_URL_TYPES['areas'][url_info['platform']] = list(
                    set(CUSTOMIZED_URL_TYPES['areas'][url_info['platform']]))
            else:
                CUSTOMIZED_URL_TYPES['areas'][url_info['platform']] = [url_info['area']]

            if not CUSTOMIZED_URL_TYPES['families'].has_key(url_info['platform']):
                CUSTOMIZED_URL_TYPES['families'][url_info['platform']] = {}
            if CUSTOMIZED_URL_TYPES['families'][url_info['platform']].has_key(url_info['area']):
                CUSTOMIZED_URL_TYPES['families'][url_info['platform']][url_info['area']].append(url_info['family'])
                CUSTOMIZED_URL_TYPES['families'][url_info['platform']][url_info['area']] = list(
                    set(CUSTOMIZED_URL_TYPES['families'][url_info['platform']][url_info['area']]))
            else:
                CUSTOMIZED_URL_TYPES['families'][url_info['platform']][url_info['area']] = [url_info['family']]

            if not CUSTOMIZED_URL_TYPES['operations'].has_key(url_info['platform']):
                CUSTOMIZED_URL_TYPES['operations'][url_info['platform']] = {}
            if not CUSTOMIZED_URL_TYPES['operations'][url_info['platform']].has_key(url_info['area']):
                CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']] = {}
            if CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']].has_key(url_info['family']):
                CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']][url_info['family']].append(
                    url_info['operation'])
                CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']][url_info['family']] = list(
                    set(CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']][
                        url_info['family']]))
            else:
                CUSTOMIZED_URL_TYPES['operations'][url_info['platform']][url_info['area']][url_info['family']] = [
                    url_info['operation']]
        except Exception, e:
            print '.....exception: ', e, url_info
    return url(regex, view, kwargs, name, prefix)

urlpatterns = patterns(
    'content.views',
    url(regex='^index$', view='index', name=u'cms_index'),
    url(regex='^img/upload$', view='upload_img', name=u'upload_picture'),
    url(regex='^autocomplete/virtual_name$', view='sync_plans.get_candidates', name=u'virtual_name_autocomplete'),
    url(regex='^iphone/preview$', view='iphone_preview', name=u'iphone_preview'),
    url(regex='^iphone/preview_save$', view='iphone_preview_save', name=u'iphone_preview_save'),
    url(regex='^iphone/preview/box$', view='iphone_preview_box', name=u'iphone_preview_box'),
    # preview on all the platform
    url(regex='^iphone/main_page/preview$', view='iphone.preview', name=u'iphone preview'),
    url(regex='^ipad/main_page/preview$', view='ipad.preview', name=u'ipad preview'),
    url(regex='^android/main_page/preview$', view='android.preview', name=u'android preview'),
    url(regex='^win_phone/main_page/preview$', view='winphone.preview', name=u'winphone preview'),
    url(regex='^android/main_page/preview_example$', view='android.preview_example', name=u'preview example'),
    url(regex='^update_items_state$', view='update_items_state', name=u'update_item_state'),#批量处理开启关闭状态
    url(regex='^main_page/module_tag_jump_type', view='new_tag_jump_type_info',
        name=u'android_new_tag_jump_type_info',),#首页模块tag新建时获取tag跳转类型


    url(regex='^entrance/client_start_images$', view='background_img.start_images', name='client_start_pages'),
    url(regex='^entrance/add/start_page$', view='background_img.add_start_image', name='add_client_start_page'),
    url(regex='^entrance/update/start_page/(\d+)$', view='background_img.update_start_image',
        name='update_client_start_page'),
    url(regex='^entrance/update_state/start_page/(\d+)$', view='background_img.update_start_image_state',
        name='update_client_start_page_state'),
    url(regex='^entrance/query/start_page/(\d+)$', view='background_img.query_start_image',
        name='query_client_start_page'),
    url(regex='^entrance/delete/start_page/(\d)$', view='background_img.delete_start_image',
        name='delete_client_start_page'),

    # ranking
    url(regex='^iphone/ranking$', view='iphone.ranking', name='iphone_ranking'),
    url(regex='^iphone/ranking/add$', view='iphone.add_ranking', name='iphone_add_ranking'),
    url(regex='^iphone/query/ranking/(\d+)$', view='iphone.query_ranking', name='iphone_query_ranking'),
    url(regex='^iphone/update/ranking/(\d+)$', view='iphone.update_ranking', name='iphone_update_ranking'),
    url(regex='^iphone/update_state/ranking/(\d+)$', view='iphone.update_ranking_state',
        name='iphone_update_ranking_state'),
    url(regex='^iphone/delete/ranking/(\d+)$', view='iphone.delete_ranking', name='iphone_delete_ranking'),
    
    url(regex='^ipad/ranking$', view='ipad.ranking', name='ipad_ranking'),
    url(regex='^ipad/ranking/add$', view='ipad.add_ranking', name='ipad_add_ranking'),
    url(regex='^ipad/query/ranking/(\d+)$', view='ipad.query_ranking', name='ipad_query_ranking'),
    url(regex='^ipad/update/ranking/(\d+)$', view='ipad.update_ranking', name='ipad_update_ranking'),
    url(regex='^ipad/update_state/ranking/(\d+)$', view='ipad.update_ranking_state',
        name='ipad_update_ranking_state'),
    url(regex='^ipad/delete/ranking/(\d+)$', view='ipad.delete_ranking', name='ipad_delete_ranking'),
    
    url(regex='^android/ranking$', view='android.ranking', name='android_ranking'),
    url(regex='^android/ranking/add$', view='android.add_ranking', name='android_add_ranking'),
    url(regex='^android/query/ranking/(\d+)$', view='android.query_ranking', name='android_query_ranking'),
    url(regex='^android/update/ranking/(\d+)$', view='android.update_ranking', name='android_update_ranking'),
    url(regex='^android/update_state/ranking/(\d+)$', view='android.update_ranking_state',
        name='android_update_ranking_state'),
    url(regex='^android/delete/ranking/(\d+)$', view='android.delete_ranking', name='android_delete_ranking'),
    # #编辑 win_phone module
    # url(regex='^win_phone/main_page/modules$', view='winphone.modules',
    # name=u'winphone_modules',
    #     kwargs={'cust_ch_name': u'winphone main_page module-sort'}),
    # url(regex='^win_phone/main_page/update_status/module',
    #     view='winphone.update_module_status', name=u'winphone_update_module_status'),
    # url(regex='^win_phone/main_page/update_is_youku_channel/module',
    #     view='winphone.update_is_youku_channel',
    #     name=u'winphone_update_is_youku_channel'),
    # url(regex='^win_phone/main_page/add/module$', view='winphone.add_module',
    #     name=u'winphone_add_module',
    #     kwargs={'cust_ch_name': u'winphone main_page module-add'}),
    # url(regex='^win_phone/main_page/update/module$', view='winphone.update_module',
    #     name=u'winphone_update_module',
    #     kwargs={'cust_ch_name': u'winphone main_page module-update'}),
    # url(regex='^win_phone/main_page/query/module/(\d+)$', view='winphone.query_module',
    #     name=u'winphone_query_module',
    #     kwargs={'cust_ch_name': u'winphone main_page module-query'}),
    # url(regex='^win_phone/main_page/delete/module/(\d+)$', view='winphone.delete_module',
    #     name=u'winphone_delete_module',
    #     kwargs={'cust_ch_name': u'winphone main_page module-delete'}),
    # #TODO: change uniq_modules to replace modules
    # url(regex='^win_phone/main_page/uniq_modules$', view='winphone.uniq_modules',
    #     name=u'winphone_uniq_modules',
    #     kwargs={'cust_ch_name': u'winphone main_page module-sort'}),

    #编辑ipad module
    url(regex='^ipad/main_page/modules$', view='ipad.modules', name=u'ipad_modules',
        kwargs={'cust_ch_name': u'ipad main_page module-sort'}),
    url(regex='^ipad/main_page/update_status/module$', view='ipad.update_module_status',
        name='ipad_update_module_status',
        kwargs={'cust_ch_name': u'ipad main_page module-switch'}),
    url(regex='^ipad/main_page/update_is_youku_channel/module$',
        view='ipad.update_is_youku_channel', name=u'ipad_update_is_youku_channel'),
    url(regex='^ipad/main_page/update_is_membership/module$',
        view='ipad.update_is_membership', name=u'ipad_update_is_membership'),
    url(regex='^ipad/main_page/add/module$', view='ipad.add_module',
        name=u'ipad_add_module', kwargs={'cust_ch_name': u'ipad main_page module-add'}),
    url(regex='^ipad/main_page/update/module$', view='ipad.update_module', name=u'ipad_update_module',
        kwargs={'cust_ch_name': u'ipad main_page module-update'}),
    url(regex='^ipad/main_page/query/module/(\d+)$', view='ipad.query_module', name=u'ipad_query_module',
        kwargs={'cust_ch_name': u'ipad main_page module-query'}),
    url(regex='^ipad/main_page/delete/module/(\d+)$', view='ipad.delete_module', name=u'ipad_delete_module',
        kwargs={'cust_ch_name': u'ipad main_page module-delete'}),
    url(regex='^ipad/main_page/uniq_modules$', view='ipad.uniq_modules', name=u'ipad_uniq_modules',
        kwargs={'cust_ch_name': u'ipad main_page module-sort'}),


    #编辑android module
    url(regex='^android/main_page/modules$', view='android.modules', name=u'android_modules',
        kwargs={'cust_ch_name': u'android main_page module-sort'}),
    url(regex='^android/main_page/update_status/module$', view='android.update_module_status',
        name=u'android_update_module_status',
        kwargs={'cust_ch_name': u'android main_page module-switch'}),
    url(regex='^android/main_page/update_is_youku_channel/module$', view='android.update_is_youku_channel',
        name=u'android_update_is_youku_channel'),
    # url(regex='^android/main_page/update_is_multiply_units/module',
    #     view='android.update_is_multiply_units',
    #     name=u'android_update_is_multiply_units'),
    url(regex='^android/main_page/add/module$', view='android.add_module', name=u'android_add_module',
        kwargs={'cust_ch_name': u'android main_page module-add'}),
    url(regex='^android/main_page/update/module$', view='android.update_module', name=u'android_update_module',
        kwargs={'cust_ch_name': u'android main_page module-update'}),
    url(regex='^android/main_page/query/module/(\d+)$', view='android.query_module', name=u'android_query_module',
        kwargs={'cust_ch_name': u'android main_page module-query'}),
    url(regex='^android/main_page/delete/module/(\d+)$', view='android.delete_module', name=u'android_delete_module',
        kwargs={'cust_ch_name': u'android main_page module-delete'}),
    url(regex='^android/main_page/uniq_modules$', view='android.uniq_modules', name=u'android_uniq_modules',
        kwargs={'cust_ch_name': u'android main_page module-sort'}),
    url(regex='^android/main_page/module/tag_titles$', view='android.get_module_tag_titles',
        name=u'android_get_module_tag_titles'),

    # 编辑 android video list
    url(regex='^android/video_lists$', view='android.video_lists', name=u'android_video_lists',
        kwargs={'cust_ch_name': u'android video_list module-sort'}),
    url(regex='^android/add/video_list$', view='android.add_video_list', name=u'android_add_video_list',
        kwargs={'cust_ch_name': u'android video_list module-add'}),
    url(regex='^android/query/video_list/(\d+)$', view='android.query_video_list', name=u'android_query_video_list',
        kwargs={'cust_ch_name': u'android video_list module-query'}),
    url(regex='^android/delete/video_list/(\d+)$', view='android.delete_video_list', name=u'android_delete_video_list',
        kwargs={'cust_ch_name': u'android video_list module-delete'}),
    url(regex='^android/update_status/video_list$', view='android.update_status_video_list',
        name=u'android_update_status_video_list'),
    url(regex='^android/update/video/video_list$', view='android.update_video_list', name=u'android_update_video_list',
        kwargs={'cust_ch_name': u'android video_list module-update'}),
    url(regex='^android/video_list/(\d+)/videos$', view='android.videos_in_vl', name=u'videos_in_vl',
        kwargs={'cust_ch_name': u'android video_list video-sort'}),
    url(regex='^android/video_list/(\d+)/add_video$', view='android.video_list_add_video', name=u'video_list_add_video',
        kwargs={'cust_ch_name': u'android video_list video-add'}),
    url(regex='^android/video_list/(\d+)/query_video/(\d+)$', view='android.video_list_query_video',
        name=u'video_list_query_video', kwargs={'cust_ch_name': u'android video_list video-add'}),
    url(regex='^android/video_list/(\d+)/update_video/(\d+)$', view='android.video_list_update_video',
        name=u'video_list_update_video', kwargs={'cust_ch_name': u'android video_list video-update'}),
    url(regex='^android/video_list/update_video_status$', view='android.video_list_update_video_status',
        name=u'video_list_update_video_status', kwargs={'cust_ch_name': u'android video_list video-update'}),
    url(regex='^android/video_list/update_video_value$', view='android.video_list_update_video_value',
        name=u'video_list_update_video_value', kwargs={'cust_ch_name': u'android video_list video-update'}),
    url(regex='^android/video_list/(\d+)/delete_video/(\d+)$', view='android.video_list_delete_video',
        name=u'video_list_delete_video', kwargs={'cust_ch_name': u'android video_list video-delete'}),


    #编辑android module tag
    url(regex='^android/main_page/add/module_tag$', view='android.add_module_tag', name=u'android_add_module_tag',
        kwargs={'cust_ch_name': u'android main_page module tag-add'}),
    url(regex='^android/main_page/delete/module_tag$', view='android.delete_module_tag',
        name=u'android_delete_module_tag', kwargs={'cust_ch_name': u'android main_page module tag-delete'}),
    url(regex='^android/main_page/query/module_tag/(\d+)$', view='android.query_module_tag',
        name=u'android_query_module_tag', kwargs={'cust_ch_name': u'android main_page module tag-query'}),
    url(regex='^android/main_page/update/module_tag$', view='android.update_module_tag',
        name=u'android_update_module_tag', kwargs={'cust_ch_name': u'android main_page module tag-update'}),
    url(regex='^android/info/sub_channel_options$', view='android.tag_sub_channel_options',
        name=u'android_tag_sub_channel_options'),
    url(regex='^android/sub_channel/add_tag$', view='android.android_add_tag', name='android_add_tag'),
    url(regex='^android/sub_channel/delete_tag$', view='android.android_delete_tag', name='android_delete_tag'),
    url(regex='^android/sub_channel/sort_tag$', view='android.android_sort_tag', name='android_sort_tag'),


    #编辑iphone module
    url(regex='^iphone/main_page/modules$', view='iphone.modules', name=u'iphone_modules',
        kwargs={'cust_ch_name': u'iphone main_page module-sort'}),
    url(regex='^iphone/main_page/update_status/module$', view='iphone.update_module_status',
        name=u'iphone_update_module_status',
        kwargs={'cust_ch_name': u'iphone main_page module-switch'}),
    url(regex='^iphone/main_page/update_is_youku_channel/module$', view='iphone.update_is_youku_channel',
        name=u'iphone_update_is_youku_channel'),
    url(regex='^iphone/main_page/add/module$', view='iphone.add_module', name=u'iphone_add_module',
        kwargs={'cust_ch_name': u'iphone main_page module-add'}),
    url(regex='^iphone/main_page/update/module$', view='iphone.update_module', name=u'iphone_update_module',
        kwargs={'cust_ch_name': u'iphone main_page module-update'}),
    url(regex='^iphone/main_page/query/module/(\d+)$', view='iphone.query_module', name=u'iphone_query_module',
        kwargs={'cust_ch_name': u'iphone main_page module-query'}),
    url(regex='^iphone/main_page/delete/module/(\d+)$', view='iphone.delete_module', name=u'iphone_delete_module',
        kwargs={'cust_ch_name': u'iphone main_page module-delete'}),
    url(regex='^iphone/main_page/uniq_modules$', view='iphone.uniq_modules', name=u'iphone_uniq_modules',
        kwargs={'cust_ch_name': u'iphone main_page module-sort'}),
    url(regex='^iphone/main_page/module/tag_titles$', view='iphone.get_module_tag_titles',
        name=u'iphone_get_module_tag_titles'),


    #编辑iphone module tag
    url(regex='^iphone/main_page/add/module_tag$', view='iphone.add_module_tag', name=u'iphone_add_module_tag',
        kwargs={'cust_ch_name': u'iphone main_page module tag-sort'}),
    url(regex='^iphone/main_page/delete/module_tag$', view='iphone.delete_module_tag', name=u'iphone_delete_module_tag',
        kwargs={'cust_ch_name': u'iphone main_page module tag-delete'}),
    url(regex='^iphone/main_page/query/module_tag/(\d+)$', view='iphone.query_module_tag',
        name=u'iphone_query_module_tag', kwargs={'cust_ch_name': u'iphone main_page module tag-query'}),
    url(regex='^iphone/main_page/update/module_tag$', view='iphone.update_module_tag', name=u'iphone_update_module_tag',
        kwargs={'cust_ch_name': u'iphone main_page module tag-update'}),
    url(regex='^iphone/info/sub_channel_options$', view='iphone.tag_sub_channel_options',
        name=u'iphone_tag_sub_channel_options'),

    #编辑video
    #ipad main_pagevideo
    url(regex='^ipad/main_page/videos$', view='ipad.videos', name=u'ipad_main_page_videos',
        kwargs={'cust_ch_name': u'ipad main_page module video-sort'}),
    url(regex='^ipad/main_page/add/video$', view='ipad.add_video', name=u'ipad_main_page_add_video',
        kwargs={'cust_ch_name': u'ipad main_page module video-add'}),
    url(regex='^ipad/main_page/delete/video/(\d+)$', view='ipad.delete_video', name=u'ipad_delete_video',
        kwargs={'cust_ch_name': u'ipad main_page module video-delete'}),
    url(regex='^ipad/main_page/query/video/(\d+)$', view='ipad.query_video', name=u'ipad_query_video',
        kwargs={'cust_ch_name': u'ipad main_page module video-query'}),
    url(regex='^ipad/main_page/update/video$', view='ipad.update_video', name=u'ipad_update_video',
        kwargs={'cust_ch_name': u'ipad main_page module video-update'}),
    url(regex='^ipad/main_page/update_status/video$', view='ipad.update_video_status',
        name=u'ipad_update_video_status'),
    url(regex='^ipad/main_page/update_video_value$', view='ipad.update_video_value', name=u'ipad_update_video_value'),
    url(regex='^ipad/main_page/add/video_field$', view='ipad.add_video_fields', name=u'ipad_add_video_fields'),

    url(regex='^ipad/main_page/query/module_tag/(\d+)$', view='ipad.query_module_tag',
        name=u'ipad_query_module_tag', kwargs={'cust_ch_name': u'ipad main_page module tag-query'}),
    url(regex='^ipad/main_page/update/module_tag$', view='ipad.update_module_tag', name=u'ipad_update_module_tag',
        kwargs={'cust_ch_name': u'ipad main_page module tag-update'}),
    url(regex='^ipad/info/sub_channel_options$', view='ipad.tag_sub_channel_options',
        name=u'ipad_tag_sub_channel_options'),
    url(regex='^ipad/main_page/module/tag_titles$', view='ipad.get_module_tag_titles',
        name=u'ipad_get_module_tag_titles'),
    url(regex='^ipad/main_page/add/module_tag$', view='ipad.add_module_tag', name=u'ipad_add_module_tag',
        kwargs={'cust_ch_name': u'ipad main_page module tag-sort'}),
    url(regex='^ipad/main_page/delete/module_tag$', view='ipad.delete_module_tag', name=u'ipad_delete_module_tag',
        kwargs={'cust_ch_name': u'ipad main_page module tag-delete'}),

    #iphone main_pagevideo
    url(regex='^iphone/main_page/videos$', view='iphone.videos', name=u'iphone_main_page_videos',
        kwargs={'cust_ch_name': u'iphone main_page module video-sort'}),
    url(regex='^iphone/main_page/add/video$', view='iphone.add_video', name=u'iphone_main_page_add_video',
        kwargs={'cust_ch_name': u'iphone main_page module video-add'}),
    url(regex='^iphone/main_page/delete/video/(\d+)$', view='iphone.delete_video', name=u'iphone_delete_video',
        kwargs={'cust_ch_name': u'iphone main_page module video-delete'}),
    url(regex='^iphone/main_page/query/video/(\d+)$', view='iphone.query_video', name=u'iphone_query_video',
        kwargs={'cust_ch_name': u'iphone main_page module video-query'}),
    url(regex='^iphone/main_page/update/video$', view='iphone.update_video', name=u'iphone_update_video',
        kwargs={'cust_ch_name': u'iphone main_page module video-update'}),
    url(regex='^iphone/main_page/update_status/video$', view='iphone.update_video_status',
        name=u'iphone_update_video_status'),
    url(regex='^iphone/main_page/update_video_value$', view='iphone.update_video_value',
        name=u'iphone_update_video_value'),
    url(regex='^iphone/main_page/add/video_field$', view='iphone.add_video_fields', name=u'iphone_add_video_fields'),
    # url(regex='^iphone/main_page/update_batch_videos', view='iphone.update_batch_videos',
    #     name=u'iphone_main_page_update_batch_videos'),
    # #android main_pagevideo
    url(regex='^android/main_page/videos$', view='android.videos', name=u'android_main_page_videos',
        kwargs={'cust_ch_name': u'android main_page module video-sort'}),
    url(regex='^android/main_page/add/video$', view='android.add_video', name=u'android_main_page_add_video',
        kwargs={'cust_ch_name': u'android main_page module video-add'}),
    url(regex='^android/main_page/delete/video/(\d+)$', view='android.delete_video', name=u'android_delete_video',
        kwargs={'cust_ch_name': u'android main_page module video-delete'}),
    url(regex='^android/main_page/query/video/(\d+)$', view='android.query_video', name=u'android_query_video',
        kwargs={'cust_ch_name': u'android main_page module video-query'}),
    url(regex='^android/main_page/update/video$', view='android.update_video', name=u'android_update_video',
        kwargs={'cust_ch_name': u'android main_page module video-update'}),
    url(regex='^android/main_page/update_status/video$', view='android.update_video_status',
        name=u'android_update_video_status'),
    url(regex='^android/main_page/update_video_value$', view='android.update_video_value',
        name=u'android_update_video_value'),
    url(regex='^android/main_page/add/video_field$', view='android.add_video_fields', name=u'android_add_video_fields'),
    # # #winphone main_pagevideo
    # url(regex='^win_phone/main_page/videos$', view='winphone.videos',
    #     name=u'winphone_main_page_videos',
    #     kwargs={'cust_ch_name': u'winphone main_page module video-sort'}),
    # url(regex='^win_phone/main_page/add/video$', view='winphone.add_video',
    #     name=u'winphone_main_page_add_video',
    #     kwargs={'cust_ch_name': u'winphone main_page module video-add'}),
    # url(regex='^win_phone/main_page/delete/video/(\d+)$', view='winphone.delete_video',
    #     name=u'winphone_delete_video',
    #     kwargs={'cust_ch_name': u'winphone main_page module video-delete'}),
    # url(regex='^win_phone/main_page/query/video/(\d+)$', view='winphone.query_video',
    #     name=u'winphone_query_video',
    #     kwargs={'cust_ch_name': u'winphone main_page module video-query'}),
    # url(regex='^win_phone/main_page/update/video', view='winphone.update_video',
    #     name=u'winphone_update_video',
    #     kwargs={'cust_ch_name': u'winphone main_page module video-update'}),
    # url(regex='^win_phone/main_page/update_status/video',
    #     view='winphone.update_video_status', name=u'winphone_update_video_status'),
    # url(regex='^win_phone/main_page/add/video_field$', view='winphone.add_video_fields',
    #     name=u'winphone_add_video_fields'),

    url(regex='^get_game_info$', view='get_game_info', name=u'从游戏服务器获取游戏信息'),
)

urlpatterns += patterns(
    'content.views',

    # #####new addded
    # url(regex='^ipad/main_page/add/video_field', view='add_video_fields', name=u'add_video_fields'),
    #url(regex='^get_game_info', view='get_game_info', name=u'从游戏服务器获取游戏信息'),

    #url(regex='^ipad/main_page/common_module', view='common_module', name=u'common_module'),
    #url(regex='^ipad/main_page/sync_common_box', view='sync_common_box', name=u'sync_common_box'),
    #url(regex='^ipad/main_page/sync_video', view='sync_video', name=u'sync_video'),

    # ipad channel channel_page
    url(regex='^ipad/channels$', view='ipad.channels', name=u'ipad_channels',
        kwargs={'cust_ch_name': u'ipad channel_page channel-update'}),
    url(regex='^ipad/add/channels$', view='ipad.add_channel', name=u'ipad_add_channel',
        kwargs={'cust_ch_name': u'ipad channel_page channel-add'}),
    url(regex='^ipad/update_status/channel$', view='ipad.update_channel_status', name=u'ipad_update_channel_status'),
    url(regex='^ipad/delete/channel/(\d+)$', view='ipad.delete_channel', name=u'ipad_delete_channel',
        kwargs={'cust_ch_name': u'ipad channel_page channel-delete'}),
    url(regex='^ipad/query/channel/(\d+)$', view='ipad.query_channel', name=u'ipad_query_channel',
        kwargs={'cust_ch_name': u'ipad channel_page channel-query'}),
    # url(regex='^ipad/update/channel$', view='ipad.update_channel', name=u'ipad_update_channel',
    #     kwargs={'cust_ch_name': u'ipad channel_page channel-update'}),
    url(regex='^ipad/update/new_channel$', view='ipad.update_channel', name=u'ipad_update_new_channel',
        kwargs={'cust_ch_name': u'ipad channel_page channel-update'}),


    #ipad new_channel
    url(regex='^ipad/new_channels$', view='ipad.new_channels', name=u'ipad_new_channels',
        kwargs={'cust_ch_name': u'ipad channel_page channel-sort'}),
    url(regex='^ipad/update_status/new_channel$', view='ipad.update_new_channel_status',
        name=u'ipad_update_new_channel_status'),
    url(regex='^ipad/channels$', view='ipad.channels', name=u'ipad_channels',
        kwargs={'cust_ch_name': u'ipad channel_page channel-sort'}),
    url(regex='^ipad/add/new_channels$', view='ipad.add_new_channel', name=u'ipad_add_new_channel',
        kwargs={'cust_ch_name': u'ipad channel_page new_channel-add'}),
    url(regex='^ipad/delete/new_channel/(\d+)$', view='ipad.delete_new_channel', name=u'ipad_delete_new_channel',
        kwargs={'cust_ch_name': u'ipad channel_page new_channel-delete'}),
    url(regex='^ipad/query/new_channel/(\d+)$', view='ipad.query_new_channel', name=u'ipad_query_new_channel',
        kwargs={'cust_ch_name': u'ipad channel_page new_channel-query'}),
    url(regex='^ipad/update/new_channel$', view='ipad.update_new_channel', name=u'ipad_update_new_channel',
        kwargs={'cust_ch_name': u'ipad channel_page new_channel-update'}),
    url(regex='^ipad/channel/publish$', view='ipad.channel_publish', name=u'ipad_channel_publish',
        kwargs={'cust_ch_name': u'ipad channel_page channel-publish'}),


    # ipad channel_video
    url(regex='^ipad/channel_videos$', view='ipad.channel_videos', name=u'ipad_channel_videos'),
    url(regex='^ipad/add/channel_videos$', view='ipad.add_channel_video', name=u'ipad_add_channel_video'),
    url(regex='^ipad/delete/channel_video/(\d+)$', view='ipad.delete_channel_video', name=u'ipad_delete_channel_video'),
    #kwargs={'cust_ch_name': u'ipad channel_page channel channel_video video-delete'}),
    url(regex='^ipad/query/channel_video/(\d+)$', view='ipad.query_channel_video', name=u'ipad_query_channel_video'),
    url(regex='^ipad/update/channel_video$', view='ipad.update_channel_video', name=u'ipad_update_channel_video'),
    url(regex='^ipad/update_status/channel_video$', view='ipad.update_channel_video_status',
        name=u'ipad_update_channel_video_status'),

    # subchannel subchanneltag管理
    url(regex='^ipad/channel/subchannels$', view='ipad.subchannels', name=u'ipad_sub_channels',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel-sort'}),
    url(regex='^ipad/add/subchannel$', view='ipad.add_subchannel', name=u'ipad_add_sub_channel',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel-add'}),
    url(regex='^ipad/delete/subchannel$', view='ipad.delete_subchannel', name=u'ipad_delete_sub_channel',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel-delete'}),
    url(regex='^ipad/query/subchannel$', view='ipad.query_subchannel', name=u'ipad_query_sub_channel',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel-query'}),
    url(regex='^ipad/update/subchannel$', view='ipad.update_subchannel', name=u'ipad_update_sub_channel',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel-update'}),
    url(regex='^ipad/update_status/subchannel$', view='ipad.update_subchannel_status',
        name=u'ipad_update_sub_channel_status'),

    # subchannel subchannelmodule管理
    url(regex='^ipad/subchannel/modules$', view='ipad.subchannel_modules', name=u'ipad_sub_channel_modules',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel module-sort'}),
    url(regex='^ipad/add/subchannel/module$', view='ipad.add_subchannel_module', name=u'ipad_add_sub_channel_module',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel module-add'}),
    url(regex='^ipad/delete/subchannel/module$', view='ipad.delete_subchannel_module',
        name=u'ipad_delete_sub_channel_module', kwargs={'cust_ch_name': u'ipad channel_page subchannel module-delete'}),
    url(regex='^ipad/query/subchannel/module$', view='ipad.query_subchannel_module',
        name=u'ipad_query_sub_channel_module', kwargs={'cust_ch_name': u'ipad channel_page subchannel module-query'}),
    url(regex='^ipad/update/subchannel/module$', view='ipad.update_subchannel_module',
        name=u'ipad_update_sub_channel_module', kwargs={'cust_ch_name': u'ipad channel_page subchannel module-update'}),
    url(regex='^ipad/update_status/subchannel/module$', view='ipad.update_subchannel_module_status',
        name=u'ipad_update_sub_channel_module_status'),
    url(regex='^ipad/subchannel/publish$', view='ipad.sub_channel_publish', name=u'ipad_subchannel_publish'),

    # subchannel subchannelmodulevideo管理
    url(regex='^ipad/subchannel/module/items$', view='ipad.subchannel_module_items',
        name=u'ipad_sub_channel_module_items', kwargs={'cust_ch_name': u'ipad channel_page subchannel video-sort'}),
    url(regex='^ipad/add/subchannel/module/item$', view='ipad.add_subchannel_module_item',
        name=u'ipad_add_sub_channel_module_item', kwargs={'cust_ch_name': u'ipad channel_page subchannel video-add'}),
    url(regex='^ipad/delete/subchannel/module/item$', view='ipad.delete_subchannel_module_item',
        name=u'ipad_delete_sub_channel_module_item',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel video-delete'}),
    url(regex='^ipad/query/subchannel/module/item$', view='ipad.query_subchannel_module_item',
        name=u'ipad_query_sub_channel_module_item',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel video-query'}),
    url(regex='^ipad/update/subchannel/module/item$', view='ipad.update_subchannel_module_item',
        name=u'ipad_update_sub_channel_module_item',
        kwargs={'cust_ch_name': u'ipad channel_page subchannel video-update'}),
    url(regex='^ipad/update_status/subchannel/module/item$', view='ipad.update_subchannel_module_item_status',
        name=u'ipad_update_sub_channel_module_status_item'),
    url(regex='^ipad/update_batch/subchannel/module/item$', view='ipad.update_batch_items',
        name=u'ipad_update_batch_items'),
    url(regex='^ipad/update_item_value/subchannel/module/item$', view='ipad.update_subchannel_module_item_value',
        name=u'ipad_update_item_value_sub_channel_module_item'),
    url(regex='ipad/channel_page/add/video_field$', view='ipad.channel_page_add_video_fields',
        name=u'android_add_video_fields'),

        # android固定位置视频管理
    url(regex='^ipad/fixed_position_videos$', view='ipad.fixed_position_videos',
        name=u'ipad_fixed_position_videos', kwargs={'cust_ch_name': u'ipad fixed_position_video video-sort'}),
    url(regex='^ipad/add/fixed_position_video$', view='ipad.add_fixed_position_video',
        name=u'ipad_add_fixed_position_video', kwargs={'cust_ch_name': u'ipad fixed_position_video video-add'}),
    url(regex='^ipad/delete/fixed_position_video$', view='ipad.delete_fixed_position_video',
        name=u'ipad_delete_fixed_position_video',
        kwargs={'cust_ch_name': u'ipad fixed_position_video video-delete'}),
    url(regex='^ipad/query/fixed_position_video$', view='ipad.query_fixed_position_video',
        name=u'ipad_query_fixed_position_video',
        kwargs={'cust_ch_name': u'ipad fixed_position_video video-query'}),
    url(regex='^ipad/update/fixed_position_video$', view='ipad.update_fixed_position_video',
        name=u'ipad_update_fixed_position_video',
        kwargs={'cust_ch_name': u'ipad fixed_position_video video-update'}),
    url(regex='^ipad/update_video_value/fixed_position_video$', view='ipad.update_fixed_position_video_value',
        name=u'ipad_update_fixed_position_video_value'),
    url(regex='^ipad/check_fixed_position/fixed_position_video$', view='ipad.check_fixed_position',
        name=u'ipad_check_fixed_position'),


    # syncjob 同步抓取任务管理
    url(regex='^sync/virtual_names/single_fetch$', view='sync_plans.single_virtual_name_fetch',
        name='single_virtual_name_fetch'),
    url(regex='^sync/virtual_names$', view='sync_plans.show_all_virtual_name', name=u'show_all_virtual_name'),
    url(regex='^sync/check_virtual_name$', view='sync_plans.check_virtual_name_from_web', name=u'check_virtual_name'),
    url(regex='^sync/select_plans$', view='sync_plans.show_sync_jobs', name=u'show_select_plans'),
    url(regex='^sync/plans$', view='sync_plans.get_all_plans', name=u'get_all_plans'),
    url(regex='^sync/plan$', view='sync_plans.show_single_plan', name=u'show_single_plan'),
    url(regex='^sync/add/plan$', view='sync_plans.add_sync_plan', name=u'add_sync_plan',
        kwargs={'cust_ch_name': u'common channel_page fetch-add'}),
    url(regex='^sync/del/plan/(\d+)$', view='sync_plans.del_sync_plan', name=u'del_sync_plan',
        kwargs={'cust_ch_name': u'common channel_page fetch-delete'}),
    url(regex='^sync/runatonce/plan/(\d+)$', view='sync_plans.run_at_once_plan', name=u'run_at_once_plan',
        kwargs={'cust_ch_name': u'common channel_page fetch-run'}),
    url(regex='^sync/update/plan/(\d+)$', view='sync_plans.update_sync_plan', name=u'update_sync_plan',
        kwargs={'cust_ch_name': u'common channel_page fetch-update'}),
    url(regex='^sync/jobs/log_watch/(\d+)$', view='sync_plans.log_watch', name=u'fetch_job_log_watch',
        kwargs={'cust_ch_name': u'common channel_page fetch-log'}),


    #below are temp not use
    # url(regex='^sync/plans$',
    #     view='sync_plans.show_sync_jobs',
    #     name=u'list_sync_plans'),
    # url(regex='^sync/update/plan$', view='sync_plans.update_sync_plan',
    #     name=u'update_sync_plan'),
    # url(regex='^sync/delete/plan$', view='sync_plans.delete_sync_plan',
    #     name=u'delete_module_plan'),

    # iphone channel管理
    # url(regex='^iphone/channels$', view='iphone.channels', name=u'iphone_channels',
    #     kwargs={'cust_ch_name': u'iphone channel_page channel-sort'}),
    # url(regex='^iphone/add/channels$', view='iphone.add_channel',
    #     name=u'iphone_add_channel',
    #     kwargs={'cust_ch_name': u'iphone channel_page channel-add'}),
    # url(regex='^iphone/delete/channel/(\d+)$', view='iphone.delete_channel',
    #     name=u'iphone_delete_channel',
    #     kwargs={'cust_ch_name': u'iphone channel_page channel-delete'}),
    # url(regex='^iphone/query/channel/(\d+)$', view='iphone.query_channel',
    #     name=u'iphone_query_channel',
    #     kwargs={'cust_ch_name': u'iphone channel_page channel-query'}),
    # url(regex='^iphone/update/channel$', view='iphone.update_channel',
    #     name=u'iphone_update_channel',
    #     kwargs={'cust_ch_name': u'iphone channel_page channel-update'}),


    url(regex='^iphone/update_status/channel$', view='iphone.update_channel_status',
        name=u'iphone_update_channel_status'),
    url(regex='^iphone/new_channels$', view='iphone.new_channels', name=u'iphone_new_channels',
        kwargs={'cust_ch_name': u'iphone channel_page channel-sort'}),
    url(regex='^iphone/update_status/new_channel$', view='iphone.update_new_channel_status',
        name=u'iphone_update_new_channel_status'),
    url(regex='^iphone/channels$', view='iphone.channels', name=u'iphone_channels',
        kwargs={'cust_ch_name': u'iphone channel_page channel-sort'}),
    url(regex='^iphone/add/new_channels$', view='iphone.add_new_channel', name=u'iphone_add_new_channel',
        kwargs={'cust_ch_name': u'iphone channel_page new_channel-add'}),
    url(regex='^iphone/delete/new_channel/(\d+)$', view='iphone.delete_new_channel', name=u'iphone_delete_new_channel',
        kwargs={'cust_ch_name': u'iphone channel_page new_channel-delete'}),
    url(regex='^iphone/query/new_channel/(\d+)$', view='iphone.query_new_channel', name=u'iphone_query_new_channel',
        kwargs={'cust_ch_name': u'iphone channel_page new_channel-query'}),
    url(regex='^iphone/update/new_channel$', view='iphone.update_new_channel', name=u'iphone_update_new_channel',
        kwargs={'cust_ch_name': u'iphone channel_page new_channel-update'}),
    url(regex='^iphone/channel/publish$', view='iphone.channel_publish', name=u'iphone_channel_publish',
        kwargs={'cust_ch_name': u'iphone channel_page channel-publish'}),
    # channel_video
    url(regex='^iphone/channel_videos$', view='iphone.channel_videos', name=u'iphone_channel_videos'),
    url(regex='^iphone/add/channel_videos$', view='iphone.add_channel_video', name=u'iphone_add_channel_video'),
    url(regex='^iphone/delete/channel_video/(\d+)$', view='iphone.delete_channel_video',
        name=u'iphone_delete_channel_video'),
    #kwargs={'cust_ch_name': u'iphone channel_page channel channel_video video-delete'}),
    url(regex='^iphone/query/channel_video/(\d+)$', view='iphone.query_channel_video',
        name=u'iphone_query_channel_video'),
    url(regex='^iphone/update/channel_video$', view='iphone.update_channel_video', name=u'iphone_update_channel_video'),
    url(regex='^iphone/update_status/channel_video$', view='iphone.update_channel_video_status',
        name=u'iphone_update_channel_video_status'),

    # iphone subchanneltag管理
    url(regex='^iphone/channel/subchannels$', view='iphone.subchannels', name=u'iphone_sub_channels',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel-sort'}),
    url(regex='^iphone/add/subchannel$', view='iphone.add_subchannel', name=u'iphone_add_sub_channel',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel-add'}),
    url(regex='^iphone/delete/subchannel$', view='iphone.delete_subchannel', name=u'iphone_delete_sub_channel',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel-delete'}),
    url(regex='^iphone/query/subchannel$', view='iphone.query_subchannel', name=u'iphone_query_sub_channel',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel-query'}),
    url(regex='^iphone/update/subchannel$', view='iphone.update_subchannel', name=u'iphone_update_sub_channel',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel-update'}),
    url(regex='^iphone/update_status/subchannel$', view='iphone.update_subchannel_status',
        name=u'iphone_update_sub_channel_status'),
    url(regex='^iphone/subchannel/publish$', view='iphone.sub_channel_publish', name=u'iphone_subchannel_publish'),

    # iphone subchannelmodule管理v4.x
    url(regex='^iphone/subchannel/modules_v4$', view='iphone.subchannel_modules_v4',
        name=u'iphone_sub_channel_modules_v4',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4-sort'}),
    url(regex='^iphone/add/subchannel/module_v4$', view='iphone.add_subchannel_module_v4',
        name=u'iphone_add_sub_channel_module_v4',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4-add'}),
    url(regex='^iphone/delete/subchannel/module_v4$', view='iphone.delete_subchannel_module_v4',
        name=u'iphone_delete_sub_channel_module_v4',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4-delete'}),
    url(regex='^iphone/query/subchannel/module_v4$', view='iphone.query_subchannel_module_v4',
        name=u'iphone_query_sub_channel_module_v4',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4-query'}),
    url(regex='^iphone/update/subchannel/module_v4$', view='iphone.update_subchannel_module_v4',
        name=u'iphone_update_sub_channel_module_v4',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4-update'}),
    url(regex='^iphone/update_status/subchannel/module_v4$', view='iphone.update_subchannel_module_status_v4',
        name=u'iphone_update_sub_channel_module_v4_status'),

    # iphone subchannelmodulevideo管理v4.x
    url(regex='^iphone/subchannel/module_v4/items$', view='iphone.subchannel_module_v4_items',
        name=u'iphone_sub_channel_module_v4_items',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4 video-sort'}),
    url(regex='^iphone/add/subchannel/module_v4/item$', view='iphone.add_subchannel_module_v4_item',
        name=u'iphone_add_sub_channel_module_v4_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4 video-add'}),
    url(regex='^iphone/delete/subchannel/module_v4/item$', view='iphone.delete_subchannel_module_v4_item',
        name=u'iphone_delete_sub_channel_module_v4_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4 video-delete'}),
    url(regex='^iphone/query/subchannel/module_v4/item$', view='iphone.query_subchannel_module_v4_item',
        name=u'iphone_query_sub_channel_module_v4_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4 video-query'}),
    url(regex='^iphone/update/subchannel/module_v4/item$', view='iphone.update_subchannel_module_v4_item',
        name=u'iphone_update_sub_channel_module_v4_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel modulev4 video-update'}),
    url(regex='^iphone/update_status/subchannel/module_v4/item$', view='iphone.update_subchannel_module_v4_item_status',
        name=u'iphone_update_subchannel_module_v4_item_status'),
    url(regex='^iphone/update_batch/subchannel/module_v4/item$', view='iphone.update_v4_batch_items',
        name=u'iphone_mod_v4_update_batch_items'),

    # iphone subchannelmodule管理v3.x
    url(regex='^iphone/subchannel/modules$', view='iphone.subchannel_modules', name=u'iphone_sub_channel_modules',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module-update'}),
    url(regex='^iphone/add/subchannel/module$', view='iphone.add_subchannel_module',
        name=u'iphone_add_sub_channel_module', kwargs={'cust_ch_name': u'iphone channel_page subchannel module-add'}),
    url(regex='^iphone/delete/subchannel/module$', view='iphone.delete_subchannel_module',
        name=u'iphone_delete_sub_channel_module',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module-delete'}),
    url(regex='^iphone/query/subchannel/module$', view='iphone.query_subchannel_module',
        name=u'iphone_query_sub_channel_module',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module-query'}),
    url(regex='^iphone/update/subchannel/module$', view='iphone.update_subchannel_module',
        name=u'iphone_update_sub_channel_module',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module-update'}),
    url(regex='^iphone/update_status/subchannel/module$', view='iphone.update_subchannel_module_status',
        name=u'iphone_update_sub_channel_module_status'),
    url(regex='^iphone/update_batch/subchannel/module/item$', view='iphone.update_batch_items',
        name=u'iphone_update_batch_items'),

    # subchannel subchannelmodulevideo管理v3.x
    url(regex='^iphone/subchannel/module/items$', view='iphone.subchannel_module_items',
        name=u'iphone_sub_channel_module_items',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module video-sort'}),
    url(regex='^iphone/add/subchannel/module/item$', view='iphone.add_subchannel_module_item',
        name=u'iphone_add_sub_channel_module_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module video-add'}),
    url(regex='^iphone/delete/subchannel/module/item$', view='iphone.delete_subchannel_module_item',
        name=u'iphone_delete_sub_channel_module_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module video-delete'}),
    url(regex='^iphone/query/subchannel/module/item$', view='iphone.query_subchannel_module_item',
        name=u'iphone_query_sub_channel_module_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module video-query'}),
    url(regex='^iphone/update/subchannel/module/item$', view='iphone.update_subchannel_module_item',
        name=u'iphone_update_sub_channel_module_item',
        kwargs={'cust_ch_name': u'iphone channel_page subchannel module video-update'}),
    url(regex='^iphone/update_status/subchannel/module/item$', view='iphone.update_subchannel_module_item_status',
        name=u'iphone_update_sub_channel_module_status_item'),
    url(regex='^iphone/update_item_value/subchannel/module/item$', view='iphone.update_subchannel_module_item_value',
        name=u'iphone_update_item_value_sub_channel_module_item'),
    url(regex='^iphone/channel_page/add/video_field$', view='iphone.channel_page_add_video_fields',
        name=u'iphone_add_video_fields'),
    url(regex='^iphone/update_video_value/fixed_position_video$', view='iphone.update_fixed_position_video_value',
        name=u'iphone_update_fixed_position_video_value'),
    url(regex='^iphone/get_img_desc$', view='iphone.get_img_desc', name='iphone_get_img_desc'),


    # Androidchannel_page
    url(regex='^android/channels$', view='android.channels', name=u'android_channels',
        kwargs={'cust_ch_name': u'android channel_page channel-sort'}),
    url(regex='^android/add/channels$', view='android.add_channel', name=u'android_add_channel',
        kwargs={'cust_ch_name': u'android channel_page channel-add'}),
    url(regex='^android/update_status/channel$', view='android.update_channel_status',
        name=u'android_update_channel_status'),
    url(regex='^android/delete/channel/(\d+)$', view='android.delete_channel', name=u'android_delete_channel',
        kwargs={'cust_ch_name': u'android channel_page channel-delete'}),
    url(regex='^android/query/channel/(\d+)$', view='android.query_channel', name=u'android_query_channel',
        kwargs={'cust_ch_name': u'android channel_page channel-query'}),
    url(regex='^android/update/channel$', view='android.update_channel', name=u'android_update_channel',
        kwargs={'cust_ch_name': u'android channel_page channel-update'}),


    url(regex='^android/new_channels$', view='android.new_channels', name=u'android_new_channels'),
    url(regex='^android/update_status/new_channel$', view='android.update_new_channel_status',
        name=u'android_update_new_channel_status'),
    url(regex='^android/channels$', view='android.channels', name=u'android_channels',
        kwargs={'cust_ch_name': u'android channel_page channel-sort'}),
    url(regex='^android/add/new_channels$', view='android.add_new_channel', name=u'android_add_new_channel',
        kwargs={'cust_ch_name': u'android channel_page new_channel-add'}),
    url(regex='^android/delete/new_channel/(\d+)$', view='android.delete_new_channel',
        name=u'android_delete_new_channel', kwargs={'cust_ch_name': u'android channel_page new_channel-delete'}),
    url(regex='^android/query/new_channel/(\d+)$', view='android.query_new_channel', name=u'android_query_new_channel',
        kwargs={'cust_ch_name': u'android channel_page new_channel-query'}),
    url(regex='^android/update/new_channel$', view='android.update_new_channel', name=u'android_update_new_channel',
        kwargs={'cust_ch_name': u'android channel_page new_channel-update'}),

    ###################################################################
    #### 频道页发布视频
    ##################################################################
    url(regex='^android/channel/publish$', view='android.channel_publish',
        name=u'android_channel_page_publish'),
    # channel_video
    url(regex='^android/channel_videos$', view='android.channel_videos', name=u'android_channel_videos'),
    url(regex='^android/add/channel_videos$', view='android.add_channel_video', name=u'android_add_channel_video'),
    url(regex='^android/delete/channel_video/(\d+)$', view='android.delete_channel_video',
        name=u'android_delete_channel_video'),
    #kwargs={'cust_ch_name': u'android channel_page channel channel_video video-delete'}),
    url(regex='^android/query/channel_video/(\d+)$', view='android.query_channel_video',
        name=u'android_query_channel_video'),
    url(regex='^android/update/channel_video$', view='android.update_channel_video',
        name=u'android_update_channel_video'),
    url(regex='^android/update_status/channel_video$', view='android.update_channel_video_status',
        name=u'android_update_channel_video_status'),
    url(regex='^android/update_video_value/channel_video$', view='android.update_channel_video_value',
        name=u'android_update_channel_video_value'),
    url(regex='^android/channel_video/add/video_field$', view='android.channel_video_add_video_fields',
        name=u'android_add_video_fields'),
    #android频道导航
    url(regex='^android/channel_navigation$', view='android.channel_navigation', name=u'android_channel_navigation'),
    url(regex='^android/add_channel_navigation$',
        view='android.add_channel_navigation', name=u'android_add_channel_navigation'),
    url(regex='^android/update_channel_navigation/(\d+)$', view='android.update_channel_navigation',
        name=u'android_update_channel_navigation'),
    url(regex='^android/delete_channel_navigation/(\d+)$', view='android.delete_channel_navigation',
        name=u'android_delete_channel_navigation'),
    url(regex='^android/update_status_channel_navigation$', view='android.update_status_channel_navigation',
        name=u'android_update_status_channel_navigation'),


    # subchannel subchanneltag管理
    url(regex='^android/channel/subchannels$', view='android.subchannels', name=u'android_sub_channel',
        kwargs={'cust_ch_name': u'android channel_page subchannel-sort'}),
    url(regex='^android/add/subchannel$', view='android.add_subchannel', name=u'android_add_sub_channel',
        kwargs={'cust_ch_name': u'android channel_page subchannel-add'}),
    url(regex='^android/delete/subchannel$', view='android.delete_subchannel', name=u'android_delete_sub_channel',
        kwargs={'cust_ch_name': u'android channel_page subchannel-delete'}),
    url(regex='^android/query/subchannel$', view='android.query_subchannel', name=u'android_query_sub_channel',
        kwargs={'cust_ch_name': u'android channel_page subchannel-query'}),
    url(regex='^android/update/subchannel$', view='android.update_subchannel', name=u'android_update_sub_channel',
        kwargs={'cust_ch_name': u'android channel_page subchannel-update'}),
    url(regex='^android/update_status/subchannel$', view='android.update_subchannel_status',
        name=u'android_update_sub_channel_status'),
    url(regex='^android/update_highlight/subchannel$', view='android.update_subchannel_highlight',
        name=u'android_update_sub_channel_highlight'),

    # subchannel subchannelmodule管理
    url(regex='^android/subchannel/modules$', view='android.subchannel_modules', name=u'android_sub_channel_modules',
        kwargs={'cust_ch_name': u'android channel_page subchannel module-sort'}),
    url(regex='^android/add/subchannel/module$', view='android.add_subchannel_module',
        name=u'android_add_sub_channel_module', kwargs={'cust_ch_name': u'android channel_page subchannel module-add'}),
    url(regex='^android/delete/subchannel/module$', view='android.delete_subchannel_module',
        name=u'android_delete_sub_channel_module',
        kwargs={'cust_ch_name': u'android channel_page subchannel module-delete'}),
    url(regex='^android/query/subchannel/module$', view='android.query_subchannel_module',
        name=u'android_query_sub_channel_module',
        kwargs={'cust_ch_name': u'android channel_page subchannel module-query'}),
    url(regex='^android/update/subchannel/module$', view='android.update_subchannel_module',
        name=u'android_update_sub_channel_module',
        kwargs={'cust_ch_name': u'android channel_page subchannel module-update'}),
    url(regex='^android/update_status/subchannel/module$', view='android.update_subchannel_module_status',
        name=u'android_update_sub_channel_module_status'),
    url(regex='^android/subchannel/publish', view='android.sub_channel_publish', name='android_subchannel_publish'),

    # subchannel subchannelmodulevideo管理
    url(regex='^android/subchannel/module/items$', view='android.subchannel_module_items',
        name=u'android_sub_channel_module_items',
        kwargs={'cust_ch_name': u'android channel_page subchannel module video-sort'}),
    url(regex='^android/add/subchannel/module/item$', view='android.add_subchannel_module_item',
        name=u'android_add_sub_channel_module_item',
        kwargs={'cust_ch_name': u'android channel_page subchannel module video-add'}),
    url(regex='^android/delete/subchannel/module/item$', view='android.delete_subchannel_module_item',
        name=u'android_delete_sub_channel_module_item',
        kwargs={'cust_ch_name': u'android channel_page subchannel module video-delete'}),
    url(regex='^android/query/subchannel/module/item$', view='android.query_subchannel_module_item',
        name=u'android_query_sub_channel_module_item',
        kwargs={'cust_ch_name': u'android channel_page subchannel module video-query'}),
    url(regex='^android/update/subchannel/module/item$', view='android.update_subchannel_module_item',
        name=u'android_update_sub_channel_module_item',
        kwargs={'cust_ch_name': u'android channel_page subchannel module video-update'}),
    url(regex='^android/update_status/subchannel/module/item$', view='android.update_subchannel_module_item_status',
        name=u'android_update_sub_channel_module_status_item'),
    url(regex='^android/update_item_value/subchannel/module/item$', view='android.update_subchannel_module_item_value',
        name=u'android_update_item_value_sub_channel_module_item'),
    url(regex='^android/update_batch/subchannel/module/item$', view='android.update_batch_items',
        name=u'android_update_batch_items'),
    url(regex='android/channel_page/add/video_field$', view='android.channel_page_add_video_fields',
        name=u'android_add_video_fields'),

    # android固定位置视频管理
    url(regex='^android/fixed_position_videos$', view='android.fixed_position_videos',
        name=u'android_fixed_position_videos', kwargs={'cust_ch_name': u'android fixed_position_video video-sort'}),
    url(regex='^android/add/fixed_position_video$', view='android.add_fixed_position_video',
        name=u'android_add_fixed_position_video', kwargs={'cust_ch_name': u'android fixed_position_video video-add'}),
    url(regex='^android/delete/fixed_position_video$', view='android.delete_fixed_position_video',
        name=u'android_delete_fixed_position_video',
        kwargs={'cust_ch_name': u'android fixed_position_video video-delete'}),
    url(regex='^android/query/fixed_position_video$', view='android.query_fixed_position_video',
        name=u'android_query_fixed_position_video',
        kwargs={'cust_ch_name': u'android fixed_position_video video-query'}),
    url(regex='^android/update/fixed_position_video$', view='android.update_fixed_position_video',
        name=u'android_update_fixed_position_video',
        kwargs={'cust_ch_name': u'android fixed_position_video video-update'}),
    url(regex='^android/update_video_value/fixed_position_video$', view='android.update_fixed_position_video_value',
        name=u'android_update_fixed_position_video_value'),
    url(regex='^android/check_fixed_position/fixed_position_video$', view='android.check_fixed_position',
        name=u'android_check_fixed_position'),

    # iphone fixed pos videos management
    url(regex='^iphone/fixed_position_videos$', view='iphone.fixed_position_videos',
        name='iphone_fixed_position_videos',
        kwargs={'cust_ch_name': u'iphone channel_page fixed-sort'}),
    url(regex='^iphone/add/fixed_position_video$', view='iphone.add_fixed_position_video',
        name='iphone_add_fixed_position_video',
        kwargs={'cust_ch_name': u'iphone channel_page fixed-add'}),
    url(regex='^iphone/query/fixed_position_video$', view='iphone.query_fixed_position_video',
        name='iphone_query_fixed_position_video'),
    url(regex='^iphone/update/fixed_position_video$', view='iphone.update_fixed_position_video',
        name='iphone_update_fixed_position_video',
        kwargs={'cust_ch_name': u'iphone channel_page fixed-update'}),
    url(regex='^iphone/delete/fixed_position_video$', view='iphone.delete_fixed_position_video',
        name='iphone_delete_fixed_position_video',
        kwargs={'cust_ch_name': u'iphone channel_page fixed-delete'}),


    #log 用户操作记录
    url(regex='^user_action/logs$', view='user_action_index', name=u'log_index'),
    url(regex='^user_action/log_filters$', view='log_form_selectors', name=u'log_filters'),
    # sth for local test, should be deleted
    #url(regex='^android/test$', view='android.test', name=u'android_test_api'),

    #公共盒子
    url(regex='^common_content/boxes$', view='home_common.common_box.boxes',
        name=u'home_common_boxes', kwargs={'cust_ch_name': u'common main_page module-sort'}),
    url(regex='^common_content/add_box$', view='home_common.common_box.add_box',
        name=u'home_common_boxes_add_box', kwargs={'cust_ch_name': u'common main_page module-add'}),
    url(regex='^common_content/box/update_status$', view='home_common.common_box.update_status',
        name=u'home_common_boxes_update_status'),
    url(regex='^common_content/box/update_box_title$', view='home_common.common_box.update_box_title',
        name=u'home_common_boxes_update_box_title'),
    url(regex='^common_content/current_box_page/(\d+)/box/(\d+)/videos$', view='home_common.common_box.videos_in_box',
        name=u'home_common_boxes_videos_in_box', kwargs={'cust_ch_name': u'common main_page module video-sort'}),
    url(regex='^common_content/box/box_sync/(\d+)$', view='home_common.common_box.box_sync',
        name=u'home_common_boxes_box_sync', kwargs={'cust_ch_name': u'common main_page module-sync'}),
    url(regex='^common_content/box/(\d+)/update_box$', view='home_common.common_box.update_box',
        name=u'home_common_boxes_update_box', kwargs={'cust_ch_name': u'common main_page module-update'}),
    url(regex='^common_content/box/(\d+)/delete_box$', view='home_common.common_box.delete_box',
        name=u'home_common_boxes_delete_box', kwargs={'cust_ch_name': u'common main_page module-delete'}),

    #公共视频
    url(regex='^common_content/current_box_page/(\d+)/box/(\d+)/videos/add_video$',
        view='home_common.common_video.add_video', name=u'home_common_videos_add_video',
        kwargs={'cust_ch_name': u'common main_page module video-add'}),
    url(regex='^common_content/video/add_video_fields$', view='home_common.common_video.add_video_fields',
        name=u'home_common_videos_add_video_fields'),
    url(regex='^common_content/current_box_page/(\d+)/box/(\d+)/video/(\d+)/update_video$',
        view='home_common.common_video.update_video', name=u'home_common_videos_update_video',
        kwargs={'cust_ch_name': u'common main_page module video-update'}),
    url(regex='^common_content/current_box_page/update_video_value$',
        view='home_common.common_video.update_video_value', name=u'home_common_videos_update_video_value'),
    url(regex='^common_content/current_box_page/(\d+)/box/(\d+)/video/(\d+)/delete_video$',
        view='home_common.common_video.delete_video', name=u'home_common_videos_delete_video',
        kwargs={'cust_ch_name': u'common main_page module video-delete'}),
    url(regex='^common_content/box_videos/sync$', view='home_common.common_video.sync_box_videos',
        name=u'home_common_videos_sync_box_videos', kwargs={'cust_ch_name': u'common main_page module video-sync'}),
    url(regex='^common_content/video/update_status$', view='home_common.common_video.update_status',
        name=u'home_common_videos_update_status'),

    url(regex='^versions$', view='version.versions', name=u'versions'),
    url(regex='^version/delete$', view='version.version_delete', name=u'version_delete'),
    url(regex='^version/add$', view='version.version_add', name=u'version_add'),

    url(regex='^features$', view='version.features', name=u'features'),
    url(regex='^feature/delete$', view='version.feature_delete', name=u'feature_delete'),
    url(regex='^feature/add$', view='version.feature_add', name=u'feature_add'),
    url(regex='^feature/edit$', view='version.feature_edit', name=u'feature_edit'),

    url(regex='^cids$', view='cid_manage.cids', name='cids'),
    url(regex='^cid/edit$', view='cid_manage.cid_edit', name='cid_edit'),
    url(regex='^cid/add$', view='cid_manage.add_cid', name='cid_add'),

    #################################################
    ######发布视频
    #################################################
    url(regex='^iphone/main_page/publish$', view='iphone.main_page_publish', name=u'iphone_main_page_publish',
        kwargs={'cust_ch_name': u'iphone main_page publish-publish'}),
    url(regex='^android/main_page/publish$', view='android.main_page_publish', name=u'android_main_page_publish',
        kwargs={'cust_ch_name': u'android main_page publish-publish'}),
    url(regex='^ipad/main_page/publish$', view='ipad.main_page_publish', name=u'ipad_main_page_publish',
        kwargs={'cust_ch_name': u'ipad main_page publish-publish'}),
    url(regex='^winphone/main_page/publish$', view='winphone.main_page_publish', name=u'winphone_main_page_publish',
        kwargs={'cust_ch_name': u'winphone main_page publish-publish'}),

    # url(regex='^perm$', view='perm.perm_index', name=u'permission_index'),

    #################################################
    ######品牌官网
    #################################################
    # brand module
    url(regex='^brand/brand_modules$', view='brand.brand_module.modules', name=u'brand_modules',
        kwargs={'cust_ch_name': u'common channel_page brand module-sort'}),
    url(regex='^brand/brand_module/add_module$', view='brand.brand_module.add_module', name=u'brand_add_module',
        kwargs={'cust_ch_name': u'common channel_page brand module-add'}),
    url(regex='^brand/brand_module/select_channel$', view='brand.brand_module.select_channel',
        name=u'brand_select_module'),
    url(regex='^brand/brand_module/update_module/(\d+)$', view='brand.brand_module.update_module',
        name=u'brand_update_module', kwargs={'cust_ch_name': u'common channel_page brand module-update'}),
    url(regex='^brand/brand_module/delete_module/(\d+)$', view='brand.brand_module.delete_module',
        name=u'brand_delete_module', kwargs={'cust_ch_name': u'common channel_page brand module-delete'}),
    #brand video
    url(regex='^brand/brand_videos$', view='brand.brand_video.videos', name=u'brand_videos',
        kwargs={'cust_ch_name': u'common channel_page brand video-delete'}),
    url(regex='^brand/brand_video/add_video$', view='brand.brand_video.add_video', name=u'brand_add_video',
        kwargs={'cust_ch_name': u'common channel_page brand video-add'}),
    url(regex='^brand/brand_video/update_video/(\d+)$', view='brand.brand_video.update_video',
        name=u'brand_update_video',
        kwargs={'cust_ch_name': u'common channel_page brand video-update'}),
    url(regex='^brand/brand_video/delete_video/(\d+)$', view='brand.brand_video.delete_video',
        name=u'brand_delete_video',
        kwargs={'cust_ch_name': u'common channel_page brand video-delete'}),
    url(regex='^brand/brand_video/update_status$', view='brand.brand_video.update_status', name=u'brand_update_status'),
    url(regex='^brand/brand_video/add_fields$', view='brand.brand_video.add_fields', name=u'brand_add_fields'),


    #在创建精选子频道之前检查该频道下是否已有精选子频道
    url(regex='^check_if_has_selected_subchannel$', view='check_if_has_selected_subchannel', name=u'判断频道下是否已有精选子频道'),


    #搜索背景图
    url(regex='^search/back_img$', view='search_back_img', name=u'search_back_img_manage'),
    url(regex='^search/back_img/add_video$', view='search_back_img_add_video', name=u'search_back_img_add_video'),
    url(regex='^search/back_img/add_fields$', view='search_back_img_add_fields', name=u'search_back_img_add_fields'),
    url(regex='^search/back_img/update_video/(\d+)$', view='search_back_img_update_video', name=u'search_back_img_update_video'),
    url(regex='^search/back_img/delete_video/(\d+)$', view='search_back_img_delete_video', name=u'search_back_img_delete_video'),
    url(regex='^search/back_img/update_status', view='search_back_img_update_status', name=u'search_back_img_update_status'),

    #会员商品页背景图
    url(regex='^vip_goods_page/back_img$', view='vip_goods_back_img', name=u'vip_goods_page_back_img_manage'),
    url(regex='^vip_goods_page/back_img/add_img$', view='vip_goods_back_img_add_img', name=u'vip_goods_back_img_add_img'),
    url(regex='^vip_goods_page/back_img/update_img/(\d+)$', view='vip_goods_back_img_update_img', name=u'vip_goods_back_img_update_img'),
    url(regex='^vip_goods_page/back_img/delete_img/(\d+)$', view='vip_goods_back_img_delete_img', name=u'vip_goods_back_img_delete_img'),
    url(regex='^vip_goods_page/back_img/update_status$', view='vip_goods_back_img_update_status', name=u'vip_goods_back_img_update_status'),
)

customized_urlpatterns = []
for item in urlpatterns:
    """
    attribute in class RegexURLPattern
    {'_regex_dict': {}, '_callback': None, 'name': u'ipad_query_channel',
    '_callback_str': u'content.views.ipad.query_channel', '_regex': 'ipad/query/channel/(\\d+)$', 'default_args': {}}
    """
    customized_urlpatterns.append(
        customized_url(
            item.__dict__['_regex'], item.__dict__['_callback_str'], item.default_args, item.name
        )
    )
urlpatterns = customized_urlpatterns
