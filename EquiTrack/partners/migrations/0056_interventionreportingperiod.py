# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-10-09 13:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0055_migrate_intervention_sectors_to_sections'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterventionReportingPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('start_date', models.DateField(verbose_name='Reporting Period Start Date')),
                ('end_date', models.DateField(verbose_name='Reporting Period End Date')),
                ('due_date', models.DateField(verbose_name='Report Due Date')),
                ('intervention', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_periods', to='partners.Intervention')),
            ],
            options={
                'ordering': ['-due_date'],
            },
        ),
    ]
