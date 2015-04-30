# coding=utf-8
from django.db import models
from app.content.management.commands.lib import youku_cms
from app.content.models.sub_channel_module_item import *
from django.db.models import Max
from app.content.models.sub_channel import *
from app.content.models.sub_channel_item import *
from app.content.models.sub_channel_module import *
from base.youkuapi.video import VideoApi
from base.youkuapi.show import ShowApi
from wi_model_util.imodel import get_object_or_none
from app.content.lib.image_helper import ImageHelper
from app.content.lib.model_util import ModelUtil
from app.content.management.commands.lib.youku_cms import get_virtual_name_query_url
from hashlib import sha1
import json
import logging
import socket
import re
import time
from datetime import datetime


class SyncJob(models.Model):
    PLATFORM = (
        (1, 'android'),
        (2, 'ipad'),
        (3, 'iphone'),
        # (4, 'win_phone')
    )

    STATUS_OPEN = 1
    STATUS_CLOSE = 0

    virtual_name = models.CharField(max_length=255, verbose_name=u'虚拟名称', default='', blank=False, db_index=True)
    # main_module_id = models.IntegerField(verbose_name='首页模块id', null=True)
    platform = models.IntegerField(verbose_name=u'平台', choices=PLATFORM, default=2)
    channel_id = models.IntegerField(verbose_name=u'频道id')
    subchannel_id = models.IntegerField(verbose_name=u'子频道id', null=True)
    module_id = models.IntegerField(verbose_name=u'子频道模块id', null=True, blank=True)
    interval = models.IntegerField(verbose_name=u'时间间隔', null=True, default=0, blank=True)
    cron = models.CharField(max_length=255, blank=True, null=True, verbose_name=u'定时间隔')  # 以分号分隔
    runatonce = models.BooleanField(verbose_name=u'立即运行', default=False)
    is_delete = models.BooleanField(verbose_name=u'删除标记', default=False, db_index=True)
    state = models.IntegerField(verbose_name=u'状态（开／关）', default=1)
    category_class = models.CharField(max_length=64, verbose_name=u'类名', blank=True)
    category_id = models.IntegerField(verbose_name=u'所在目录的id', blank=True, null=True)
    category_name = models.CharField(max_length=255, verbose_name=u'虚拟名称抓取目的地', blank=True)
    is_auto_published = models.BooleanField(verbose_name=u'是否自动上线', default=True)
    sha1_of_last_fetch = models.CharField(max_length=160, verbose_name=u'上次抓取的SHA1结果', default='')
    max_fetch_count = models.IntegerField(verbose_name=u'最大抓取数量', default=0, blank=True)

    def __unicode__(self):
        return 'SyncJob for %s' % self.virtual_name

    @classmethod
    def platform_to_str(cls, plat_num):
        for item in cls.PLATFORM:
            if plat_num == item[0]:
                return item[1]

        return cls.PLATFORM[2][1]

    @classmethod
    def platform_to_int(cls, plat_str):
        plat_str = str(plat_str)
        for item in cls.PLATFORM:
            if plat_str == item[1]:
                return item[0]

        return 0

    class Meta:
        verbose_name = u"抓取计划表"
        verbose_name_plural = verbose_name
        app_label = "content"

    @classmethod
    def jobs(cls):
        return cls.objects.filter(state=SyncJob.STATUS_OPEN, is_delete=False) or []

    @property
    def cron_list(self):
        if self.cron:
            results = []
            cron_list = self.cron.split(';')
            for single_cron in cron_list:
                hour, minute = map(int, single_cron.split(':'))
                results.append(dict(
                    hour=hour,
                    minute=minute
                ))
            return results

    @property
    def key(self):
        cron_str = self.cron if self.cron else ''
        return '%d_%s_%s_%s' % (self.id, str(self.virtual_name), cron_str, str(self.interval))

    @classmethod
    def plan_list(cls, subchannel_id=None, module_id=None, platform=1, plat_str=None):
        plan_list, plans, query_dict = [], [], {}
        plat = cls.platform_to_int(plat_str)
        plat = plat if plat else platform
        if module_id:
            query_dict = {
                'module_id': module_id,
                'platform': plat
            }
        elif subchannel_id:
            query_dict = {
                'subchannel_id': subchannel_id,
                'platform': plat
            }
        plans = cls.objects.filter(**query_dict)
        if plans:
            for plan in plans:
                tmp_plan = plan.__dict__
                tmp_plan['interval'] /= 60.0  # 转化为分钟表示
                plan_list.append(tmp_plan)
        return plan_list

    def query_data_src_url(self):
        return get_virtual_name_query_url(self.virtual_name)

    def get_interval_display(self):
        return int(self.interval / 60.0)

    def get_platform_display(self):
        for k, v in self.PLATFORM:
            if k == self.platform:
                return v


