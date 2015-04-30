# coding=utf-8
from app.content.models import IpadChannel, IpadSubChannel, IpadSubChannelModule, Platform, SyncLog
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from app.content.models import SyncJob, AndroidChannel, AndroidSubChannel, AndroidSubChannelModule, \
    IpadChannel, IpadSubChannel, IpadSubChannelModule, IphoneChannel, IphoneSubChannel, IphoneSubChannelModule, \
    VirtualNameFetch
from django.shortcuts import render, get_object_or_404
import json
import re
from wi_model_util.imodel import get_object_or_none
from content.management.commands.lib import youku_cms


CONTRAST = {
    1: (AndroidChannel, AndroidSubChannel, AndroidSubChannelModule),
    2: (IpadChannel, IpadSubChannel, IpadSubChannelModule),
    3: (IphoneChannel, IphoneSubChannel, IphoneSubChannelModule)
}


def single_virtual_name_fetch(request):
    virtual_name = request.GET.get('virtual_name').strip()
    plans = SyncJob.objects.filter(virtual_name=virtual_name)
    return render(request, 'syncjob/show_single_virtualname_fetch.html', {
        'jobs': plans,
        'ask_name': virtual_name
    })


def get_single_channel_and_branch_info(channel_id, subchannel_id, module_id, platform):
    contrast = CONTRAST
    channel = subchannel = module = None
    try:
        platform = int(platform)
    except ValueError:
        platform = SyncJob.platform_to_int(platform)
    cha_cls, sub_cls, mod_cls = contrast[int(platform)]
    try:
        channel = cha_cls.objects.get(id=channel_id)
        subchannel = sub_cls.objects.get(id=subchannel_id)
        module = mod_cls.objects.get(id=module_id)
    except Exception, e:
        pass
    return {
        'channel': channel, 'subchannel': subchannel, 'module': module
    }


def show_single_plan(request):
    param_d = {}
    param_list = ['channel', 'subchannel', 'module', 'platform']
    for param in param_list:
        if param == 'platform':
            param_d[param] = request.GET.get(param)
        else:
            param += '_id'
            param_d[param] = request.GET.get(param)
    query_d = {'platform': SyncJob.platform_to_int(param_d['platform'])}
    if param_d['module_id']:
        query_d.update({'module_id': param_d['module_id']})
    elif param_d['subchannel_id']:
        query_d.update({'subchannel_id': param_d['subchannel_id']})
    else:
        query_d = {}
    plans = []
    if query_d:
        plans = SyncJob.objects.filter(**query_d)
        if plans:
            for plan in plans:
                plan.interval /= 60.0
    context = {'jobs': plans}
    context.update(param_d)
    context.update(get_single_channel_and_branch_info(**param_d))
    return render(request, 'syncjob/single_sync_job.html', context)


def check_virtual_name_from_web(request):
    check_res = check_virtual_name(request.POST.get('virtual_name'))
    if check_res:
        return check_res
    else:
        return HttpResponse(json.dumps({'status': 'success'}))


def check_virtual_name(v_name):
    v_name_list = [item['name'] for item in VirtualNameFetch().v_name_list()]
    if not v_name or v_name not in v_name_list:
        return HttpResponse(json.dumps({'status': 'failed', 'msg': '无效的虚拟名称!'}))

    return


def add_sync_plan(request):
    if request.method == 'POST':
        check_res = check_virtual_name(request.POST.get('virtual_name'))
        if check_res:
            return check_res

        query_list = ['channel_id', 'subchannel_id', 'module_id', 'virtual_name']
        other_param_list = ['interval', 'cron', 'max_fetch_count', 'platform', 'category_name']
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
        res['platform'] = SyncJob.platform_to_int(res['platform'])
        query_dict = dict([(k, res[k]) for k in query_list + ['platform']])
        if res['module_id']:
            if not SyncJob.objects.filter(**query_dict):
                is_add = True
        elif res['subchannel_id']:
            query_dict.pop('module_id', None)
            if not SyncJob.objects.filter(**query_dict):
                is_add = is_sub = True

        if is_add:
            if is_sub:
                res.pop('module_id', None)
            job = SyncJob()
            job.__dict__.update(res)
            job.save()

        return HttpResponse(json.dumps({'status': 'success'}))


def del_sync_plan(request, job_id):
    """redirect to one platform's plans after del"""
    try:
        # job_id = request.GET.get('job_id')
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.delete()
        url_str = pack_url(request.GET.dict())
    except ValueError, SyncJob.DoesNotExist:
        pass
    finally:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return HttpResponseRedirect(reverse('show_single_plan') + url_str)


