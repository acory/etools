from __future__ import unicode_literals

import json
import datetime

from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status

from EquiTrack.factories import (
    PartnerFactory,
    UserFactory,
    ResultFactory,
    AgreementFactory,
    InterventionFactory,
    FundsReservationHeaderFactory
)
from EquiTrack.tests.mixins import APITenantTestCase
from reports.models import ResultType, Sector
from partners.models import (
    InterventionSectorLocationLink,
    InterventionBudget,
    InterventionAmendment,
    Intervention
)


class TestInterventionsAPI(APITenantTestCase):
    fixtures = ['initial_data.json']

    def setUp(self):
        self.unicef_staff = UserFactory(is_staff=True)
        self.partner = PartnerFactory()
        self.agreement = AgreementFactory(partner=self.partner, signed_by_unicef_date=datetime.date.today())

        self.intervention = InterventionFactory(agreement=self.agreement)
        self.intervention_2 = InterventionFactory(agreement=self.agreement, document_type=Intervention.PD)

        self.result_type = ResultType.objects.get(name=ResultType.OUTPUT)
        self.result = ResultFactory(result_type=self.result_type)

        self.pcasector = InterventionSectorLocationLink.objects.create(
            intervention=self.intervention,
            sector=Sector.objects.create(name="Sector 1")
        )
        self.partnership_budget = InterventionBudget.objects.create(
            intervention=self.intervention,
            unicef_cash=100,
            unicef_cash_local=10,
            partner_contribution=200,
            partner_contribution_local=20,
            in_kind_amount_local=10,
        )
        self.amendment = InterventionAmendment.objects.create(
            intervention=self.intervention,
            type="Change in Programme Result",
        )
        self.location = InterventionSectorLocationLink.objects.create(
            intervention=self.intervention,
            sector=Sector.objects.create(name="Sector 2")
        )
        # set up two frs not connected to any interventions
        self.fr_1 = FundsReservationHeaderFactory(intervention=None)
        self.fr_2 = FundsReservationHeaderFactory(intervention=None)

    def run_post_request(self, data):
        response = self.forced_auth_req(
            'post',
            reverse('partners_api:intervention-list'),
            user=self.unicef_staff,
            data=data
        )
        return response.status_code, json.loads(response.rendered_content)

    def run_request(self, intervention_id, data=None, method='get'):
        response = self.forced_auth_req(
            method,
            reverse('partners_api:intervention-detail', kwargs={'pk': intervention_id}),
            user=self.unicef_staff,
            data=data or {}
        )
        return response.status_code, json.loads(response.rendered_content)

    def test_api_pd_output_not_populated(self):
        data = {
            "result_links": [
                {"cp_output": self.result.id,
                 # "ram_indicators": [152],
                 "ll_results": [
                     {"id": None, "name": None, "applied_indicators": []}
                 ]}]
        }
        response = self.forced_auth_req(
            'patch',
            '/api/v2/interventions/' + str(self.intervention.id) + '/',
            user=self.unicef_staff,
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        result = json.loads(response.rendered_content)
        self.assertEqual(result.get('result_links'), {'name': ['This field may not be null.']})

    def test_add_one_valid_fr_on_create_pd(self):
        frs_data = [self.fr_1.id]
        data = {
            "document_type": Intervention.PD,
            "title": "My test intervention",
            "start": (timezone.now().date() - datetime.timedelta(days=1)).isoformat(),
            "end": (timezone.now().date() + datetime.timedelta(days=31)).isoformat(),
            "agreement": self.agreement.id,
            "frs": frs_data
        }
        status_code, response = self.run_post_request(data)

        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertItemsEqual(response['frs'], frs_data)

    def test_add_two_valid_frs_on_create_pd(self):
        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "document_type": Intervention.PD,
            "title": "My test intervention",
            "start": (timezone.now().date() - datetime.timedelta(days=1)).isoformat(),
            "end": (timezone.now().date() + datetime.timedelta(days=31)).isoformat(),
            "agreement": self.agreement.id,
            "frs": frs_data
        }
        status_code, response = self.run_post_request(data)

        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertItemsEqual(response['frs'], frs_data)

    def test_fr_details_is_accurate_on_creation(self):
        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "document_type": Intervention.PD,
            "title": "My test intervention",
            "start": (timezone.now().date() - datetime.timedelta(days=1)).isoformat(),
            "end": (timezone.now().date() + datetime.timedelta(days=31)).isoformat(),
            "agreement": self.agreement.id,
            "frs": frs_data
        }
        status_code, response = self.run_post_request(data)

        self.assertEqual(status_code, status.HTTP_201_CREATED)
        self.assertItemsEqual(response['frs'], frs_data)
        self.assertEquals(response['frs_details']['total_actual_amt'],
                          float(sum([self.fr_1.actual_amt, self.fr_2.actual_amt])))
        self.assertEquals(response['frs_details']['total_outstanding_amt'],
                          float(sum([self.fr_1.outstanding_amt, self.fr_2.outstanding_amt])))
        self.assertEquals(response['frs_details']['total_frs_amt'],
                          float(sum([self.fr_1.total_amt, self.fr_2.total_amt])))
        self.assertEquals(response['frs_details']['total_intervention_amt'],
                          float(sum([self.fr_1.intervention_amt, self.fr_2.intervention_amt])))

    def test_add_two_valid_frs_on_update_pd(self):
        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertItemsEqual(response['frs'], frs_data)
        self.assertEquals(response['frs_details']['total_actual_amt'],
                          float(sum([self.fr_1.actual_amt, self.fr_2.actual_amt])))
        self.assertEquals(response['frs_details']['total_outstanding_amt'],
                          float(sum([self.fr_1.outstanding_amt, self.fr_2.outstanding_amt])))
        self.assertEquals(response['frs_details']['total_frs_amt'],
                          float(sum([self.fr_1.total_amt, self.fr_2.total_amt])))
        self.assertEquals(response['frs_details']['total_intervention_amt'],
                          float(sum([self.fr_1.intervention_amt, self.fr_2.intervention_amt])))

    def test_remove_an_fr_from_pd(self):
        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertItemsEqual(response['frs'], frs_data)

        # Remove fr_1
        frs_data = [self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')

        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertItemsEqual(response['frs'], frs_data)

    def test_fail_add_expired_fr_on_pd(self):
        self.fr_1.end_date = timezone.now().date() - datetime.timedelta(days=1)
        self.fr_1.save()

        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['frs'], ['One or more selected FRs is expired, {}'.format(self.fr_1.fr_number)])

    def test_fail_add_used_fr_on_pd(self):
        self.fr_1.intervention = self.intervention
        self.fr_1.save()

        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')

        self.assertEqual(status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response['frs'],
                         ['One or more of the FRs selected is related '
                          'to a different PD/SSFA, {}'.format(self.fr_1.fr_number)])

    def test_add_same_frs_twice_on_pd(self):
        frs_data = [self.fr_1.id, self.fr_2.id]
        data = {
            "frs": frs_data
        }
        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertItemsEqual(response['frs'], frs_data)

        status_code, response = self.run_request(self.intervention_2.id, data, method='patch')
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertItemsEqual(response['frs'], frs_data)