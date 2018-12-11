from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models, connection
from django.utils.translation import ugettext_lazy as _

from django_fsm import FSMField, transition
from model_utils import Choices
from model_utils.fields import MonitorField
from model_utils.managers import InheritanceManager
from model_utils.models import TimeStampedModel
from ordered_model.models import OrderedModel

from etools.applications.field_monitoring.planning.models import Task
from etools.applications.field_monitoring.fm_settings.models import CheckListItem, FMMethodType, CPOutputConfig
from etools.applications.field_monitoring.shared.models import FMMethod
from etools.applications.publics.models import SoftDeleteMixin
from etools.applications.utils.common.models.mixins import InheritedModelMixin


class FindingMixin(models.Model):
    FINDING_CHOICES = Choices(
        ('y', _('As Planned')),
        ('n', _('Not As Planned')),
    )

    finding_value = models.CharField(max_length=1, blank=True, choices=FINDING_CHOICES, verbose_name=_('Finding'))
    finding_description = models.TextField(blank=True, verbose_name=_('Description'))
    finding_attachments = GenericRelation('attachments.Attachment', verbose_name=_('Attachments'), blank=True)

    class Meta:
        abstract = True


class VisitTaskLink(FindingMixin, models.Model):
    visit = models.ForeignKey('Visit', related_name='visit_task_links', on_delete=models.CASCADE)
    task = models.ForeignKey(Task, related_name='visit_task_links', on_delete=models.CASCADE)


class Visit(InheritedModelMixin, SoftDeleteMixin, TimeStampedModel):
    STATUS_CHOICES = Choices(
        ('draft', _('Draft')),
        ('assigned', _('Assigned')),
        ('finalized', _('Finalized')),
        ('cancelled', _('Cancelled')),
    )

    STATUSES_DATES = {
        STATUS_CHOICES.draft: 'date_created',
        STATUS_CHOICES.assigned: 'date_assigned',
        STATUS_CHOICES.finalized: 'date_finalized',
        STATUS_CHOICES.cancelled: 'date_cancelled',
    }

    # to be used by frontend to know what's the type of the visit is presented
    visit_type = 'unknown'

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    primary_field_monitor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='fm_primary_visits',
                                              verbose_name=_('Primary Field Monitor'), blank=True, null=True,
                                              on_delete=models.CASCADE)
    team_members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='fm_visits',
                                          verbose_name=_('Team Members'), blank=True)

    tasks = models.ManyToManyField(Task, related_name='visits', through=VisitTaskLink)

    start_date = models.DateField(verbose_name=_('Start Date'))
    end_date = models.DateField(verbose_name=_('End Date'))

    status = FSMField(choices=STATUS_CHOICES, default=STATUS_CHOICES.draft, verbose_name=_('Status'))

    date_assigned = MonitorField(verbose_name=_('Date Visit Assigned'), null=True, blank=True, default=None,
                                 monitor='status', when=[STATUS_CHOICES.assigned])
    date_finalized = MonitorField(verbose_name=_('Date Visit Finalized'), null=True, blank=True, default=None,
                                  monitor='status', when=[STATUS_CHOICES.finalized])
    date_cancelled = MonitorField(verbose_name=_('Date Visit Cancelled'), null=True, blank=True, default=None,
                                  monitor='status', when=[STATUS_CHOICES.cancelled])

    history = GenericRelation('unicef_snapshot.Activity', object_id_field='target_object_id',
                              content_type_field='target_content_type')

    objects = InheritanceManager()

    class Meta:
        verbose_name = _('Visit')
        verbose_name_plural = _('Visits')
        ordering = ('id',)

    @property
    def date_created(self):
        return self.created.date()

    @property
    def status_date(self):
        return getattr(self, self.STATUSES_DATES[self.status])

    def freeze_checklist(self):
        for task_link in self.visit_task_links.prefetch_related(
            'visit',
            'task__partner',
            'task__cp_output_config__planned_checklist_items__checklist_item',
            'task__cp_output_config__planned_checklist_items__methods',
            'task__cp_output_config__planned_checklist_items__partners_info',
        ):
            for planned_checklist_item in task_link.task.cp_output_config.planned_checklist_items.all():
                partner_info = [
                    info for info in planned_checklist_item.partners_info.all()
                    if info.partner is None or info.partner == task_link.task.partner
                ]
                partner_info = partner_info[0] if partner_info else None

                item = TaskCheckListItem.objects.create(
                    parent_slug=planned_checklist_item.checklist_item.slug,
                    visit_task=task_link,
                    question_number=planned_checklist_item.checklist_item.question_number,
                    question_text=planned_checklist_item.checklist_item.question_text,
                    specific_details=partner_info.specific_details if partner_info else '',
                )
                item.methods.add(*planned_checklist_item.methods.all())

    def freeze_configs(self):
        for link in self.visit_task_links.prefetch_related(
            'task__cp_output_config__cp_output',
            'task__cp_output_config__government_partners',
            'task__cp_output_config__recommended_method_types__method',
        ):
            visit_config = VisitCPOutputConfig.objects.create(
                visit_task=link,
                parent=link.task.cp_output_config,
                is_priority=link.task.cp_output_config.is_priority,
            )
            visit_config.government_partners.add(*link.task.cp_output_config.government_partners.all())

            method_types = []
            for method_type in link.task.cp_output_config.recommended_method_types.all():
                method_types.append(VisitMethodType.objects.create(
                    method=method_type.method,
                    parent_slug=method_type.slug,
                    visit=self,
                    name=method_type.name,
                    is_recommended=True
                ))
            visit_config.recommended_method_types.add(*method_types)

    @property
    def reference_number(self):
        return '{}/{}/{}/FMT'.format(
            connection.tenant.country_short_code or '',
            self.created.year,
            self.id,
        )

    @transition(
        status, source=STATUS_CHOICES.draft, target=STATUS_CHOICES.assigned,
    )
    def assign(self):
        self.freeze_checklist()
        self.freeze_configs()

    @transition(
        status, source=STATUS_CHOICES.assigned, target=STATUS_CHOICES.finalized,
    )
    def finalize(self):
        pass

    @transition(
        status, source=[STATUS_CHOICES.draft, STATUS_CHOICES.assigned], target=STATUS_CHOICES.cancelled,
    )
    def cancel(self):
        pass


