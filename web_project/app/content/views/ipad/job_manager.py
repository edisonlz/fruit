# coding=utf-8
from app.content.models import IpadChannel, IpadSubChannel, IpadSubChannelModule, Platform
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from app.content.models import SyncJob, AndroidChannel, AndroidSubChannel, AndroidSubChannelModule, \
    IpadChannel, IpadSubChannel, IpadSubChannelModule, IphoneChannel, IphoneSubChannel, IphoneSubChannelModule
from django.shortcuts import render, get_object_or_404


def add_sync_subchannel_job(request):
    if request.method == 'POST':
        query_list = ['channel_id', 'subchannel_id', 'module_id', 'virtual_name']
        other_param_list = ['interval', 'cron', 'max_fetch_count', 'platform']
        bool_list = ['runatonce', 'is_auto_published']
        res = {}
        for name in other_param_list + bool_list + query_list:
            result = request.POST.get(name, '')
            if name in bool_list:
                result = True if result else False
            result = 60 * int(result) if name == 'interval' else result
            res[name] = result

        if res['cron']:
            res['interval'] = 0
        is_add = is_sub = False
        query_dict = dict([(k, res[k]) for k in query_list])
        if res['module_id']:
            if not SyncJob.objects.filter(**query_dict):
                is_add = True
        elif res['subchannel_id']:
            query_dict.pop('module_id', None)
            if not SyncJob.objects.filter(**query_dict):
                is_add = True
                is_sub = True

        if is_add:
            if is_sub:
                res.pop('module_id', None)
            job = SyncJob()
            job.__dict__.update(res)
            job.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def list_sync_subchannel_job(request):
    if request.method == 'POST':
        pass
    else:
        channel_id = request.POST.get('channel_id', '')
        subchannel_id = request.POST.get('subchannel_id', '')
        subchannel_module_id = request.POST.get('subchannel_module_id', '')
        jobs = SyncJob.objects.filter(subchannel_module_id=subchannel_module_id)
        from pprint import pprint

        pprint(request.POST)
        pprint(jobs)
        return render(request, 'channel/ipad_channels.html', {'channels': channels, 'platform': platform})


def show_sync_jobs(request):
    if request.method == 'GET':
        channel_id, subchannel_id, module_id, platform = (None,) * 4
        query_d = {}
        param_list = ['channel', 'subchannel', 'module', 'platform']
        for param in param_list:
            if param == 'platform':
                query_d[param] = request.GET.get(param)
            else:
                query_d[param+'_id'] = request.GET.get('select_'+param)
        pro_context = get_channel_and_branch_info(**query_d)
        if pro_context['module']:
            job_query = {'module_id': pro_context['module'].id}
        elif pro_context['subchannel']:
            job_query = {'subchannel_id': pro_context['subchannel'].id}
        else:
            job_query = {}

        if job_query:
            job_query.update({'platform': query_d['platform']})
            print 'job query', job_query
            jobs = SyncJob.objects.filter(**job_query)
            print 'jobs', jobs
        else:
            jobs = []
        if jobs:
            for job in jobs:
                job.interval /= 60.0
        query_d.update({'jobs': jobs, 'platform_str': SyncJob.platform_to_str(int(query_d['platform']))})
        pro_context.update(query_d)
        print pro_context
        return render(request, 'syncjob/show_module_items.html', pro_context)


def get_channel_and_branch_info(channel_id, subchannel_id, module_id, platform):
    contrast = {
        1: (AndroidChannel, AndroidSubChannel, AndroidSubChannelModule),
        2: (IpadChannel, IpadSubChannel, IpadSubChannelModule),
        3: (IphoneChannel, IphoneSubChannel, IphoneSubChannelModule)
    }
    channels, subchannels, modules, channel, subchannel, module = (None,) * 6
    try:
        cha_cls, sub_cls, mod_cls = contrast[int(platform)]
        channels = cha_cls.objects.filter(is_delete=0).order_by('-position')
        if channels and len(channels) > 0:
            channel = cha_cls.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = sub_cls.objects.get(pk=subchannel_id, is_delete=0) if subchannel_id \
                    else subchannels[0]
                if subchannel.type == 1:  # 子频道下的模块类型
                    modules = subchannel.module.order_by('-position')
                    # for module in modules:
                    #     print module.id, module.title
                    # print mod_cls.objects.get(pk=module_id).title
                    if modules and len(modules) > 0:
                        module = mod_cls.objects.get(pk=module_id, is_delete=0) if module_id \
                            else modules[0]
                    # print 'module', module.id, module.title
    except Exception, e:
        pass
    finally:
        return {
            'channel': channel, 'channels': channels, 'subchannel': subchannel, 'subchannels': subchannels,
            'module': module, 'modules': modules
        }


