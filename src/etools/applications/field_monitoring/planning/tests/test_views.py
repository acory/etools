from datetime import date

from django.urls import reverse

from rest_framework import status

from etools.applications.EquiTrack.tests.cases import BaseTenantTestCase
from etools.applications.field_monitoring.planning.models import YearPlan
from etools.applications.field_monitoring.planning.tests.factories import YearPlanFactory, TaskFactory
from etools.applications.field_monitoring.tests.base import FMBaseTestCaseMixin


class YearPlanViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    def _test_year(self, year, expected_status):
        self.assertEqual(YearPlan.objects.count(), 0)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_planning:year-plan-detail', args=[year]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, expected_status)

    def test_current_year(self):
        self._test_year(date.today().year, status.HTTP_200_OK)

    def test_next_year(self):
        self._test_year(date.today().year + 1, status.HTTP_200_OK)

    def test_year_after_next(self):
        self._test_year(date.today().year + 2, status.HTTP_404_NOT_FOUND)

    def test_previous_year(self):
        self._test_year(date.today().year - 1, status.HTTP_404_NOT_FOUND)

    def test_plan_by_month(self):
        TaskFactory(plan_by_month=[1]*12)
        TaskFactory(plan_by_month=[2]*12)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_planning:year-plan-detail', args=[date.today().year]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['tasks_by_month'], [3]*12)

    def test_totals(self):
        task_1 = TaskFactory()
        TaskFactory()
        TaskFactory(cp_output_config=task_1.cp_output_config)
        TaskFactory(cp_output_config=task_1.cp_output_config, location_site=task_1.location_site)

        response = self.forced_auth_req(
            'get', reverse('field_monitoring_planning:year-plan-detail', args=[date.today().year]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_planned'], {'tasks': 4, 'cp_outputs': 2, 'sites': 3})


class YearPlanTasksViewTestCase(FMBaseTestCaseMixin, BaseTenantTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.year_plan = YearPlanFactory()
        cls.task = TaskFactory()

    def test_list(self):
        response = self.forced_auth_req(
            'get', reverse('field_monitoring_planning:year-plan-tasks-list', args=[self.year_plan.pk]),
            user=self.unicef_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create(self):
        response = self.forced_auth_req(
            'post', reverse('field_monitoring_planning:year-plan-tasks-list', args=[self.year_plan.pk]),
            user=self.unicef_user,
            data={
                'cp_output_config': self.task.cp_output_config.id,
                'partner': self.task.partner.id,
                'intervention': self.task.intervention.id,
                'location': self.task.location.id,
                'location_site': self.task.location_site.id,
                'plan_by_month': [1] + [0]*11
            }
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['plan_by_month'], [1] + [0]*11)

    def test_update_plan(self):
        task = TaskFactory()

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_planning:year-plan-tasks-detail', args=[self.year_plan.pk, task.id]),
            user=self.unicef_user,
            data={
                'plan_by_month': [1] + [0] * 10 + [1]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['plan_by_month'], [1] + [0]*10 + [1])

    def test_update_plan_incorrect(self):
        task = TaskFactory()

        response = self.forced_auth_req(
            'patch', reverse('field_monitoring_planning:year-plan-tasks-detail', args=[self.year_plan.pk, task.id]),
            user=self.unicef_user,
            data={
                'plan_by_month': [0] * 11 + [-1]
            }
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('plan_by_month', response.data)
