# Generated by Django 1.10.8 on 2018-03-08 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tpmpartners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tpmpartner',
            name='city',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='email',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='Phone Number'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=32, verbose_name='Postal Code'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='street_address',
            field=models.CharField(blank=True, default='', max_length=500, verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='tpmpartner',
            name='vendor_number',
            field=models.CharField(blank=True, default='', max_length=30, unique=True, verbose_name='Vendor Number'),
        ),
    ]