def show_sync_module_jobs(request):
    if request.method == 'POST':
        pass
    else:
        channel_id, subchannel_id, module_id, platform = (None,) * 4
        jobs = []
        try:
            channel_id = int(request.GET.get('select_channel'))
            subchannel_id = int(request.GET.get('select_subchannel'))
            module_id = int(request.GET.get('select_module'))
            platform = int(request.GET.get('platform'))
        except:
            pass
        # platform = Platform.get_platform(request.path)
        # channels = IpadChannel.objects.filter(platform=platform).order_by("position")
        channels = IpadChannel.objects.order_by("position")
        channel = None
        subchannel = None
        module = None
        modules = []
        subchannels = []
        try:
            if channels and len(channels) > 0:
                channel = IpadChannel.objects.get(pk=channel_id) if channel_id else channels[0]
                subchannels = channel.subchannel.order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = IpadSubChannel.objects.get(pk=subchannel_id) if subchannel_id else subchannels[0]
            if subchannel.type == 1:
                modules = subchannel.module.order_by('-position')
            if modules and len(modules) > 0:
                module = IpadSubChannelModule.objects.get(pk=module_id) if module_id else modules[0]
        except:
            pass

        if module_id:
            jobs = SyncJob.objects.filter(module_id=module_id)
        elif subchannel_id:
            jobs = SyncJob.objects.filter(subchannel_id=subchannel_id)
            multi_module_jobs = jobs.exclude(module_id=None)
            if multi_module_jobs:
                module_jobs = multi_module_jobs.filter(
                    module_id=multi_module_jobs[0].module_id)
                jobs = module_jobs if module_jobs else jobs
        elif channel_id:
            jobs = SyncJob.objects.filter(channel_id=channel_id)
            if jobs:
                jobs = SyncJob.objects.filter(subchannel_id=jobs[0].subchannel_id)
                if jobs:
                    multi_module_jobs = jobs.exclude(module_id=None)
                    if multi_module_jobs:
                        module_jobs = multi_module_jobs.filter(
                            module_id=multi_module_jobs[0].module_id)
                        jobs = module_jobs if module_jobs else jobs
        elif channel_id is None and subchannel_id is None and module_id is None:
            if module:
                jobs = SyncJob.objects.filter(module_id=module.id)
            elif subchannel:
                jobs = SyncJob.objects.filter(subchannel_id=subchannel.id)
            else:
                jobs = None
        else:
            jobs = None

        if jobs:
            for job in jobs:
                job.interval /= 60.0
        return render(request, 'syncjob/show_module_items.html', {
            'jobs': jobs,
            'subchannels': subchannels, 'channels': channels,
            'this_channel': channel,
            'this_subchannel': subchannel, 'modules': modules,
            'this_module': module
        })


def update_sync_module_jobs(request):
    if request.method == 'POST':
        try:
            job_id = request.POST.get('id')
            sel_job = SyncJob.objects.get(pk=job_id)
            sel_job.interval = int(request.POST.get('interval', 60)) * 60
            sel_job.virtualName = request.POST.get('virtualName')
            runatonce = request.POST.get('runatonce', '')
            sel_job.runatonce = True if runatonce == 'on' else False
            sel_job.save()
        except:
            pass
        return HttpResponseRedirect(reverse('list_sync_plans'))
    else:
        channel_name = request.GET.get('channel_name', '')
        subchannel_name = request.GET.get('subchannel_name', '')
        module_name = request.GET.get('module_name', '')
        job_id = request.GET.get('job_id')
        sel_job = SyncJob.objects.get(pk=job_id)
        return render(request, 'syncjob/update_sync_job.html', {'job': sel_job, 'channel_name': channel_name,
                                                                    'subchannel_name': subchannel_name,
                                                                    'module_name': module_name})


def delete_sync_module_jobs(request):
    try:
        job_id = request.GET.get('job_id')
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.delete()
    except ValueError, SyncJob.DoesNotExist:
        pass
    return HttpResponseRedirect(reverse('list_sync_plans'))


def run_sync_module_jobs(request):
    job_id = request.GET.get('job_id')
    channel_id = request.GET.get('channel_id', '')
    subchannel_id = request.GET.get('subchannel_id', '')
    module_id = request.GET.get('module_id', '')
    platform = request.GET.get('platform', '')
    try:
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.runatonce = 1
        sel_job.save()
    except SyncJob.DoesNotExist:
        pass

    return HttpResponseRedirect(reverse(
        'list_sync_plans') + '?channel_id=' + channel_id + '&subchannel_id=' + subchannel_id + '&module_id=' + module_id)