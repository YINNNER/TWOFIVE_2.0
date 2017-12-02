# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm

# Create your models here.

# 用户数据库
class User(AbstractUser):
    nickname=models.CharField(max_length=50,blank=True)

    class Meta(AbstractUser.Meta):
        pass

    def __unicode__(self):
        return self.username