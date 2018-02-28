# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-21 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('funds', '0010_auto_20171024_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundsreservationheader',
            name='actual_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Actual Cash Transfer Local'),
        ),
        migrations.AddField(
            model_name='fundsreservationheader',
            name='outstanding_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='Outstanding DCT Local'),
        ),
        migrations.AddField(
            model_name='fundsreservationheader',
            name='total_amt_local',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12, verbose_name='FR Overall Amount DC'),
        ),
    ]