def update_sync_plan(request, job_id):
    if request.method == 'POST':
        try:
            param_list = ['run_type', 'interval', 'cron', 'virtual_name']
            update_context = {}
            for param in param_list:
                if param == 'interval':
                    update_context[param] = int(request.POST.get(param, 0)) * 60
                else:
                    update_context[param] = request.POST.get(param)
            update_context.pop('run_type', None)
            SyncJob.objects.filter(id=job_id).update(**update_context)
            if request.POST.get('from') == 'show_select_plans':
                url = re.sub(r'(\w+)_id', r'select_\1', pack_url(request.POST.dict()))
                return HttpResponseRedirect(reverse("show_select_plans") + url)
            else:
                return HttpResponseRedirect(reverse("show_single_plan") + pack_url(request.POST.dict()))
        except Exception, e:
            print e
            return HttpResponseRedirect(reverse('request.META.HTTP_REFERER'))
    else:
        param_d = {}
        param_list = ['channel', 'subchannel', 'module', 'platform']
        for param in param_list:
            if param == 'platform':
                param_d[param] = request.GET.get(param)
            else:
                param += '_id'
                param_d[param] = request.GET.get(param, '')
        joint_info = get_single_channel_and_branch_info(**param_d)
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.interval = int(sel_job.interval / 60.0)
        joint_info.update({'job': sel_job, 'platform': param_d['platform']})
        if request.GET.get('from'):
            back = request.GET.get('back')
            joint_info.update({'from': 'show_select_plans', 'back': back})
        else:
            joint_info.update({'from': 'show_single_plan'})
        return render(request, 'syncjob/update_sync_job.html', joint_info)


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


def get_all_plans(request):
    pass


def show_sync_jobs(request):
    if request.method == 'GET':
        levels, query_d = ['channel', 'subchannel', 'module'], {}
        for param in levels:
            if param == 'platform':
                query_d[param] = request.GET.get(param)
            else:
                query_d[param + '_id'] = request.GET.get('select_' + param, '_')
        query_d['platform'] = request.GET.get('platform')
        platform_int = SyncJob.platform_to_int(query_d['platform'])
        # set default platform
        if platform_int == 0:
            query_d['platform'] = 'all'
            traverse = [1, 2, 3]
        else:
            traverse = [platform_int]
        pro_context = get_channel_and_branch_info(**query_d)
        contrast = CONTRAST
        for key in traverse:
            if query_d['channel_id'] == '_':
                choosen_cls = contrast[key][0]
                pro_context['channels'] = choosen_cls.objects.filter(is_delete=0).order_by('-position')
                pro_context['channel'] = '_'
            elif query_d['subchannel_id'] == '_':
                choosen_cls = contrast[key][0]
                try:
                    pro_context['subchannels'] = choosen_cls.objects.get(pk=query_d['channel_id'], is_delete=0) \
                        .subchannel.filter(is_delete=0).order_by('-position')
                except choosen_cls.DoesNotExist:
                    pass
                pro_context['subchannel'] = '_'
            elif query_d['module_id'] == '_':
                choosen_cls = contrast[key][1]
                try:
                    pro_context['modules'] = choosen_cls.objects.get(pk=query_d['subchannel_id'], is_delete=0) \
                        .module.filter(is_delete=0).order_by('-position')
                except choosen_cls.DoesNotExist:
                    pass
                pro_context['module'] = '_'

        pro_context['total_flag'] = False
        for key in levels:
            if pro_context[key] == '_':
                pro_context['total_flag'] = True

        job_query = {}
        for key in levels:
            save_key = key + '_id'
            try:
                job_query[save_key] = pro_context[key].id
            except AttributeError:
                # try channel.id first, if failed then try GET param from query_d
                job_query[save_key] = query_d[save_key]
            if not job_query[save_key] or job_query[save_key] == '_':
                job_query.pop(save_key, None)
        if query_d['platform'] != 'all':
            job_query.update({'platform': platform_int})
        jobs = SyncJob.objects.filter(**job_query)
        for job in jobs:
            job.interval /= 60
        plats = [query_d['platform']] + [item for item in Platform.KEYS.keys() if item != query_d['platform']
                                         and item != 'win_phone']
        if 'all' not in plats:
            plats += ['all']
        query_d.update({'jobs': jobs, 'platform_int': platform_int, 'plats': plats})
        pro_context.update(query_d)
        return render(request, 'syncjob/show_module_items.html', pro_context)


