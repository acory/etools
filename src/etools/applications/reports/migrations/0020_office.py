# Generated by Django 2.2.4 on 2019-10-11 12:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reports', '0019_auto_20190816_1609'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254, verbose_name='Name')),
                ('zonal_chief', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offices', to=settings.AUTH_USER_MODEL, verbose_name='Chief')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]
