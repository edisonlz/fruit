#coding=utf-8
import re


def parse_item_id_and_type(url):
    """
    分析url中的video id, e.g.:
    http://v.youku.com/v_show/id_XODc3ODYxODM2.html
    http://v.youku.com/v_show/id_XODc3ODYxODM2_ev_5.html
    """

    pat = re.compile('id_(.*)\.html')
    match = pat.search(url)
    if match:
        item_id = match.group(1).split('_')[0]
        if item_id.startswith('z'):  # show
            return item_id[1:], 'show'
        elif item_id.startswith('X'):  # video
            return item_id, 'video'
        else:  # default playlist
            return item_id, 'playlist'


def parse_user_id(url):
    '''
    分析url中得user_id
    e.g.:
    http://i.youku.com/u/UNjk1NTI0MDA=
    http://i.youku.com/u/UMzc4MDYzNzA4?param=something
    '''
    pass