class SyncLog(models.Model):
    job = models.ForeignKey(SyncJob, related_name='log', verbose_name='日志')

    ids = models.TextField(verbose_name=u'视频id集合', default='', blank=False)
    titles = models.TextField(verbose_name=u'视频title集合', default='', blank=False)
    indexes = models.TextField(verbose_name=u'视频序号集合', default='', blank=False)

    created_at = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    executed_at = models.DateTimeField(verbose_name=u'执行时间', auto_now_add=True)

    class Meta:
        verbose_name = u"抓取日志"
        verbose_name_plural = verbose_name
        app_label = "content"


class BasicJob(object):
    _contrast = {
        'ipad': (IpadSubChannelModuleItem, IpadSubChannelItem),
        'iphone': (IphoneSubChannelModuleVideo, IphoneSubChannelVideo),
        'android': (AndroidSubChannelModuleVideo, AndroidSubChannelVideo),
        'win_phone': None  # winphone频道页好像没写的样子
    }
    _video_type_list = ['show', 'video', 'faceted_video', 'text']

    def __init__(self, job, result):
        self.job = job
        self.cms_fetch_info = result
        self.cms_video_list = self.get_cms_video_list(result)
        self.cms_extra_info = {}
        self.mid_extra_info = {}
        self.integrate_info = {}
        self.video_type = None
        self.type = None

    @property
    def is_updated(self):
        # return True
        update_tags = sha1(json.dumps(self.cms_video_list)).hexdigest()
        # 由于memcache的缓存，经常没有“更新”
        if update_tags == self.job.sha1_of_last_fetch:
            self.add_log([])
            return False
        else:
            self.job.sha1_of_last_fetch = update_tags
            self.job.save()
            return True

    @property
    def is_sub(self):
        if getattr(self.job, 'module_id', None):
            return False
        elif getattr(self.job, 'subchannel_id', None):
            return True

    @property
    def is_pass_handle(self):
        flag = False
        is_updated = self.is_updated
        if not is_updated or (not self.cms_video_list):
            flag = True

        cms_type = self.get_videotype_from_cmstype(self.cms_fetch_info.get('type', ''))
        if not cms_type or cms_type not in self._video_type_list:
            # 不处理一些其它类型或出错类型
            flag = True

        mes = 'UPDATE' if is_updated else 'NOT UPDATE'
        print 'state:%-9s - type:%-13s - len:%-2s - name_id:%s' % \
              (mes, cms_type, len(self.cms_video_list), self.job.id)

        self.type = cms_type
        return flag

    @staticmethod
    def is_trailer(mid_info):
        try:
            v_types = mid_info['hasvideotype']
            if unicode('正片') in v_types:
                return False
            else:
                print '这是预告片this is trailer!!!!'
                return True
        except KeyError:
            return False

    @staticmethod
    def get_trailer_videoid(res):
        try:
            return res['trailer_videoid']
        except KeyError:
            return ''

    @staticmethod
    def validate_and_set_image(image):
        pat = re.compile(r'^http')
        result = {}
        if image and pat.search(image):
            if ImageHelper.if_h_image(image):
                result['v_image'] = image
            else:
                result['h_image'] = image
        return result

    @staticmethod
    def covert_image_to_standard(info):
        if info.get('h_image'):
            info['h_image'] = ImageHelper.convert_to_448_252(info['h_image'])
        if info.get('v_image'):
            info['v_image'] = ImageHelper.convert_to_200_300(info['v_image'])

        return info

    @staticmethod
    def is_empty(item):
        try:
            if item is None or item == 0 or item.strip() == '':
                return True
            else:
                return False
        except AttributeError:
            return True

    @staticmethod
    def cover_exist_video_info(main_item, extra_item):
        """更新视频时，在一些字段上用抓取的信息覆盖已存在的信息"""
        # TODO: judge the useful keys to replace
        replace_keys = ['title', 'subtitle', 'intro', 'h_image', 's_image', 'v_image', 'state', 'video_id',
                        'video_type', 'paid', 'pay_type', 'has_copyright',
                        # 'module_id', 'subchannel_id', 'position'
                        ]
        for k in replace_keys:
            if k == "pay_type":
                main_item.pay_type = extra_item.pay_type
            else:
                main_item.__dict__[k] = extra_item.__dict__[k]

        return main_item

    @staticmethod
    def is_equal(exist_item, new_item):
        """根据一些字段值是否相等判断两个object是否相等"""
        for k, v in new_item.__dict__.iteritems():
            if not k.startswith('_') and k != 'position':
                if v is not None and v != exist_item.__dict__[k]:
                    return False

        return True

    @staticmethod
    def print_beauty(struct):
        beauty_str = json.dumps(struct, ensure_ascii=False, indent=4, sort_keys=True)
        print beauty_str

    def get_max_position(self, dest_cls):
        if self.is_sub:
            results = dest_cls.objects.filter(subchannel_id=self.job.subchannel_id)
        else:
            results = dest_cls.objects.filter(module_id=self.job.module_id)
        return results.aggregate(Max('position'))['position__max'] if results else 0

    def get_cms_video_list(self, result):
        data = result.get('data', [])
        if not isinstance(data, list):
            return []
        if self.job.max_fetch_count == 0:
            return data
        elif self.job.max_fetch_count > 0:
            return data[:self.job.max_fetch_count]

    def lay_image_from_cms(self, info, res):
        # TODO: change to res.get('logo', ''), because res type image can not convert to other size?
        image = res.get('big_logo') or res.get('medium_logo') or res.get('logo', '')
        info.update(self.validate_and_set_image(image))
        return info

    def get_image_from_middleware(self, mid_info):
        v_type = self.video_type
        tmp_context = {}
        if v_type == 'video':
            tmp_context['h_image'] = mid_info.get('thumburl_v2') or mid_info.get('thumburl', '')
        elif v_type == 'show':
            tmp_context['h_image'] = mid_info.get('show_thumburl', '')
            tmp_context['v_image'] = mid_info.get('show_vthumburl', '')

        res_context = {}
        for v in tmp_context.values():
            res_context.update(self.validate_and_set_image(v))

        return res_context

    def extract_cms_info(self, res):
        info = dict(video_type=VideoType.to_i(res['type']),
                    state=1 if self.job.is_auto_published else 0,  # state is determined by is_auto_published
                    video_id=res['video_id']
                    )
        key_list = ['title', 'h_image', 'v_image']
        for key in key_list:
            info[key] = res.get(key, '')

        if self.video_type == 'show':
            info['title'] = res.get('title') or res.get('showname', '')

        if self.is_sub:
            info['subchannel_id'] = self.job.subchannel_id
        else:
            info['module_id'] = self.job.module_id

        self.lay_image_from_cms(info, res)
        self.cms_extra_info = info

    def extract_middleware_info(self, res):
        """提取中间层信息到mid_extra_info"""
        video_id = self.cms_extra_info['video_id']
        video_type = self.video_type
        info, middle_info, img_info = ({},) * 3
        try:
            if video_type == 'video':
                middle_info = VideoApi.get_video_info(video_id)
                img_info = self.get_image_from_middleware(middle_info)
            elif video_type == 'show':
                middle_info = ShowApi.get_show_info(video_id)
                img_info = self.get_image_from_middleware(middle_info)
        except socket.timeout:
            print 'TIMEOUT - the virtual name is : %s' % self.job.virtual_name
        except Exception, e:
            print e

        info.update(img_info)
        device = 'pad' if SyncJob.platform_to_str(self.job.platform) == 'pad' else 'mobile'
        info['has_copyright'] = ModelUtil.check_copyright(VideoType.to_i(self.video_type), res, device_type=device)
        info['paid'] = middle_info.get('paid', 0)
        pay_type = middle_info.get('pay_type', [])
        info['pay_type'] = BaseVideo().set_video_pay_type(pay_type) if pay_type is not None else 0
        if self.is_trailer(middle_info):
            self.cms_extra_info['video_type'] = VideoType.to_i('video')
            self.cms_extra_info['video_id'] = self.get_trailer_videoid(middle_info)

        self.mid_extra_info = info

    def integrate_all_info(self, pos, res):
        """集成cms主站的抓取和中间层的信息，还有position"""
        self.extract_cms_info(res)
        self.extract_middleware_info(res)

        set_info = self.mid_extra_info
        set_info['position'] = pos
        for k, v in self.cms_extra_info.items():
            if k in set_info:
                # 两种信息哪种存在使用哪种,都存在时cms中的信息优先级更高
                if self.is_empty(set_info[k]) or not self.is_empty(v):
                    pass
                else:
                    continue
            set_info[k] = v

        self.integrate_info = self.covert_image_to_standard(set_info)

    def get_video_insert_or_update(self, video_cls, item):
        """判断抓取的视频应该更新还是插入，并完成相应操作"""
        new_item = video_cls()
        pay_type = self.integrate_info.pop("pay_type")
        new_item.__dict__.update(self.integrate_info)
        new_item.pay_type = pay_type

        if item:
            if self.is_equal(item, new_item):
                item.position = new_item.position
            else:
                item = self.cover_exist_video_info(item, new_item)
            item.is_delete = False  # keep the video can be seen
            item.save()
            return item
        else:
            new_item.save()
            return new_item

    def get_video_id_from_type(self, res):
        try:
            if self.type == 'text':
                if 'encodeid' not in res and 'id' not in res:
                    return ''
            elif self.type == 'show':
                return res.get('encodeid') or youku_cms.convert_pk_odshow_to_showid(res.get('id'))
            else:
                return res['encodeid']
        except Exception, e:
            print 'get video_id error happened', e
            BasicJob.print_beauty(res)

    def get_videotype_from_cmstype(self, cms_type):
        if cms_type and cms_type.startswith('cms_'):
            cms_type = cms_type[4:]
            if cms_type in self._video_type_list:
                return cms_type

        return ''

    def handle_platform_job(self, video_cls):
        """一次抓取的所有视频信息的插入或更新处理"""
        if self.is_pass_handle:
            return

        max_pos = self.get_max_position(video_cls)
        log_info = []
        video_index = 1
        for res in reversed(self.cms_video_list):
            # if res['type'] not in ['video', 'show']:
            # continue
            video_index += 1
            self.video_type = res['type']
            v_id = self.get_video_id_from_type(res)
            if not v_id:
                continue
            res['video_id'] = v_id
            item = get_object_or_none(video_cls, video_id=v_id)
            max_pos += 1
            self.integrate_all_info(max_pos, res)
            item = self.get_video_insert_or_update(video_cls, item)
            log_info.insert(0, (item.video_id, item.title, video_index))
        self.add_log(log_info)

    def handle_sync_job(self):
        """分配到不同平台(模型)"""
        platform = SyncJob.platform_to_str(self.job.platform)
        dest_tup = self._contrast.get(platform)
        dest_cls = dest_tup[1] if self.is_sub else dest_tup[0]
        if dest_cls:
            self.handle_platform_job(dest_cls)

    def add_log(self, log_info):
        """
        log_info: [(id,title),(id,title)]
        """
        print "new add_log: ", log_info
        self.remove_redundant_logs()
        if not self.update_same_result_fetch_log(log_info):
            self.create_new_log(log_info)

    def update_same_result_fetch_log(self, log_info):
        last_two_logs = SyncLog.objects.filter(job_id=self.job.id).order_by('-id')[:2]
        if len(last_two_logs) > 1:
            last_log, last_log_2 = last_two_logs
            ids = self.generate_log_ids(log_info)
            titles = self.generate_log_titles(log_info)
            print 'last_log.ids...:', last_log.ids
            if last_log.ids == ids and last_log.titles == titles \
                    and last_log_2.ids == ids and last_log_2.titles == titles:
                last_log.executed_at = datetime.now()
                last_log.save()
                print 'last_log.update...'
                return last_log
        print 'new_log.will_be_add...'
        return None

    def remove_redundant_logs(self):
        job_id = self.job.id
        max_log_count = 200
        current_log_count = SyncLog.objects.filter(job_id=job_id).count()
        if current_log_count > max_log_count:
            delete_count = current_log_count - max_log_count
            del_objs = SyncLog.objects.filter(job_id=job_id).order_by('created_at')[:delete_count]
            for obj in del_objs:
                obj.delete()

    def create_new_log(self, log_info):
        log = SyncLog()
        log.job_id = self.job.id
        log.ids = self.generate_log_ids(log_info)
        log.titles = self.generate_log_titles(log_info)
        log.indexes = self.generate_log_indexes(log_info)
        log.save()

    def generate_log_ids(self, log_info):
        return ';'.join([str(detail[0]) for detail in log_info])

    def generate_log_titles(self, log_info):
        return ';'.join([str(detail[1]) for detail in log_info])

    def generate_log_indexes(self, log_info):
        return ';'.join([str(detail[2]) for detail in log_info])
