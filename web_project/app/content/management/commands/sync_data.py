# coding=utf-8
from django.core.management.base import BaseCommand
from django.core.exceptions import MultipleObjectsReturned
from apscheduler.schedulers.blocking import BlockingScheduler
from lib import youku_cms
from app.content.models import *
from base.youkuapi.video import VideoApi
from base.youkuapi.show import ShowApi
from base.youkuapi.playlist import PlaylistApi
import json
import logging
from hashlib import sha1

logging.getLogger('apscheduler.executors.default').addHandler(logging.StreamHandler())


def extract_fetch_info(fetch_info, is_sub=False):
    """
    将从cms主站抓取的信息提取到对应的base_video字段
    """
    info = dict(video_type=VideoType.to_i(fetch_info['type']),
                h_image=fetch_info['big_logo'] or fetch_info['medium_logo'] or fetch_info['logo'],
                video_id=fetch_info['encodeid'])
    key_list = ['title', 'subtitle', 'intro', 'module_id', 'subchannel_id']
    for key in key_list:
        info[key] = fetch_info[key]
    if is_sub:
        info.pop('module_id', None)
    else:
        info.pop('subchannel_id', None)

    return info


def extract_middleware_info(video_id, video_type):
    """
    提取中间层信息
    """
    info = {}
    if video_type == 'video':
        middle_info = VideoApi.get_video_info(video_id)
    elif video_type == 'show':
        middle_info = ShowApi.get_show_info(video_id)
    elif video_type == 'playlist':
        middle_info = PlaylistApi.get_playlist_info(video_id)
    else:
        return {}
    print_beauty(middle_info)
    info['intro'] = middle_info.get('desc')
    info['has_copyright'] = 1 if middle_info.get('copyright_status') == 'authorized' else 0
    info['h_image'] = middle_info.get('thumburl_v2') or middle_info.get('thumburl')
    info['paid'] = middle_info.get('paid') or 0
    pay_type = middle_info.get('pay_type')
    info['pay_type'] = BaseVideo().set_video_pay_type(pay_type) if pay_type is not None else 0
    info['state'] = 1 if middle_info.get('state') == 'normal' else 0

    return info


def is_equal(exist_item, new_item):
    """
    根据一些字段值是否相等判断两个object是否相等
    """
    for k, v in new_item.__dict__.iteritems():
        if not k.startswith('_') and k != 'position':
            if v is not None and v != exist_item.__dict__[k]:
                return False

    return True


def is_cms_fetch_update(job, results):
    """
    判断是否进行抓取结果的sha1值更新
    """
    new_sha1_res = sha1(json.dumps(results)).hexdigest()
    if new_sha1_res != job.sha1_of_last_fetch:
        job.sha1_of_last_fetch = new_sha1_res
        job.save()
        return True
    else:
        return False


def integrate_base_video_info(main_item, extra_item):
    """
    更新视频信息时，在一些字段上使用抓取的信息覆盖已存在的信息
    """
    #TODO: judge the useful keys to replace
    replace_keys = ['title', 'subtitle', 'intro', 'h_image', 's_image', 'v_image', 'state', 'video_id', 'video_type',
                    'paid', 'pay_type', 'has_copyright',
                    # 'module_id', 'subchannel_id',
                    # 'attached_game_type', 'url', 'created_at', 'position', 'pgc_uid', 'image_size',
                    # 'game_page_id', 'game_id', 'first_episode_video_id', 'first_episode_video_pv',
                    ]
    for k in replace_keys:
        main_item.__dict__[k] = extra_item.__dict__[k]

    return main_item


def drag_all_info(result, pos):
    """
    集成cms主站的抓取信息和中间层的信息，还有position
    """
    fetch_info = extract_fetch_info(result)
    total_info = extract_middleware_info(video_id=fetch_info['video_id'], video_type=result['type'])
    total_info.update(fetch_info)
    total_info['position'] = pos
    return total_info


