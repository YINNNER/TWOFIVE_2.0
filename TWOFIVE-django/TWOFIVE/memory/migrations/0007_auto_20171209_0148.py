# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 01:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0006_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256, verbose_name='\u6807\u9898')),
                ('content', models.TextField(blank=True, default='', verbose_name='\u5185\u5bb9')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='\u53d1\u8868\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('summary', models.CharField(max_length=244, verbose_name='\u6587\u7ae0\u6982\u8981')),
                ('poll_count', models.IntegerField(default=0, verbose_name='\u70b9\u8d5e\u6570')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005')),
            ],
        ),
        migrations.CreateModel(
            name='Article_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='\u6587\u7ae0\u5185\u5bb9')),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='memory.Article1', verbose_name='\u6240\u5c5e\u6587\u7ae0')),
            ],
        ),
        migrations.CreateModel(
            name='Article_poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='\u70b9\u8d5e\u65f6\u95f4')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='memory.Article1', verbose_name='\u70b9\u8d5e\u6587\u7ae0')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u70b9\u8d5e\u4eba')),
            ],
            options={
                'verbose_name_plural': '\u6587\u7ae0\u70b9\u8d5e\u8868',
            },
        ),
        migrations.CreateModel(
            name='Mood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=32, verbose_name='\u5fc3\u60c5')),
                ('url', models.CharField(max_length=64, unique=True, verbose_name='\u540e\u7f00')),
                ('theme', models.CharField(max_length=32, verbose_name='\u4e3b\u9898')),
                ('author', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6240\u5c5e\u7528\u6237')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='name',
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u8bc4\u8bba\u4eba'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memory.Article1', verbose_name='\u8bc4\u8bba\u6587\u7ae0'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.CharField(max_length=265, verbose_name='\u8bc4\u8bba\u5185\u5bb9'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u8bc4\u8bba\u65f6\u95f4'),
        ),
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.AddField(
            model_name='article1',
            name='mood',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='memory.Mood', verbose_name='\u6240\u5c5e\u7c7b\u522b'),
        ),
        migrations.AlterUniqueTogether(
            name='article_poll',
            unique_together=set([('author', 'article')]),
        ),
    ]
