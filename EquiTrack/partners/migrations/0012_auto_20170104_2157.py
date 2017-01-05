# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-01-04 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0011_auto_20170103_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interventionamendment',
            name='type',
            field=models.CharField(choices=[('CPR', b'Change in Programme Result'), ('CPF', b'Change in Population Focus'), ('CGC', b'Change in Georgraphical Coverage'), ('CTBGT20', b'Change in Total Budget >20%'), ('CTBLT20', b'Change in Total Budget <=20%'), ('CABLT20', b'Changes in Activity Budget <=20% - No Change in Total Budget'), ('CABGT20', b'Changes in Activity Budget >20% - No Change in Total Budget - Prior approval in authorized FACE'), ('CABGT20FACE', b'Changes in Activity Budget >20% - No Change in Total Budget - Reporting at FACE')], max_length=50),
        ),
        migrations.AlterUniqueTogether(
            name='interventionbudget',
            unique_together=set([('year', 'intervention')]),
        ),
    ]
