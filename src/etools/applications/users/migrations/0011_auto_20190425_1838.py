# Generated by Django 2.1.8 on 2019-04-25 18:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20190423_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='threshold_tae_usd',
        ),
        migrations.RemoveField(
            model_name='country',
            name='threshold_tre_usd',
        ),
    ]
