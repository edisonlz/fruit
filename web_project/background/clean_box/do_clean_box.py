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

from app.content.models import AndroidBoxVideo, IpadBoxVideo, IphoneBoxVideo, WinPhoneBoxVideo
from app.content.models import IphoneHomePublishedVideo, AndroidHomePublishedVideo, IpadHomePublishedVideo, \
    WinPhonePublishedVideo
from app.content.models import HomeBox, VideoType, Platform
from django.db.models import Max
import re
from app.content.lib.main_page_publish_tool import MainPagePublishTool
from redis_model.queue import Worker
from base.core.dateutils import *
import json
import time


def do_clean_box(data):
    print "**Recieve data: ", data

    # you should import required video/box class first
    box_id = data["box_id"]
    box_class = eval(data["box_class"])
    box = box_class.objects.get(id=box_id)
    publish_video_class = eval(data['video_class'])
    max_position_for_each_box = data["max_position_for_each_box"]
    max_video_count_for_each_box = data["max_video_count_for_each_box"]

    publish_video_class.tighten_position_in_box(box, max_position_for_each_box)

    publish_video_class.remove_redundant_videos_in_box(box, max_video_count_for_each_box)


if __name__ == "__main__":
    worker = Worker("cache.do_clean_box")
    try:
        worker.register(do_clean_box)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e

