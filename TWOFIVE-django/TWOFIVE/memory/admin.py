# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from models import *


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'pub_date', 'update_time',)

    def save_model(self, request, obj, form, change):
        if change:  # 更改的时候
            obj_original = self.model.objects.get(pk=obj.pk)
        else:  # 新增的时候
            obj_original = None

        obj.user = request.user
        obj.save()
    def delete_model(self, request, obj):
        """
        Given a model instance delete it from the database.
        """
        # handle something here
        obj.delete()


admin.site.register(User)
admin.site.register(Article, ArticleAdmin)