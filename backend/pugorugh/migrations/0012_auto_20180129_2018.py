# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-29 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0011_auto_20180129_2015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='age',
            field=models.CharField(default='b', max_length=10),
        ),
    ]
