#coding=utf-8
import os,sys
import re , string
import base64


def encodevid(vid):
    """
    encode vid from int to str
    """
    
    try:
        return 'X{0}'.format(base64.b64encode(str(long(vid) << 2)))
    except ValueError:
        return vid


def decodevid(vid):
    """
    decode vid from string to int
    """
    
    if isinstance(vid, (int, long)) or str(vid).isdigit():
        return long(vid)
    else:
        try:
            return long(base64.b64decode(vid[1:])) >> 2
        except TypeError:
            return 0L


def isvid(vid):
    """
    is video id
    
    :param str vid: youku video id
    :return: true or false
    """
    if not isinstance(vid, (int, long, basestring)):
        return False

    if isinstance(vid, basestring):
        if not (vid.isdigit() or vid.startswith('X')):
            return False

    longid = 0L
    try:
        longid = decodevid(vid)
    except:
        longid = 0L

    return longid > 0


def isshowid(showid):
    """
    is show id
    
    :param str show: youku show id
    :return: true or false
    
    """
    _p_showid = re.compile(r'^[a-f0-9]{20}$')
    return bool(_p_showid.match(showid))
