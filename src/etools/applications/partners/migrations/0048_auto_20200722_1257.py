# Generated by Django 2.2.7 on 2020-07-22 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('partners', '0047_auto_20200721_1842'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='capacity_development',
            field=models.TextField(blank=True, verbose_name='Capacity Development'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='other_info',
            field=models.TextField(blank=True, verbose_name='Other Info'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='other_partners_involved',
            field=models.TextField(blank=True, verbose_name='Other Partners Involved'),
        ),
        migrations.AddField(
            model_name='intervention',
            name='technical_guidance',
            field=models.TextField(blank=True, verbose_name='Technical Guidance'),
        ),
    ]
