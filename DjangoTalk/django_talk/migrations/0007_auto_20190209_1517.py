# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2019-02-09 07:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_talk', '0006_auto_20190131_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='black_list',
            field=models.ManyToManyField(blank=True, related_name='be_forbiden', to=settings.AUTH_USER_MODEL, verbose_name='黑名单'),
        ),
        migrations.AlterField(
            model_name='chatroom',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='be_members', to=settings.AUTH_USER_MODEL, verbose_name='当前频道内成员'),
        ),
    ]