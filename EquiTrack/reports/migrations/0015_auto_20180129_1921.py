# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2018-01-29 19:21
from __future__ import unicode_literals, print_function

from django.db import migrations, models, connection
from django.utils import six
import django.utils.timezone
import model_utils.fields
import mptt.fields

from django.db.models import Q


def myprint(*args):
    print(*args)
    file_name = 'migration_reports_0015.txt'
    args_list = [six.text_type(arg) for arg in args]
    with open(file_name, 'ab') as f:
        f.write(', '.join(args_list))
        f.write('\n')

def initiate_migrations(apps, schema_editor):
    myprint(' ########################  ', connection.schema_name)
    myprint(' ')
    AppliedIndicator = apps.get_model('reports', 'AppliedIndicator')
    IndicatorBlueprint = apps.get_model('reports', 'IndicatorBlueprint')

    # Delete all Applied indicators that do not have lower_results
    nind = AppliedIndicator.objects.filter(lower_result__isnull=True).all().delete()
    myprint(' Number of Applied indicators without results : ', nind)

    # Delete all IndicatorBlueprints that do not have applied indicators
    nind = IndicatorBlueprint.objects.filter(appliedindicator__isnull=True).all().delete()
    myprint(' Number of Blueprint indicators without Applied Indicators : ', nind)

def check_fields(apps, schema_editor):
    AppliedIndicator = apps.get_model('reports', 'AppliedIndicator')

    ainds = AppliedIndicator.objects.all()

    myprint('number of applied indicators indicators checked: ', ainds.count())

    for aind in ainds:
        try:
            int(aind.target)
            if aind.baseline is not None:
                int(aind.baseline)

            assert int(aind.target) >= 0
        except:
            myprint('bad indicator: ',
                    ' '.join(six.text_type(i) for i in ['id', aind.id, 'target', aind.target, 'baseline', aind.baseline,
                                                  'interventionid', aind.lower_result.result_link.intervention.id]))

            if not aind.target:
                aind.target = 0
                aind.save()
                myprint('FIXED TARGET')

            else:
                aind.target = aind.target.replace(',', '')
                aind.target = aind.target.replace('.', '')
                if int(aind.target) < 0:
                    aind.target = 0
                aind.save()
                myprint('FIXED TARGET')

            if aind.baseline == '':
                aind.baseline = None
                myprint('FIXED BASELINE')
                aind.save()
            elif aind.baseline:
                aind.baseline = aind.baseline.replace(',', '')
                aind.baseline = aind.baseline.replace('.', '')
                if int(aind.baseline) < 0:
                    aind.baseline = 0
                aind.save()
                myprint('FIXED BASELINE')

def reverse_unit(apps, schema_editor):
    pass
    # raise Exception('YesNo indicators cannot be migrated backwards')


def change_unit(apps, schema_editor):
    AppliedIndicator = apps.get_model('reports', 'AppliedIndicator')\

    # indicator blueprint unit migration (indicator type if type yes/no move to quantity, target is 1 baseline 0)

    yesno_indicators = AppliedIndicator.objects.filter(Q(indicator__unit='yesno') |
                                                       Q(target='yes')).all()

    myprint('number of yesno indicators updated: ', yesno_indicators.count())

    for aind in yesno_indicators:
        aind.indicator.unit = 'number'
        aind.indicator.save()
        aind.target = 1
        aind.baseline = 0
        aind.save()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0006_auto_20171024_1011'),
        ('reports', '0014_auto_20171013_2147'),
        ('partners', '0058_intervention_locations'),
    ]

    operations = [
        migrations.RunPython(initiate_migrations, migrations.RunPython.noop),

        migrations.RunPython(change_unit, reverse_code=reverse_unit),

        migrations.RunPython(check_fields, migrations.RunPython.noop),
    ]
