# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-03-26 08:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('release', '0004_auto_20190326_1605'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='create_time',
            field=models.DateField(auto_created=True, auto_now_add=True, verbose_name='创建时间'),
        ),
    ]
