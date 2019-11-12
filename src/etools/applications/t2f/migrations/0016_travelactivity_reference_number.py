# Generated by Django 2.2.3 on 2019-08-14 12:34

from django.db import migrations, models


def set_reference_number(apps, schema_editor):
    TravelActivity = apps.get_model("t2f", "travelactivity")
    for activity in TravelActivity.objects.all():
        travel = activity.travels.filter(
            traveler=activity.primary_traveler
        ).first()
        if travel:
            activity.reference_number = travel.reference_number
            activity.save()


class Migration(migrations.Migration):

    dependencies = [
        ('t2f', '0015_auto_20190326_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelactivity',
            name='reference_number',
            field=models.CharField(max_length=12, null=True, verbose_name='Reference Number'),
        ),
        migrations.RunPython(set_reference_number),
    ]
