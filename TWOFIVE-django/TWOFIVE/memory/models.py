# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
import os
from TWOFIVE.settings import MEDIA_URL

# Create your models here.

# 用户数据库
class User(AbstractUser):
    nickname=models.CharField(max_length=50,blank=True)
    title=models.CharField(max_length=120,blank=True,default=u'总要有一个拿来回忆的地方')
    portrait_url=models.CharField(max_length=200,blank=True,default=os.path.join(MEDIA_URL,'default.png'))

    class Meta(AbstractUser.Meta):
        pass

    def __unicode__(self):
        return self.username