class UNICEFVisit(Visit):
    visit_type = 'unicef'

    class Meta:
        verbose_name = _('UNICEF Visit')
        verbose_name_plural = _('UNICEF Visits')
        ordering = ('id',)


class TaskCheckListItem(FindingMixin, OrderedModel):
    parent_slug = models.CharField(max_length=50, verbose_name=_('Parent Slug'))
    visit_task = models.ForeignKey(VisitTaskLink, verbose_name=_('Task Link'), on_delete=models.CASCADE,
                                   related_name='checklist_items')

    question_number = models.CharField(max_length=10, verbose_name=_('Question Number'))
    question_text = models.CharField(max_length=255, verbose_name=_('Question Text'))
    specific_details = models.TextField(verbose_name=_('Specific Details To Probe'), blank=True)

    methods = models.ManyToManyField(FMMethod, verbose_name=_('Recommended Methods'))

    class Meta:
        verbose_name = _('Task Checklist Item')
        verbose_name_plural = _('Task Checklist Items')
        ordering = ('visit_task', 'order',)

    def __str__(self):
        return '{} {}'.format(self.question_number, self.question_text)

    @property
    def parent(self):
        return CheckListItem.objects.filter(slug=self.parent_slug).first()


class VisitMethodType(models.Model):
    method = models.ForeignKey(FMMethod, verbose_name=_('Method'), related_name='visit_types', on_delete=models.CASCADE)
    parent_slug = models.CharField(max_length=50, verbose_name=_('Parent Slug'))
    visit = models.ForeignKey(Visit, verbose_name=_('Visit'), related_name='method_types', on_delete=models.CASCADE)
    name = models.CharField(verbose_name=_('Name'), max_length=300)
    is_recommended = models.BooleanField(default=False, verbose_name=_('Is Recommended'))

    class Meta:
        verbose_name = _('Visit Method Type')
        verbose_name_plural = _('Visit Method Types')
        ordering = ('id',)

    @property
    def parent(self):
        return FMMethodType.objects.filter(slug=self.parent_slug).first()


class VisitCPOutputConfig(models.Model):
    visit_task = models.ForeignKey(VisitTaskLink, verbose_name=_('Visit Task'), related_name='cp_output_configs',
                                   on_delete=models.CASCADE)
    parent = models.ForeignKey(CPOutputConfig, verbose_name=_('Parent'), on_delete=models.CASCADE)
    is_priority = models.BooleanField(default=False, verbose_name=_('Priority?'))
    government_partners = models.ManyToManyField('partners.PartnerOrganization', blank=True,
                                                 verbose_name=_('Contributing Government Partners'))
    recommended_method_types = models.ManyToManyField(VisitMethodType, blank=True, verbose_name=_('Method(s)'),
                                                      related_name='cp_output_configs')

    class Meta:
        verbose_name = _('Visit CPOutput Config')
        verbose_name_plural = _('Visit CPOutput Configs')
        ordering = ('id',)

    def __str__(self):
        return '{}: {}'.format(self.visit_task, self.parent)
