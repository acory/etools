# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-02 13:38
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0007_auto_20180502_0938'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='risk',
            unique_together=set([]),
        ),
    ]
