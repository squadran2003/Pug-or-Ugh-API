# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-02-06 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0013_auto_20180129_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(default='m', max_length=10),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(default='s', max_length=10),
        ),
    ]
