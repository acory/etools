# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-20 12:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0011_auto_20181119_1343'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logissue',
            name='date_of_close',
        ),
    ]
