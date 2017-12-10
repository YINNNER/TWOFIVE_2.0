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
    "用户表"
    nickname=models.CharField(max_length=50,blank=True)
    title=models.CharField(max_length=120,blank=True,default=u'总要有一个拿来回忆的地方')
    portrait_url=models.CharField(max_length=200,blank=True,default=os.path.join(MEDIA_URL,'default.png'))

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.username


#文章数据库
class Article(models.Model):
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['pub_date']
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('p', 'Published'),
    )

    title = models.CharField(u'标题', max_length=256)
    author =models.ForeignKey(to="User",verbose_name="作者", null=True, blank=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    content = models.TextField(u'内容', default='', blank=True)
    mood = models.ForeignKey(to="Mood", verbose_name="所属类别", null=True, on_delete=models.SET_NULL)
    limit=models.ForeignKey(to="Limit",verbose_name="权限", null=True, blank=True)
    pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable=True)

    summary = models.CharField(u'摘要', max_length=54, blank=True, null=True,
                                help_text="可选，如若为空将摘取正文的前54个字符")
    # topped = models.BooleanField(u'置顶', default=False)
    poll_count = models.PositiveIntegerField(verbose_name="点赞数", default=0)
    score=models.IntegerField(verbose_name="分数", default=0)
    img=models.ForeignKey(to="IMG")

    def __str__(self):
        return self.title + "+" + self.author.username

    class Meta:
        ordering = ['-pub_date']


#评论
class Comment(models.Model):
    "评论表"
    article=models.ForeignKey(to="Article", verbose_name='评论文章')
    author=models.ForeignKey(to="User",verbose_name="评论人",null=True,blank=True)
    content = models.CharField(max_length=265,verbose_name="评论内容")
    created = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)

    def __str__(self):
        return self.author.nickname + "----" + self.article.title + "+" + self.article.author.username



class Article_detail(models.Model):
    "文章细节表"
    article = models.OneToOneField(to="Article",verbose_name="所属文章")
    content =models.TextField(verbose_name="文章内容")

    def __str__(self):
        return self.article.title




class Article_poll(models.Model):
    "文章点赞表"
    created = models.DateTimeField(verbose_name="点赞时间",auto_now_add=True)
    article = models.ForeignKey(to="Article",verbose_name="点赞文章",null=True,blank=True)   #一个文章可以有多个赞
    author = models.ForeignKey(to="User",verbose_name="点赞人",null=True,blank=True)


    class Meta:
        "联合唯一"
        unique_together = ("author", "article",)
        verbose_name_plural = "文章点赞表"
    def __str__(self):
        return self.author.nickname+"---"+self.article.title+"+"+self.article.author.username




class Mood(models.Model):
    "心情表"
    color = models.CharField(max_length=32,verbose_name="心情")
    # url = models.CharField(max_length=64,verbose_name="后缀",unique=True)
    # theme = models.CharField(max_length=32,verbose_name="主题")
    author= models.OneToOneField(to="User", verbose_name="所属用户")

    def __str__(self):
        return self.color

class Limit(models.Model):
    limit=models.CharField(max_length=32,verbose_name="权限")
    author = models.OneToOneField(to="User", verbose_name="所属用户")
    def __str__(self):
        return self.limit

class IMG(models.Model):
    img=models.ImageField(upload_to='upload')