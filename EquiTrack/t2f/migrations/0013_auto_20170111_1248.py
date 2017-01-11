# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-11 10:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0012_invoice_vision_fi_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelpermission',
            name='usage_place',
            field=models.CharField(choices=[('travel', 'Travel'), ('action_point', 'Action point')], default='travel', max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('processing', 'Processing'), ('success', 'Success'), ('error', 'Error')], max_length=16),
        ),
        migrations.AlterField(
            model_name='travelpermission',
            name='status',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='travelpermission',
            name='user_type',
            field=models.CharField(max_length=25),
        ),
    ]
