# Generated by Django 2.1.5 on 2019-02-27 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('audit', '0013_auto_20190102_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskblueprint',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order'),
        ),
        migrations.AlterField(
            model_name='riskcategory',
            name='order',
            field=models.PositiveIntegerField(db_index=True, editable=False, verbose_name='order'),
        ),
    ]