def get_channel_and_branch_info(channel_id, subchannel_id, module_id, platform):
    contrast = CONTRAST
    channels, subchannels, modules, channel, subchannel, module = (None,) * 6
    try:
        cha_cls, sub_cls, mod_cls = contrast[SyncJob.platform_to_int(platform)]
        channels = cha_cls.objects.filter(is_delete=0).order_by('-position')
        if channels and len(channels) > 0:
            channel = cha_cls.objects.get(pk=channel_id, is_delete=0) if channel_id else channels[0]
            subchannels = channel.subchannel.filter(is_delete=0).order_by('-position')
            if subchannels and len(subchannels) > 0:
                subchannel = sub_cls.objects.get(id=subchannel_id, is_delete=0) if subchannel_id else subchannels[0]
                if subchannel.type == 1:  # 子频道下的模块类型
                    modules = subchannel.module.filter(is_delete=0).order_by('-position')
                    if modules and len(modules) > 0:
                        module = mod_cls.objects.get(pk=module_id, is_delete=0) if module_id \
                            else modules[0]
    except Exception, e:
        print e
    finally:
        # print channel.id, channel.title, subchannel.id, subchannel.title, module.id, module.title
        return {
            'channel': channel, 'channels': channels, 'subchannel': subchannel, 'subchannels': subchannels,
            'module': module, 'modules': modules
        }


# depredcated
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


# def update_sync_plan(request):
# if request.method == 'POST':
#         try:
#             param_list = ['id', 'run_type', 'interval', 'cron', 'virtual_name']
#             update_context = {}
#             for param in param_list:
#                 if param == 'interval':
#                     update_context[param] = int(request.POST.get(param, 0)) * 60
#                 else:
#                     update_context[param] = request.POST.get(param)
#             update_context.pop('run_type', None)
#             SyncJob.objects.filter(id=update_context['id']).update(**update_context)
#             get_str = order_url(request.POST.dict())
#             return HttpResponseRedirect(reverse('list_sync_plans') + '?' + get_str[1:])
#         except Exception, e:
#             print e
#             return HttpResponseRedirect(reverse('list_sync_plans'))
#     else:
#         channel_id = request.GET.get('channel_id', '')
#         subchannel_id = request.GET.get('subchannel_id', '')
#         module_id = request.GET.get('module_id', '')
#         platform = request.GET.get('platform')
#         cha_cls, sub_cls, mod_cls = CONTRAST[int(platform)]
#         channel = cha_cls.objects.get(id=channel_id)
#         subchannel = sub_cls.objects.get(id=subchannel_id)
#         module = mod_cls.objects.get(id=module_id)
#         job_id = request.GET.get('job_id')
#         sel_job = SyncJob.objects.get(pk=job_id)
#         sel_job.interval = int(sel_job.interval / 60.0)
#         return render(request, 'syncjob/update_sync_job.html', {'job': sel_job, 'channel': channel,
#                                                                 'subchannel': subchannel,
#                                                                 'module': module,
#                                                                 'platform': platform})


def delete_sync_plan(request):
    get_str = ''
    try:
        job_id = request.GET.get('job_id')
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.delete()
        get_str = order_url(request.GET.dict())
    except ValueError, SyncJob.DoesNotExist:
        pass
    finally:
        return HttpResponseRedirect(reverse('list_sync_plans') + '?' + get_str[1:])


def pack_url(params):
    pack_str = ''
    for key in ['channel', 'subchannel', 'module', 'platform']:
        if key == 'platform':
            pack_str += '&' + key + '=' + params.get(key, '')
        else:
            pack_str += '&' + key + '_id=' + params.get(key + '_id', '')
    return '?' + pack_str[1:]


#deprecated
def order_url(param_dict):
    get_str = ''
    for key in ['channel', 'subchannel', 'module', 'platform']:
        if key == 'platform':
            get_str += '&' + key + '=' + param_dict.get(key, '')
        else:
            get_str += '&select_' + key + '=' + param_dict.get(key + '_id', '')
    return get_str


def run_at_once_plan(request, job_id):
    response = {'status': 'error'}
    try:
        sel_job = SyncJob.objects.get(pk=job_id)
        sel_job.runatonce = 1
        sel_job.save()
        response['status'] = 'success'
    except SyncJob.DoesNotExist:
        pass

    return HttpResponse(json.dumps(response), content_type="application/json")


def log_watch(request, job_id):
    logs = SyncLog.objects.filter(job_id=job_id)
    for index, log in enumerate(logs):
        log.video_id_list = log.ids.split(";")
        log.title_list = log.titles.split(";")
        log.index_list = log.indexes.split(";")
    job = get_object_or_none(SyncJob, pk=job_id)
    return render(request, "syncjob/sync_job_log.html", {'logs': logs, 'job': job})
