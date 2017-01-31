# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-30 14:30
from __future__ import unicode_literals

from django.db import migrations


def reverse(apps, schema_editor):
    pass

def bank_details_to_partner(apps, schema_editor):
    BankDetails = apps.get_model('partners', 'BankDetails')
    bds = BankDetails.objects.all()
    if bds.count() > 0:
        for bd in bds:
            if not bd.partner_organization:
                bd.partner_organization = bd.agreement.partner
                print(bd.partner_organization.name)
                bd.save()


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0015_auto_20170127_2140'),
    ]

    operations = [
        migrations.RunPython(
            bank_details_to_partner, reverse_code=reverse
        ),
        migrations.RemoveField(
            model_name='bankdetails',
            name='agreement',
        ),
    ]
