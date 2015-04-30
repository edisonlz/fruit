#!/usr/bin/env python
# -*- coding: utf-8 -*-

def humanreadable_file_size(size):
    for x in [u'字节',u'K',u'M',u'G',u'T']:
        if size < 1024.0:
            return "%3.1f%s" % (size, x)
        size /= 1024.0



