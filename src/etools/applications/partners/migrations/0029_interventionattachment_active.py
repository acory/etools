# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-14 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0028_auto_20181108_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='interventionattachment',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
