import datetime
from unittest import skip

from django.contrib.auth.models import AnonymousUser
from django.test import SimpleTestCase
from django.urls import reverse

from rest_framework import status

from etools.applications.core.tests.cases import BaseTenantTestCase
from etools.applications.core.tests.mixins import URLAssertionMixin
from etools.applications.partners.models import PartnerStaffMember
from etools.applications.partners.tests.factories import AgreementFactory, PartnerFactory, PartnerStaffFactory
from etools.applications.users.tests.factories import GroupFactory, UserFactory


class URLsTestCase(URLAssertionMixin, SimpleTestCase):
    """Simple test case to verify URL reversal"""

    def test_urls(self):
        """Verify URL pattern names generate the URLs we expect them to."""
        names_and_paths = (
            ('partner-list', '', {}),
        )
        self.assertReversal(
            names_and_paths,
            'pmp_v3:',
            '/api/pmp/v3/partners/',
        )
        self.assertIntParamRegexes(names_and_paths, 'pmp_v3:')


class BasePartnerOrganizationTestCase(BaseTenantTestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory(
            is_staff=True,
            groups__data=['UNICEF User', 'Partnership Manager'],
        )
        self.user.groups.add(GroupFactory())
        self.partner = PartnerFactory(name='Partner 1', vendor_number="VP1")
        self.agreement = AgreementFactory(
            partner=self.partner,
            signed_by_unicef_date=datetime.date.today(),
        )


class TestPartnerOrganizationList(BasePartnerOrganizationTestCase):
    def test_list_for_partner(self):
        partner = PartnerFactory()
        user = UserFactory(is_staff=False, groups__data=[])
        user_staff_member = PartnerStaffFactory(
            partner=partner,
            email=user.email,
        )
        user.profile.partner_staff_member = user_staff_member.pk
        user.profile.save()

        response = self.forced_auth_req(
            "get",
            reverse('pmp_v3:partner-list'),
            user=user,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], partner.pk)

    def test_not_authenticated(self):
        response = self.forced_auth_req(
            "get",
            reverse('pmp_v3:partner-list'),
            user=AnonymousUser(),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @skip("waiting on update to partner permissions")
    def test_not_partner_user(self):
        response = self.forced_auth_req(
            "get",
            reverse('pmp_v3:partner-list'),
            user=UserFactory(is_staff=False, groups__data=[]),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestPartnerStaffMemberList(BasePartnerOrganizationTestCase):
    def test_list_for_partner(self):
        partner = PartnerFactory()
        for __ in range(10):
            user = UserFactory(is_staff=False, groups__data=[])
            user_staff_member = PartnerStaffFactory(
                partner=partner,
                email=user.email,
            )
            user.profile.partner_staff_member = user_staff_member.pk
            user.profile.save()

        response = self.forced_auth_req(
            "get",
            reverse('pmp_v3:partner-staff-members-list', args=[partner.pk]),
            user=user,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data),
            PartnerStaffMember.objects.filter(partner=partner).count(),
        )

        # partner user not able to view another partners users
        response = self.forced_auth_req(
            "get",
            reverse('pmp_v3:partner-staff-members-list', args=[partner.pk]),
            user=self.user,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_not_authenticated(self):
        response = self.forced_auth_req(
            "get",
            reverse(
                'pmp_v3:partner-staff-members-list',
                args=[self.partner.pk],
            ),
            user=AnonymousUser(),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @skip("waiting on update to partner permissions")
    def test_not_partner_user(self):
        response = self.forced_auth_req(
            "get",
            reverse(
                'pmp_v3:partner-staff-members-list',
                args=[self.partner.pk],
            ),
            user=UserFactory(is_staff=False, groups__data=[]),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
