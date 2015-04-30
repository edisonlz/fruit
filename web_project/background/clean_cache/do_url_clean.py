# coding=utf-8

import os, sys

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

sys.path.insert(0, os.path.join(PROJECT_ROOT, os.pardir))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../..')))
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__), '../../../..')))

from base.settings import load_django_settings

load_django_settings('m-cms-new.base', 'm-cms-new.app')

from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned
import json
import logging

from redis_model.queue import Worker
from base.core.dateutils import *
from app.content.lib.cache_plan import CachePlan
import json
import time
import urllib2
import socket

def do_url_clean(data):
    print "**Recieve data: ", data

    url = data["url"]
    user_agents = data.get("user_agents",['Youku HD;3.3;Android;4.1.1;MI-ONE C1',])
    try:
        for ua in user_agents:
            request = urllib2.Request(url)
            request.add_header('User-Agent', ua)
            request.add_header('Is-Update-Cache', 'YES')
            try:
                response = urllib2.urlopen(request, timeout=5).read()
                data = json.loads(response)
            except socket.timeout ,e:
                logging.error(e)
                #read one more
                response = urllib2.urlopen(request, timeout=5).read()
                data = json.loads(response)
            print "url is %s" % url
            print "ua is %s" % ua
            print "result is %s " % data['status']
            print "****************************"

    except Exception, e:
        if hasattr(e, 'code'):
            print e.code
        else:
            print e
    


if __name__ == "__main__":
    worker = Worker("cache.do_url_clean")
    try:
        worker.register(do_url_clean)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e

