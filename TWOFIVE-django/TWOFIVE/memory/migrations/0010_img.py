# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-09 19:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memory', '0009_article_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMG',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='upload')),
            ],
        ),
    ]