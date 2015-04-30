# -*- coding: utf-8 -*-
from api.util.file_size import humanreadable_file_size

def format_app(app_obj, on_board=True):

    slide_pics = filter(lambda x:bool(x),[app_obj.screenshot_1,app_obj.screenshot_2,app_obj.screenshot_3,app_obj.screenshot_4,app_obj.screenshot_5,app_obj.screenshot_6])

    if hasattr(app_obj, 'categories'):
        categories = app_obj.categories
    else:
        categories = u'益智'

    return {
        "id": app_obj.id,
        "type": categories,
        "update_version_time":app_obj.upload_time.strftime("%Y-%m-%d"),
        "icon":app_obj.logo,
        "desc":app_obj.desc,
        "short_desc": app_obj.short_desc,
        "size": humanreadable_file_size(app_obj.size),
        "slide_pics": slide_pics,
        "slide_pic_type": app_obj.screenshot_type,
        "month_download_times": app_obj.stats.total_downloads + app_obj.init_download_amount,
        "download_link": app_obj.china_cache_publish_url,
        "pkg_id": app_obj.package,
        "pkg_activity": app_obj.activity,
        "pkg_ver": app_obj.ver_code,
        "pkg_ver_name": app_obj.version,
        "pic": app_obj.scoller,
        "name": app_obj.appname,
        "on_board": on_board, #是否在tab中
        "score":float(app_obj.score)/2,
    }


def convert_category_apps(app):
    pass


def convert_app(app):
    slide_pics = filter(lambda x:bool(x),[app.screenshot_1,app.screenshot_2,app.screenshot_3,app.screenshot_4,app.screenshot_5,app.screenshot_6])
    tmp = {}
    tmp['id'] = app.id
    tmp['appname'] = app.appname
    tmp['version'] = app.version
    tmp['ver_code'] = app.ver_code
    tmp['logo'] = app.logo
    tmp['scoller'] = app.scoller2
    tmp['package'] = app.package

    #tmp['app_source_url'] = app.app_source_url
    tmp['md5'] = app.md5
    tmp['download_link'] = app.china_cache_publish_url
    #tmp['short_desc'] = app.short_desc
    #tmp['app_status'] = app.app_status
    tmp['on_board'] = True if app.app_status else False
    tmp['upload_time'] = app.upload_time.strftime('%Y-%m-%d')
    tmp['size'] = humanreadable_file_size(app.size)
    #tmp['created_time'] = app.created_time.strftime('%Y-%m-%d')
    #tmp['oid'] = app.oid
    tmp['activity'] = app.activity
    #tmp['screenshot'] = slide_pics
    #tmp['screenshot_type'] = app.screenshot_type
    tmp['total_downloads'] = app.stats.total_downloads + app.init_download_amount
    tmp['score'] = float(app.score)/2

    if app.recommend_type:
        tmp["recommend_type"] = app.recommend_type.id
    else:
        tmp["recommend_type"] = ''

    return tmp



def convert_detail(app, on_board=True):

    slide_pics = filter(lambda x:bool(x),[app.screenshot_1,app.screenshot_2,app.screenshot_3,app.screenshot_4,app.screenshot_5,app.screenshot_6])

    if hasattr(app, 'categories'):
        categories = app.categories
    else:
        categories = u'益智'

    tmp = {}
    tmp['id'] = app.id
    tmp['appname'] = app.appname
    tmp['version'] = app.version
    tmp['ver_code'] = app.ver_code
    tmp['logo'] = app.logo
    tmp['scoller'] = app.scoller2
    tmp['package'] = app.package
    #tmp['app_source_url'] = app.app_source_url
    tmp['md5'] = app.md5
    tmp['download_link'] = app.china_cache_publish_url
    tmp['desc'] = app.desc
    tmp['short_desc'] = app.short_desc
    #tmp['app_status'] = app.app_status
    tmp['upload_time'] = app.upload_time.strftime('%Y-%m-%d')
    tmp['size'] = humanreadable_file_size(app.size)
    #tmp['created_time'] = app.created_time.strftime('%Y-%m-%d')
    #tmp['oid'] = app.oid
    tmp['activity'] = app.activity
    tmp['screenshot'] = slide_pics
    tmp['score'] = float(app.score)/2
    tmp['type'] = categories
    tmp['on_board'] = on_board
    tmp["type"] = categories
    tmp['total_downloads'] = app.stats.total_downloads + app.init_download_amount
    tmp["slide_pic_type"] = app.screenshot_type
    tmp['vids'] = app.vids
    if app.recommend_type:
        tmp["recommend_type"] = app.recommend_type.id
    else:
        tmp["recommend_type"] = ''

    return tmp


def convert_rank_app(app):

    game_infos = {}
    game_infos["id"] = int(app.id)
    game_infos['ver_code'] = app.ver_code
    game_infos["appname"] = app.appname
    game_infos["logo"] = app.logo
    game_infos["upload_time"] = app.upload_time.strftime("%Y-%m-%d")
    game_infos["total_downloads"] = int(app.num)#app.stats.total_downloads + app.stats.init_download_amount
    game_infos["size"] = humanreadable_file_size(app.size)
    game_infos["score"] = float(app.score)/2

    game_infos["recommend_type"] = app.recommend_type_id if app.recommend_type_id else ''
    game_infos['package'] = app.package
    game_infos['download_link'] = app.china_cache_publish_url
    game_infos["rank"] = app.rank

    return game_infos

def ios_convert_app(app, seq, recwd=None):
    tmp = {}
    tmp['id'] = int(app.id)
    tmp['appname'] = app.appname
    tmp['logo'] = app.logo
    tmp['scroller'] = app.scoller
    tmp['upload_time'] = app.upload_time.strftime("%Y-%m-%d")
    tmp['init_downloads'] = app.init_download_amount
    tmp["size"] = humanreadable_file_size(app.size)
    tmp["score"] = "%.1f" % (float(app.score)/2)
    tmp["recommend_type"] = app.recommend_type_id if app.recommend_type_id else ''
    if recwd and recwd != '':
        tmp['desc'] = recwd
    else:
        tmp['desc'] = app.desc
    tmp['charge'] = app.charge
    tmp['price'] = app.price
    tmp['version'] = app.version
    tmp['url'] = app.ios_url
    tmp['locationid'] = seq

    return tmp