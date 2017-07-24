# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-07-20 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0005_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audit',
            name='audited_expenditure',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Audited expenditure (USD)'),
        ),
        migrations.AlterField(
            model_name='audit',
            name='financial_findings',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Financial findings (USD)'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='additional_supporting_documentation_provided',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='additional supporting documentation provided'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='amount_refunded',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='amount refunded'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='justification_provided_and_accepted',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='justification provided and accepted'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='pending_unsupported_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='pending unsupported amount'),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='write_off_required',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='write off required'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Amount (USD)'),
        ),
        migrations.AlterField(
            model_name='financialfinding',
            name='local_amount',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Amount (local)'),
        ),
        migrations.AlterField(
            model_name='spotcheck',
            name='total_amount_of_ineligible_expenditure',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total amount of ineligible expenditure'),
        ),
        migrations.AlterField(
            model_name='spotcheck',
            name='total_amount_tested',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True, verbose_name='Total amount tested'),
        ),
    ]
