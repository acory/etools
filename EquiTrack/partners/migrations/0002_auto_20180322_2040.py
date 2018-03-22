# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-03-22 20:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0001_initial'),
        ('funds', '0002_auto_20180322_2040'),
        ('users', '0001_initial'),
        ('locations', '0001_initial'),
        ('partners', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interventionsectorlocationlink',
            name='sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervention_locations', to='reports.Sector'),
        ),
        migrations.AddField(
            model_name='interventionresultlink',
            name='cp_output',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='intervention_links', to='reports.Result'),
        ),
        migrations.AddField(
            model_name='interventionresultlink',
            name='intervention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_links', to='partners.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionresultlink',
            name='ram_indicators',
            field=models.ManyToManyField(blank=True, to='reports.Indicator'),
        ),
        migrations.AddField(
            model_name='interventionreportingperiod',
            name='intervention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_periods', to='partners.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionplannedvisits',
            name='intervention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_visits', to='partners.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionbudget',
            name='intervention',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='planned_budget', to='partners.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionattachment',
            name='intervention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='partners.Intervention'),
        ),
        migrations.AddField(
            model_name='interventionattachment',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='partners.FileType'),
        ),
        migrations.AddField(
            model_name='interventionamendment',
            name='intervention',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amendments', to='partners.Intervention', verbose_name='Reference Number'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interventions', to='partners.Agreement', verbose_name='Agreement'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='country_programme',
            field=models.ForeignKey(blank=True, help_text='Which Country Programme does this Intervention belong to?', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='interventions', to='reports.CountryProgramme', verbose_name='Country Programme'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='flat_locations',
            field=models.ManyToManyField(blank=True, related_name='intervention_flat_locations', to='locations.Location'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='offices',
            field=models.ManyToManyField(blank=True, related_name='_intervention_offices_+', to='users.Office', verbose_name='Office'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_authorized_officer_signatory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signed_interventions', to='partners.PartnerStaffMember', verbose_name='Signed by Partner'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_focal_points',
            field=models.ManyToManyField(blank=True, related_name='_intervention_partner_focal_points_+', to='partners.PartnerStaffMember', verbose_name='CSO Authorized Officials'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='interventions', to='reports.Sector', verbose_name='Sections'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='unicef_focal_points',
            field=models.ManyToManyField(blank=True, related_name='_intervention_unicef_focal_points_+', to=settings.AUTH_USER_MODEL, verbose_name='UNICEF Focal Points'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='unicef_signatory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='signed_interventions+', to=settings.AUTH_USER_MODEL, verbose_name='Signed by UNICEF'),
        ),
        migrations.AddField(
            model_name='fundingcommitment',
            name='grant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='funds.Grant'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='approving_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Approving Officer'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assessments', to='partners.PartnerOrganization', verbose_name='Partner'),
        ),
        migrations.AddField(
            model_name='assessment',
            name='requesting_officer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requested_assessments', to=settings.AUTH_USER_MODEL, verbose_name='Requesting Officer'),
        ),
        migrations.AddField(
            model_name='agreementamendment',
            name='agreement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amendments', to='partners.Agreement', verbose_name='Agreement'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='authorized_officers',
            field=models.ManyToManyField(blank=True, related_name='agreement_authorizations', to='partners.PartnerStaffMember', verbose_name='Partner Authorized Officer'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='country_programme',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='reports.CountryProgramme', verbose_name='Country Programme'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agreements', to='partners.PartnerOrganization'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='partner_manager',
            field=smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='partner', chained_model_field='partner', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreements_signed', to='partners.PartnerStaffMember', verbose_name='Signed by partner'),
        ),
        migrations.AddField(
            model_name='agreement',
            name='signed_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agreements_signed+', to=settings.AUTH_USER_MODEL, verbose_name='Signed By UNICEF'),
        ),
        migrations.AlterUniqueTogether(
            name='interventionplannedvisits',
            unique_together=set([('intervention', 'year')]),
        ),
    ]
