from django.urls import reverse
from rest_framework import status

from etools.applications.EquiTrack.tests.cases import BaseTenantTestCase
from etools.applications.field_monitoring.data_collection.tests.base import AssignedVisitMixin
from etools.applications.field_monitoring.data_collection.tests.factories import StartedMethodFactory, TaskDataFactory
from etools.applications.field_monitoring.tests.base import FMBaseTestCaseMixin
from etools.applications.field_monitoring.visits.models import Visit
from etools.applications.field_monitoring.visits.tests.factories import UNICEFVisitFactory


class VisitDataCollectionViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def test_details(self):
        visit = UNICEFVisitFactory(status=Visit.STATUS_CHOICES.assigned)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_data_collection:visits-detail', args=[visit.id]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class StartedMethodsViewTestCase(FMBaseTestCaseMixin, AssignedVisitMixin, BaseTenantTestCase):
    def test_list(self):
        StartedMethodFactory(
            visit=self.assigned_visit,
            method=self.assigned_visit_method_type.method,
            method_type=self.assigned_visit_method_type,
        )

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_data_collection:started-methods-list', args=[self.assigned_visit.id]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def start_new_method(self):
        response = self.forced_auth_req(
            'post', reverse('field_monitoring_data_collection:started-methods-list', args=[self.assigned_visit.id]),
            user=self.unicef_user,
            data={
                'method': self.assigned_visit_method_type.method.id,
                'method_type': self.assigned_visit_method_type.id,
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author']['id'], self.unicef_user.id)


class TaskDataViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.visit = UNICEFVisitFactory(status=Visit.STATUS_CHOICES.assigned)
        cls.started_method = StartedMethodFactory(visit=cls.visit)
        cls.task_data = TaskDataFactory(visit_task__visit=cls.visit, started_method=cls.started_method)

    def test_list(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_data_collection:task-data-list',
                           args=[self.visit.id, self.started_method.id]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
