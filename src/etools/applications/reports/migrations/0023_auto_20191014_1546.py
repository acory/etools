# Generated by Django 2.2.4 on 2019-10-14 15:46

from django.db import connection, migrations
from django_tenants.utils import get_public_schema_name


def convert_tenant_profile_data(apps, schema):
    """For each UserProfile setup office relation in ProfileOffice
    for each country that UserProfile has available
    Use the connection to determine the current country
    """
    UserProfile = apps.get_model("users", "userprofile")
    UserTenantProfile = apps.get_model("reports", "usertenantprofile")
    Office = apps.get_model("reports", "office")
    country = connection.tenant
    country_name= getattr(country, "name", None)
    if country_name and country_name != get_public_schema_name():
        for profile in UserProfile.objects.all():
            if country in profile.countries_available.all():
                office = Office.objects.get(pk=profile.office.pk)
                UserTenantProfile.objects.create(
                    profile=profile,
                    office=office,
                )


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0022_userprofileoffice'),
    ]

    operations = [
        migrations.RunPython(
            convert_tenant_profile_data,
            reverse_code=migrations.RunPython.noop,
        )
    ]
