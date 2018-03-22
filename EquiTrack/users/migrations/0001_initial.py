# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-22 20:40
from __future__ import unicode_literals

from decimal import Decimal
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import tenant_schemas.postgresql_backend.base


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('publics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_url', models.CharField(max_length=128, unique=True)),
                ('schema_name', models.CharField(max_length=63, unique=True, validators=[tenant_schemas.postgresql_backend.base._check_schema_name])),
                ('name', models.CharField(max_length=100)),
                ('country_short_code', models.CharField(blank=True, max_length=10, null=True)),
                ('long_name', models.CharField(blank=True, max_length=255, null=True)),
                ('business_area_code', models.CharField(blank=True, max_length=10, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('-90')), django.core.validators.MaxValueValidator(Decimal('90'))])),
                ('longitude', models.DecimalField(blank=True, decimal_places=5, max_digits=8, null=True, validators=[django.core.validators.MinValueValidator(Decimal('-180')), django.core.validators.MaxValueValidator(Decimal('180'))])),
                ('initial_zoom', models.IntegerField(default=8)),
                ('vision_sync_enabled', models.BooleanField(default=True)),
                ('vision_last_synced', models.DateTimeField(blank=True, null=True)),
                ('threshold_tre_usd', models.DecimalField(decimal_places=4, default=None, max_digits=20, null=True)),
                ('threshold_tae_usd', models.DecimalField(decimal_places=4, default=None, max_digits=20, null=True)),
                ('local_currency', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='workspaces', to='publics.Currency')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('zonal_chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offices', to=settings.AUTH_USER_MODEL, verbose_name=b'Chief')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('code', models.CharField(blank=True, max_length=32, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.CharField(max_length=40, null=True, unique=True)),
                ('partner_staff_member', models.IntegerField(blank=True, null=True)),
                ('job_title', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('staff_id', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('org_unit_code', models.CharField(blank=True, max_length=32, null=True)),
                ('org_unit_name', models.CharField(blank=True, max_length=64, null=True)),
                ('post_number', models.CharField(blank=True, max_length=32, null=True)),
                ('post_title', models.CharField(blank=True, max_length=64, null=True)),
                ('vendor_number', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('section_code', models.CharField(blank=True, max_length=32, null=True)),
                ('countries_available', models.ManyToManyField(blank=True, related_name='accessible_by', to='users.Country')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Country')),
                ('country_override', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country_override', to='users.Country')),
                ('office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Office')),
                ('oic', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.Section')),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisee', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkspaceCounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('travel_reference_number_counter', models.PositiveIntegerField(default=1)),
                ('travel_invoice_reference_number_counter', models.PositiveIntegerField(default=1)),
                ('workspace', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='counters', to='users.Country')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='offices',
            field=models.ManyToManyField(related_name='offices', to='users.Office'),
        ),
        migrations.AddField(
            model_name='country',
            name='sections',
            field=models.ManyToManyField(related_name='sections', to='users.Section'),
        ),
    ]
