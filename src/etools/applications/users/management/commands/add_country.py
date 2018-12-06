from django.core.management.base import BaseCommand, CommandError
from django_tenants.utils import get_tenant_domain_model

from etools.applications.publics.models import Currency
from etools.applications.users.models import Country


class Command(BaseCommand):
    help = 'Create a new country and related schema'

    def add_arguments(self, parser):
        parser.add_argument('country_name', type=str)

    def handle(self, *args, **options):
        try:
            name = options['country_name']
            slug = name.lower().replace(' ', '-').strip()
            usd = Currency.objects.get(code='USD')
            country = Country.objects.create(
                schema_name=name.lower().replace(' ', '_').strip(),
                name=name,
                local_currency=usd,
            )
            get_tenant_domain_model().objects.create(domain='{}.etools.unicef.org'.format(slug), tenant=country)
        except Exception as exp:
            raise CommandError(*exp.args)
