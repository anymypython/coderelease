# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0002_remove_host_isadmin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='dev',
            field=models.ManyToManyField(related_name='dev_user', to='release.UserProfile', verbose_name='研发人员'),
        ),
    ]
