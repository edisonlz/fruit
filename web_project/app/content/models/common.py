#coding=utf-8

class Status(object):
    StatusOpen = 1
    StatusClose = 0
    STATUS_HASH = {
        StatusClose: u'关闭',
        StatusOpen: u'开启'
    }
    STATUS = [
        (StatusClose, u'关闭'),
        (StatusOpen, u'开启'),
    ]