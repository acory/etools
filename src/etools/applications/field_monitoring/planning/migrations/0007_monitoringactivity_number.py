# Generated by Django 2.2.7 on 2020-02-05 13:46

from django.db import connection, migrations, models


def assign_reference_number(apps, schema_editor):
    MonitoringActivity = apps.get_model('field_monitoring_planning', 'MonitoringActivity')

    for activity in MonitoringActivity.admin_objects.all():
        activity.number = '{}/{}/{}/FMA'.format(
            connection.tenant.country_short_code or '',
            activity.created.year,
            activity.id,
        )
        activity.save(update_fields=['number'])


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_planning', '0006_monitoringactivity_report_reject_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoringactivity',
            name='number',
            field=models.CharField(blank=True, editable=False, max_length=64, null=True, unique=True, verbose_name='Reference Number'),
        ),
        migrations.RunPython(assign_reference_number, migrations.RunPython.noop),
    ]
