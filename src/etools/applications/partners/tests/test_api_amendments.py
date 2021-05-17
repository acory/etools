import datetime

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone

from rest_framework import status

from etools.applications.core.tests.cases import BaseTenantTestCase
from etools.applications.partners.models import Intervention, InterventionAmendment
from etools.applications.partners.permissions import PARTNERSHIP_MANAGER_GROUP, UNICEF_USER
from etools.applications.partners.tests.factories import AgreementFactory, InterventionFactory, PartnerFactory
from etools.applications.reports.tests.factories import ReportingRequirementFactory
from etools.applications.users.tests.factories import UserFactory


class TestInterventionAmendments(BaseTenantTestCase):
    # test basic api flow

    def setUp(self):
        super().setUp()
        today = timezone.now().date()
        self.unicef_staff = UserFactory(is_staff=True, groups__data=[UNICEF_USER])
        self.pme = UserFactory(is_staff=True, groups__data=[UNICEF_USER, PARTNERSHIP_MANAGER_GROUP])

        self.partner = PartnerFactory(name='Partner')
        self.active_agreement = AgreementFactory(
            partner=self.partner,
            status='active',
            signed_by_unicef_date=datetime.date.today(),
            signed_by_partner_date=datetime.date.today()
        )

        self.active_intervention = InterventionFactory(
            agreement=self.active_agreement,
            title='Active Intervention',
            document_type=Intervention.PD,
            start=today - datetime.timedelta(days=1),
            end=today + datetime.timedelta(days=90),
            status=Intervention.ACTIVE,
            date_sent_to_partner=today - datetime.timedelta(days=1),
            signed_by_unicef_date=today - datetime.timedelta(days=1),
            signed_by_partner_date=today - datetime.timedelta(days=1),
            unicef_signatory=self.unicef_staff,
            partner_authorized_officer_signatory=self.partner.staff_members.all().first()
        )
        ReportingRequirementFactory(intervention=self.active_intervention)

    def test_start_amendment(self):
        intervention = InterventionFactory()
        response = self.forced_auth_req(
            'post',
            reverse('partners_api:intervention-amendments-add', args=[intervention.pk]),
            UserFactory(is_staff=True, groups__data=[UNICEF_USER, PARTNERSHIP_MANAGER_GROUP]),
            data={
                'types': [InterventionAmendment.TYPE_CHANGE],
                'signed_amendment': SimpleUploadedFile('hello_world.txt', 'hello world!'.encode('utf-8')),
                'signed_date': (timezone.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'kind': InterventionAmendment.KIND_NORMAL,
            },
            request_format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        response = self.forced_auth_req(
            'post',
            reverse('partners_api:intervention-amendments-add', args=[intervention.pk]),
            UserFactory(is_staff=True, groups__data=['UNICEF User', 'Partnership Manager']),
            data={
                'types': [InterventionAmendment.TYPE_CHANGE],
                'signed_amendment': SimpleUploadedFile('hello_world.txt', 'hello world!'.encode('utf-8')),
                'signed_date': (timezone.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'kind': InterventionAmendment.KIND_CONTINGENCY,
            },
            request_format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)

        response = self.forced_auth_req(
            'post',
            reverse('partners_api:intervention-amendments-add', args=[intervention.pk]),
            UserFactory(is_staff=True, groups__data=[UNICEF_USER, PARTNERSHIP_MANAGER_GROUP]),
            data={
                'types': [InterventionAmendment.TYPE_CHANGE],
                'signed_amendment': SimpleUploadedFile('hello_world.txt', 'hello world!'.encode('utf-8')),
                'signed_date': (timezone.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
                'kind': InterventionAmendment.KIND_CONTINGENCY,
            },
            request_format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, response.data)

    def test_amend_intervention(self):
        intervention = InterventionFactory(start=timezone.now().date())
        amendment = InterventionAmendment.objects.create(
            intervention=intervention,
            types=[InterventionAmendment.TYPE_ADMIN_ERROR],
            signed_date=timezone.now().date() - datetime.timedelta(days=1),
            signed_amendment=SimpleUploadedFile('hello_world.txt', 'hello world!'.encode('utf-8'))
        )

        response = self.forced_auth_req(
            'patch',
            reverse('pmp_v3:intervention-detail', args=[amendment.amended_intervention.pk]),
            UserFactory(is_staff=True, groups__data=[UNICEF_USER, PARTNERSHIP_MANAGER_GROUP]),
            data={
                'start': timezone.now().date() + datetime.timedelta(days=1),
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK, response.data)

        # todo: replace with api call
        intervention.amendments.first()._merge_amendment()

        intervention.refresh_from_db()
        self.assertEqual(intervention.start, timezone.now().date() + datetime.timedelta(days=1))
        self.assertFalse(Intervention.objects.filter(pk=amendment.amended_intervention.pk).exists())
