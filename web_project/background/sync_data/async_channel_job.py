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

from app.content.management.commands.lib import youku_cms
from app.content.models import *
import logging
from app.content.models.sync_job import BasicJob
from redis_model.queue import Worker


def do_job(data):
    print "**Recieve data: ", data
    job_id = data.get("job_id")
    if job_id:
        job = SyncJob.objects.get(id=job_id)
        name = job.virtual_name
        try:
            result = youku_cms.getVideosByVirtualName(name)
        except Exception, e:
            logging.error(e)
            return
        work_job = BasicJob(job, result)
        work_job.handle_sync_job()
    else:
        logging.error("job_id is none")

    


if __name__ == "__main__":
    worker = Worker("async.channel.job")
    try:
        worker.register(do_job)
        worker.start()
    except KeyboardInterrupt:
        worker.stop()
        print "consume job exited cleanly"
        sys.exit(1)
    except Exception, e:
        print e
