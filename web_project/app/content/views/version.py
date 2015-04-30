# coding=utf8
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json

from app.content.models import VersionControl, VersionFeature


@login_required
def versions(request):
    if request.method == 'GET':
        platform_versions = VersionControl.objects.all().order_by('platform', 'version')
        return render(request, 'version/versions.html', locals())


@login_required
def version_add(request):
    if request.method == 'POST':
        platform_id = request.POST.get('platform_id')
        version = request.POST.get('version')
        VersionControl.objects.create(platform=platform_id, version=version)

        return HttpResponseRedirect(reverse('versions', ))


@login_required
def version_delete(request):
    if request.method == 'GET':
        version_id = request.GET.get('id')
        VersionControl.objects.filter(pk=version_id).delete()

        return HttpResponseRedirect(reverse('versions', ))


@login_required
def features(request):
    if request.method == 'GET':
        features = VersionFeature.objects.all().order_by('platform', 'feature', 'value')
        versions = sorted(set([i.version for i in VersionControl.objects.all().order_by('version')]))
        box_type_features = VersionFeature.get_all_box_type_features()
        video_type_features = VersionFeature.get_all_video_type_feature()
        feature_value_dict = {}
        for i in video_type_features:
            feature_value_dict[i['name']] = i['desc']
        for i in box_type_features:
            feature_value_dict[i['name']] = i['desc']
        print feature_value_dict

        return render(request, 'version/features.html', locals())


@login_required
def feature_delete(request):
    if request.method == 'GET':
        pk = request.GET.get('id')
        VersionFeature.objects.filter(pk=pk).delete()

        return HttpResponseRedirect(reverse('features', ))


@login_required
def feature_add(request):
    if request.method == 'POST':
        platform_id = request.POST.get('platform_id')
        version_begin = request.POST.get('version_begin')
        version_end = request.POST.get('version_end')
        feature_type = request.POST.get('feature_type')
        feature_value = request.POST.get('feature_value')
        VersionFeature.objects.create(platform=platform_id, version_begin=version_begin, version_end=version_end,
                                      feature=feature_type, value=feature_value)

        return HttpResponseRedirect(reverse('features', ))


@login_required
def feature_edit(request):
    pass
