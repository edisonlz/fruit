# coding=utf8
from app.content.models import CidDetail
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse


@login_required
def cids(request):
    cids = CidDetail.objects.filter(is_delete=False).order_by('cid')
    all_cid_num = '|'.join([str(i.cid) for i in cids])
    return render(request, 'cid/cids.html', locals())


@login_required
def add_cid(request):
    if request.method == 'POST':
        print request.POST
        args = request.POST.dict()
        CidDetail.objects.create(cid=args.get('cid'), title=args.get('title'),
                                 is_youku_channel=args.get('is_youku_channel'))
        return HttpResponseRedirect(reverse('cids'))


@login_required
def cid_edit(request):
    if request.method == 'GET':
        pk = request.GET.get('id')
        cid = CidDetail.objects.get(pk=pk)
        return render(request, 'cid/cid_edit.html', locals())
    if request.method == 'POST':
        print request.POST.dict()
        args = request.POST.dict()
        cid = CidDetail.objects.get(pk=args.get('id'))
        cid.title = args.get('title')
        cid.is_youku_channel = int(args.get('is_youku_channel'))
        cid.save()
        return HttpResponseRedirect(reverse('cids'))


@login_required
def delete_cid(request):
    pass