from datetime import timedelta

from django.urls import reverse
from django.utils import timezone

from rest_framework import status

import factory.fuzzy

from etools.applications.EquiTrack.tests.cases import BaseTenantTestCase
from etools.applications.field_monitoring.fm_settings.tests.factories import FMMethodFactory, FMMethodTypeFactory, \
    PlannedCheckListItemFactory
from etools.applications.field_monitoring.tests.base import FMBaseTestCaseMixin
from etools.applications.field_monitoring.visits.models import Visit
from etools.applications.field_monitoring.visits.tests.factories import UNICEFVisitFactory, VisitMethodTypeFactory


class VisitsViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_list(self):
        for status_code, status_display in Visit.STATUS_CHOICES:
            UNICEFVisitFactory(status=status_code)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_visits:visits-list'),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Visit.STATUS_CHOICES))

    def test_create(self):
        response = self.forced_auth_req(
            'post', reverse('field_monitoring_visits:visits-unicef-list'),
            user=self.unicef_user,
            data={
                'start_date': timezone.now().date(),
                'end_date': timezone.now().date() + timedelta(days=1),
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_scope_by_methods(self):
        visit = UNICEFVisitFactory(status=Visit.STATUS_CHOICES.assigned, tasks__count=1)

        method_type = FMMethodTypeFactory()
        task = visit.tasks.first()
        self.assertIsNotNone(task)

        task.cp_output_config.recommended_method_types.add(method_type)
        PlannedCheckListItemFactory(
            cp_output_config=task.cp_output_config,
            methods=[method_type.method, FMMethodFactory(is_types_applicable=False)]
        )

        visit.freeze_checklist()
        visit.freeze_configs()

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_visits:visits-unicef-detail', args=[visit.id]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        scope_by_methods = response.data['scope_by_methods']
        self.assertNotEqual(scope_by_methods, [])


class VisitMethodTypesVIewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_create(self):
        visit = UNICEFVisitFactory(status=Visit.STATUS_CHOICES.draft)

        response = self.forced_auth_req(
            'post', reverse('field_monitoring_visits:visit-method-types-list', args=[visit.id]),
            user=self.unicef_user,
            data={
                'method': FMMethodFactory(is_types_applicable=True).id,
                'name': factory.fuzzy.FuzzyText().fuzz(),
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(visit.method_types.count(), 1)
        self.assertFalse(visit.method_types.first().is_recommended)

    def test_update_recommended(self):
        method_type = VisitMethodTypeFactory(is_recommended=True)

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_visits:visit-method-types-detail',
                             args=[method_type.visit.id, method_type.id]),
            user=self.unicef_user,
            data={}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update(self):
        method_type = VisitMethodTypeFactory(is_recommended=False)

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_visits:visit-method-types-detail',
                             args=[method_type.visit.id, method_type.id]),
            user=self.unicef_user,
            data={}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
