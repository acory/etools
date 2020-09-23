# Generated by Django 2.2.7 on 2020-09-14 07:58

from django.db import migrations


def create_budgets(apps, schema_editor):
    Intervention = apps.get_model('partners', 'Intervention')
    InterventionBudget = apps.get_model('partners', 'InterventionBudget')
    InterventionManagementBudget = apps.get_model('partners', 'InterventionManagementBudget')

    for i in Intervention.objects.all():
        InterventionBudget.objects.get_or_create(
            intervention=i,
            defaults={
                "total": 0,
            }
        )
        InterventionManagementBudget.objects.get_or_create(intervention=i)


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0060_auto_20200908_0839'),
    ]

    operations = [
        migrations.RunPython(create_budgets, migrations.RunPython.noop)
    ]
