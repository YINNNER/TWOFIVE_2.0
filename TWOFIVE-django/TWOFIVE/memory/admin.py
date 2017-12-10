# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


class ArticleAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()



admin.site.register(User)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Mood)