# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-09-28 07:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0050_auto_20170914_1510'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='governmentinterventionresult',
            name='activities',
        ),
    ]
