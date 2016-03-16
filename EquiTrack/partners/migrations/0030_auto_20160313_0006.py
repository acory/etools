# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0029_auto_20160308_0142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partnerorganization',
            name='rating',
            field=models.CharField(default='High', max_length=50, verbose_name='Risk Rating'),
        ),
    ]
