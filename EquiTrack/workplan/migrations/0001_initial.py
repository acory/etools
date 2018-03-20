# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-11-09 22:23
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reports', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '0001_initial'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('tagged_users', models.ManyToManyField(blank=True, related_name='_comment_tagged_users_+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CoverPage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('national_priority', models.CharField(max_length=255)),
                ('responsible_government_entity', models.CharField(max_length=255)),
                ('planning_assumptions', models.TextField()),
                ('logo', models.ImageField(blank=True, height_field='logo_height', null=True, upload_to='', width_field='logo_width')),
            ],
        ),
        migrations.CreateModel(
            name='CoverPageBudget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('to_date', models.DateField()),
                ('total_amount', models.CharField(max_length=64)),
                ('funded_amount', models.CharField(max_length=64)),
                ('unfunded_amount', models.CharField(max_length=64)),
                ('cover_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgets', to='workplan.CoverPage')),
            ],
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quarter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ResultWorkplanProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assumptions', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('On Track', 'On Track'), ('Constrained', 'Constrained'), ('No Progress', 'No Progress'), ('Target Met', 'Target Met')], max_length=255, null=True)),
                ('prioritized', models.BooleanField(default=False)),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('other_partners', models.CharField(blank=True, max_length=2048, null=True)),
                ('rr_funds', models.PositiveIntegerField(blank=True, null=True)),
                ('or_funds', models.PositiveIntegerField(blank=True, null=True)),
                ('ore_funds', models.PositiveIntegerField(blank=True, null=True)),
                ('total_funds', models.PositiveIntegerField(blank=True, null=True)),
                ('geotag', models.ManyToManyField(related_name='_resultworkplanproperty_geotag_+', to='locations.Location')),
                ('labels', models.ManyToManyField(to='workplan.Label')),
                ('partners', models.ManyToManyField(related_name='_resultworkplanproperty_partners_+', to='partners.PartnerOrganization')),
                ('responsible_persons', models.ManyToManyField(related_name='_resultworkplanproperty_responsible_persons_+', to=settings.AUTH_USER_MODEL)),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workplan_properties', to='reports.Result')),
                ('sections', models.ManyToManyField(related_name='_resultworkplanproperty_sections_+', to='users.Section')),
            ],
        ),
        migrations.CreateModel(
            name='Workplan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('On Track', 'On Track'), ('Constrained', 'Constrained'), ('No Progress', 'No Progress'), ('Target Met', 'Target Met')], max_length=32, null=True)),
                ('country_programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reports.CountryProgramme')),
            ],
        ),
        migrations.CreateModel(
            name='WorkplanProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workplan_projects', to='workplan.Workplan')),
            ],
        ),
        migrations.AddField(
            model_name='resultworkplanproperty',
            name='workplan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workplan.Workplan'),
        ),
        migrations.AddField(
            model_name='quarter',
            name='workplan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quarters', to='workplan.Workplan'),
        ),
        migrations.AddField(
            model_name='coverpage',
            name='workplan_project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cover_page', to='workplan.WorkplanProject'),
        ),
        migrations.AddField(
            model_name='comment',
            name='workplan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='workplan.Workplan'),
        ),
    ]
