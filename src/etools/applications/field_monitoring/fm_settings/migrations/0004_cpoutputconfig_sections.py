# Generated by Django 2.0.9 on 2018-12-27 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20180709_1348'),
        ('field_monitoring_settings', '0003_remove_plannedchecklistitem_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='cpoutputconfig',
            name='sections',
            field=models.ManyToManyField(blank=True, to='reports.Section', verbose_name='Sections'),
        ),
    ]
