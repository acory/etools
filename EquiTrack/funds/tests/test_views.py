from __future__ import unicode_literals

import json
from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status

from EquiTrack.tests.mixins import APITenantTestCase
from EquiTrack.factories import FundsReservationHeaderFactory, UserFactory, InterventionFactory


class TestFRHeaderView(APITenantTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.unicef_staff = UserFactory(is_staff=True)
        self.intervention = InterventionFactory()
        self.fr_1 = FundsReservationHeaderFactory(intervention=None)
        self.fr_2 = FundsReservationHeaderFactory(intervention=None)

    def run_request(self, data):
        response = self.forced_auth_req(
            'get',
            reverse('funds:frs'),
            user=self.unicef_staff,
            data=data
        )
        return response.status_code, json.loads(response.rendered_content)

    def test_get_one_fr(self):

        data = {'values': self.fr_1.fr_number}

        status_code, result = self.run_request(data)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(result['frs']), 1)
        self.assertEquals(result['total_actual_amt'], float(self.fr_1.actual_amt))
        self.assertEquals(result['total_outstanding_amt'], float(self.fr_1.outstanding_amt))
        self.assertEquals(result['total_frs_amt'], float(self.fr_1.total_amt))
        self.assertEquals(result['total_intervention_amt'], float(self.fr_1.intervention_amt))

    def test_get_two_frs(self):

        data = {'values': ','.join([self.fr_1.fr_number, self.fr_2.fr_number])}

        status_code, result = self.run_request(data)

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(result['frs']), 2)

        # Make sure result numbers match up
        # float the Decimal sum
        self.assertEquals(result['total_actual_amt'],
                          float(sum([self.fr_1.actual_amt, self.fr_2.actual_amt])))
        self.assertEquals(result['total_outstanding_amt'],
                          float(sum([self.fr_1.outstanding_amt, self.fr_2.outstanding_amt])))
        self.assertEquals(result['total_frs_amt'],
                          float(sum([self.fr_1.total_amt, self.fr_2.total_amt])))
        self.assertEquals(result['total_intervention_amt'],
                          float(sum([self.fr_1.intervention_amt, self.fr_2.intervention_amt])))

    def test_get_fail_with_no_values(self):
        data = {}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['error'], 'Values are required')

    def test_get_fail_with_nonexistant_values(self):
        data = {'values': ','.join(['im a bad value', 'another bad value'])}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['error'],
                         'One or more of the FRs selected is either expired, has been used by another '
                         'intervention or could not be found in eTools')

    def test_get_fail_with_one_bad_value(self):
        data = {'values': ','.join(['im a bad value', self.fr_1.fr_number])}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['error'],
                         'One or more of the FRs selected is either expired, has been used by another '
                         'intervention or could not be found in eTools')

    def test_get_fail_with_expired_fr(self):
        self.fr_1.end_date = timezone.now().date() - timedelta(days=1)
        self.fr_1.save()
        data = {'values': ','.join([self.fr_2.fr_number, self.fr_1.fr_number])}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['error'],
                         'One or more of the FRs selected is either expired, has been used by another '
                         'intervention or could not be found in eTools')

    def test_get_fail_with_intervention_fr(self):
        self.fr_1.intervention = self.intervention
        self.fr_1.save()
        data = {'values': ','.join([self.fr_2.fr_number, self.fr_1.fr_number])}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(result['error'],
                         'One or more of the FRs selected is either expired, has been used by another '
                         'intervention or could not be found in eTools')

    def test_get_with_intervention_fr(self):
        self.fr_1.intervention = self.intervention
        self.fr_1.save()
        data = {'values': ','.join([self.fr_2.fr_number, self.fr_1.fr_number]),
                'intervention': self.intervention.id}
        status_code, result = self.run_request(data)
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(len(result['frs']), 2)
        self.assertEquals(result['total_actual_amt'], float(sum([self.fr_1.actual_amt, self.fr_2.actual_amt])))
        self.assertEquals(result['total_outstanding_amt'],
                          float(sum([self.fr_1.outstanding_amt, self.fr_2.outstanding_amt])))
        self.assertEquals(result['total_frs_amt'],
                          float(sum([self.fr_1.total_amt, self.fr_2.total_amt])))
        self.assertEquals(result['total_intervention_amt'],
                          float(sum([self.fr_1.intervention_amt, self.fr_2.intervention_amt])))