def get_video_insert_or_update(cls, item, total_info):
    """
    判断抓取的视频应该更新还是插入，并完成相应操作
    """
    new_item = cls()
    new_item.__dict__.update(total_info)
    if item and not is_equal(item, new_item):
        print '++++++++++update'
        item = integrate_base_video_info(item, new_item)
        item.save()
    elif not item:
        print '**********new add'
        new_item.save()


def print_beauty(struct):
    beauty_str = json.dumps(struct, ensure_ascii=False, indent=4, sort_keys=True)
    print beauty_str


def handle_job_of_android(job, result):
    pass


def handle_job_of_iphone(job, result):
    pass


def batching(up_cls, video_cls, results, pk_id):
    """
    一次抓取的所有视频信息的插入或更新的处理
    """
    #TODO: up_cls　can be removed
    try:
        block = up_cls.objects.get(pk=pk_id)
        max_pos = video_cls.objects.aggregate(Max('position'))['position__max'] or 0
        for res in reversed(results):
            v_id = res['encodeid']
            item = video_cls.objects.filter(video_id=v_id).first()
            total_info = drag_all_info(res, max_pos+1)
            get_video_insert_or_update(video_cls, item, total_info)
            max_pos += 1
    except up_cls.DoesNotExist, e:
        print e


def handle_job_of_ipad(job, results):
    if getattr(job, 'module_id', None):
        batching(IpadSubChannelModule, IpadSubChannelModuleItem, results, job.module_id)
    elif getattr(job, 'subchannel_id', None):
        batching(IpadSubChannel, IpadSubChannelItem, results, job.subchannel_id)


def handle_job_of_win_phone(job, result):
    pass


def handle_sync_job(job, results):
    func_str = 'handle_job_of_' + SyncJob.platform_to_str(job.platform)
    globals()[func_str](job, results)


class Command(BaseCommand):
    def __init__(self):
        self.sched = BlockingScheduler()
        super(Command, self).__init__()
        self.sched.add_job(self.load_circle, "interval", seconds=5)
        self.jobs = {}

    def load_circle(self):
        # executors = {
        # 'default': ProcessPoolExecutor(max_workers=4)
        # }
        store_keys = self.jobs.keys()
        for job in SyncJob.objects.filter(state=1, is_delete=False):
            key = '%s_%s' % (str(job.id), str(job.virtual_name))
            try:
                store_keys.remove(key)
            except ValueError:
                pass
            if self.jobs.get(key) is None:
                self.jobs[key] = 1

                def job_func(*args, **kwargs):
                    name = kwargs.get('name')
                    job = kwargs.get('job')
                    items = youku_cms.getVideosByVirtualName(name).get('data', [])
                    if job.max_fetch_count > 0:
                        items = items[:job.max_fetch_count]
                    for item in items:
                        if isinstance(item, unicode):
                            continue
                        for field in ['module_id', 'subchannel_id']:
                            item[field] = job.__dict__[field]

                    # sha1值与上一次抓取不同时才handle
                    if is_cms_fetch_update(job, items):
                        handle_sync_job(job, items)
                        print 'Video nums:%s, Name:%s' % (len(items), name)

                job_mes = {'name': job.virtual_name, 'job': job}
                if job.interval:
                    self.sched.add_job(job_func, trigger="interval", seconds=job.interval, id=key, max_instances=100,
                                       kwargs=job_mes)
                else:
                    hour, minute = map(int, job.cron.split(':'))
                    self.sched.add_job(job_func, trigger="cron", id=key, max_instances=100, hour=hour, minute=minute,
                                       second=0, kwargs=job_mes)
                if job.runatonce:
                    job.runatonce = False
                    job_func(name=job.virtual_name, job=job)
                job.save()

        for k in store_keys:
            self.sched.remove_job(job_id=k)
            del self.jobs[k]

    def handle(self, *args, **options):
        try:
            self.sched.start()
        except KeyboardInterrupt:
            pass

    # non-used
    def tick(self):
        ret = youku_cms.getVirtualNames(page=1, count=50)
        for d in ret.get('data', []):
            print d.get('name', '')
        print "~~~~~~"
        items = youku_cms.getVideosByVirtualName(u'搞笑今日笑点')
        print items
