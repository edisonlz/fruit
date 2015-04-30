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

from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Max
from apscheduler.schedulers.blocking import BlockingScheduler
from app.content.management.commands.lib import youku_cms
from app.content.models import *
from base.youkuapi.video import VideoApi
from base.youkuapi.show import ShowApi
from wi_model_util.imodel import get_object_or_none
from app.content.lib.image_helper import ImageHelper
from app.content.lib.model_util import ModelUtil
from hashlib import sha1
import json
import logging
import socket
import re
from redis_model.queue import Client


logging.getLogger('apscheduler.executors.default').addHandler(logging.StreamHandler())

class SyncChannelJob(object):
    """
    频道同步任务
    """

    queue_client = Client()
    
    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.run_jobs = {}
        self.is_run = False
        self.job_sig = {}
        
    @property
    def is_running(self):
        return self.is_run

    def done(self):
        self.is_run = False

    def do(self):
        self.is_run = True

    def loop(self):
        self.scheduler.add_job(self.io_loop, "interval", seconds=5)
        self.scheduler.start()

    def io_loop(self):
        """主函数，循环更新任务"""
        if self.is_running:
            return

        #starting
        self.do()
        last_jobs = self.run_jobs.keys()
        for job in SyncJob.jobs():
            if job.key in last_jobs:
                last_jobs.remove(job.key)

            if self.run_jobs.get(job.key):
                continue
            self.run_jobs[job.key] = True

            #job start
            job_info = {'job': job}
            if job.interval:
                self.scheduler.add_job(self.do_job, trigger="interval",
                                       seconds=job.interval, id=job.key, misfire_grace_time=60,
                                       kwargs=job_info)
            else:
                # hour, minute = job.hour_and_minute
                for cron_job in job.cron_list:
                    self.scheduler.add_job(self.do_job, trigger="cron", id=job.key, misfire_grace_time=60,
                                           hour=cron_job['hour'], minute=cron_job['minute'], kwargs=job_info)

            if job.runatonce:
                job.runatonce = False
                self.do_job(name=job.virtual_name, job=job)
                job.save()

        #delete already admin stop or delete job
        self.stop_job(last_jobs)

        #done.......
        self.done()

    def do_job(self, *args, **kwargs):
        """执行同步任务"""
        job = kwargs["job"]
        print 'send  job', job.id,  job.virtual_name.encode('utf8')
        self.queue_client.dispatch("async.channel.job", {"job_id": job.id})

    def stop_job(self, deleted_jobs):
        for k in deleted_jobs:
            self.scheduler.remove_job(job_id=k)
            del self.run_jobs[k]

if __name__ == "__main__":

    # logging.basicConfig(level=logging.DEBUG)
    # The "apscheduler." prefix is hard coded
    scheduler = BlockingScheduler({
        'apscheduler.executors.default': {
            'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
            'max_workers': '20'
        },
        'apscheduler.executors.processpool': {
            'type': 'processpool',
            'max_workers': '30'
        },
        'apscheduler.job_defaults.coalesce': 'false',
        'apscheduler.job_defaults.max_instances': '600',
        # 'apscheduler.timezone': 'UTC',
        })
    try:
        sync_job = SyncChannelJob(scheduler)
        sync_job.loop()
    except KeyboardInterrupt:
        print "send job exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e
