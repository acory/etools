# Generated by Django 2.0.9 on 2019-01-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('field_monitoring_data_collection', '0002_auto_20181212_0844'),
        ('field_monitoring_visits', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unicefvisit',
            name='visit_ptr',
        ),
        migrations.AddField(
            model_name='visit',
            name='visit_type',
            field=models.CharField(choices=[('staff', 'Staff'), ('tpm', 'TPM')], default='staff', max_length=10),
        ),
        migrations.DeleteModel(
            name='UNICEFVisit',
        ),
    ]
