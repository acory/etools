# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-05-14 11:04
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import etools.applications.EquiTrack.utils
import model_utils.fields


def migrate_data(apps, schema):
    PartnerPlannedVisits = apps.get_model("partners", "partnerplannedvisits")
    InterventionPlannedVisits = apps.get_model(
        "partners",
        "interventionplannedvisits"
    )
    for visit in InterventionPlannedVisits.objects.all():
        partner = visit.intervention.agreement.partner
        partner_visit, _ = PartnerPlannedVisits.objects.get_or_create(
            partner=partner,
            year=visit.year,
        )
        partner_visit.programmatic_q1 += visit.programmatic_q1
        partner_visit.programmatic_q2 += visit.programmatic_q2
        partner_visit.programmatic_q3 += visit.programmatic_q3
        partner_visit.programmatic_q4 += visit.programmatic_q4
        partner_visit.save()


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0009_auto_20180510_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerPlannedVisits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('year', models.IntegerField(default=etools.applications.EquiTrack.utils.get_current_year, verbose_name='Year')),
                ('programmatic_q1', models.IntegerField(default=0, verbose_name='Programmatic Q1')),
                ('programmatic_q2', models.IntegerField(default=0, verbose_name='Programmatic Q2')),
                ('programmatic_q3', models.IntegerField(default=0, verbose_name='Programmatic Q3')),
                ('programmatic_q4', models.IntegerField(default=0, verbose_name='Programmatic Q4')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_visits', to='partners.PartnerOrganization', verbose_name='Partner')),
            ],
            options={
                'verbose_name_plural': 'Partner Planned Visits',
            },
        ),
        migrations.AlterUniqueTogether(
            name='partnerplannedvisits',
            unique_together=set([('partner', 'year')]),
        ),
        migrations.RunPython(migrate_data, migrations.RunPython.noop)
    ]
