# Generated by Django 2.2.1 on 2019-08-28 11:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_settings', '0009_auto_20190827_1000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='value',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Value'),
        ),
    ]
