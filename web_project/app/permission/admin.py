#coding=utf-8
from models import *
from django.core import urlresolvers
from django.contrib import admin
from django.contrib.auth.models import Permission




class PermAdmin(admin.ModelAdmin):
    list_display = ('name','code','url_regex', 'action')
    list_display_links = ('name',)
    search_fields = ['name']
    readonly_fields = ('code','url_regex','action')


admin.site.register(Perm,PermAdmin)
# admin.site.register(Permission)