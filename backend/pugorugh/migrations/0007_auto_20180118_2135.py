# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-18 21:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0006_auto_20180109_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdog',
            name='status',
            field=models.CharField(choices=[('l', 'Liked'), ('d', 'disliked')], default='', max_length=10),
        ),
    ]