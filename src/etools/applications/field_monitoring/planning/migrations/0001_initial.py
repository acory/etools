# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-11-22 15:25
from __future__ import unicode_literals

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import django.utils.timezone
from django.utils.timezone import utc
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locations', '0004_pcode_remap_related'),
        ('partners', '0028_auto_20181108_1503'),
        ('field_monitoring_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(default=datetime.datetime(1970, 1, 1, 0, 0, tzinfo=utc), verbose_name='Deleted At')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('plan_by_month', django.contrib.postgres.fields.ArrayField(base_field=models.PositiveSmallIntegerField(blank=True, default=0), blank=True, default=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], size=None, verbose_name='Plan By Month')),
                ('cp_output_config', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='field_monitoring_settings.CPOutputConfig', verbose_name='CP Output Config')),
                ('intervention', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='partners.Intervention', verbose_name='PD or SSFA')),
                ('location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='locations.Location', verbose_name='Location')),
                ('location_site', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='field_monitoring_settings.LocationSite', verbose_name='Site')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='partners.PartnerOrganization', verbose_name='Partner')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('admin_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='YearPlan',
            fields=[
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('year', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('prioritization_criteria', models.TextField(blank=True, verbose_name='Prioritization Criteria')),
                ('methodology_notes', models.TextField(blank=True, verbose_name='Methodology Notes & Standards')),
                ('target_visits', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='Target Visits For The Year')),
                ('modalities', models.TextField(blank=True, verbose_name='Modalities')),
                ('partner_engagement', models.TextField(blank=True, verbose_name='Partner Engagement')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='task',
            name='year_plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='field_monitoring_planning.YearPlan', verbose_name='Year Plan'),
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ('id',), 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.AlterModelOptions(
            name='yearplan',
            options={'ordering': ('year',), 'verbose_name': 'Year Plan', 'verbose_name_plural': 'Year Plans'},
        ),
    ]
