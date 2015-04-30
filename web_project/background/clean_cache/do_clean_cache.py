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

def do_clean(data):
    print "**Recieve data: ", data
    
    key = data["key"]
    params = data["params"]
    delay_seconds = data["delay_seconds"]
    #delay cache expire time varnish 1m , cms api cache 1m
    #time.sleep(delay_seconds)
    time.sleep(3.5)
    CachePlan.do_clean_cache(key, params)

    


if __name__ == "__main__":
    worker = Worker("cache.do_clean")
    try:
        worker.register(do_clean)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e

