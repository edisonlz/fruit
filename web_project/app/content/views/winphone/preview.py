# coding: utf8
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


def preview(request):

    return render(request, 'winphone/preview/preview_index.html')
