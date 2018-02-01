# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2018-01-29 20:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pugorugh', '0012_auto_20180129_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpref',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female')], default='m', max_length=10),
        ),
        migrations.AlterField(
            model_name='userpref',
            name='size',
            field=models.CharField(choices=[('s', 'small'), ('m', 'medium'), ('l', 'large'), ('xl', 'extra large')], default='s', max_length=10),
        ),
    ]