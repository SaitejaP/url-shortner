from django.contrib import admin

from .models import *


class UrlMapperAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ['short_url', 'long_url']
    list_display = ('short_url', 'long_url')
    ordering = ('long_url',)
