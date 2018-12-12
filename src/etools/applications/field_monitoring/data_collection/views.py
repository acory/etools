from rest_framework import mixins, viewsets

from django_filters.rest_framework import DjangoFilterBackend

from unicef_attachments.serializers import BaseAttachmentSerializer
from unicef_restlib.views import NestedViewSetMixin

from etools.applications.field_monitoring.data_collection.models import StartedMethod, TaskData, CheckListItemValue
from etools.applications.field_monitoring.data_collection.serializers import VisitDataCollectionSerializer, \
    StartedMethodSerializer, TaskDataSerializer, VisitTaskLinkDataCollectionSerializer, \
    TasksOverallCheckListSerializer, StartedMethodCheckListSerializer, CheckListValueSerializer
from etools.applications.field_monitoring.views import FMBaseViewSet, FMBaseAttachmentsViewSet
from etools.applications.field_monitoring.visits.models import Visit, VisitTaskLink, TaskCheckListItem


class VisitsDataCollectionViewSet(
    FMBaseViewSet,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = VisitDataCollectionSerializer
    queryset = Visit.objects.all()


class VisitTasksDataCollectionViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    viewsets.ModelViewSet
):
    lookup_field = 'task_id'
    serializer_class = VisitTaskLinkDataCollectionSerializer
    queryset = VisitTaskLink.objects.all()


class StartedMethodViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    viewsets.ModelViewSet
):
    serializer_class = StartedMethodSerializer
    queryset = StartedMethod.objects.all()


class TaskDataViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TaskDataSerializer
    queryset = TaskData.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('visit_task__task',)


class TasksOverallCheckListViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    viewsets.ModelViewSet
):
    serializer_class = TasksOverallCheckListSerializer
    queryset = TaskCheckListItem.objects.all()


class TasksOverallCheckListAttachmentsViewSet(FMBaseAttachmentsViewSet):
    serializer_class = BaseAttachmentSerializer
    related_model = TaskCheckListItem


class StartedMethodCheckListViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TaskCheckListItem.objects.all()
    serializer_class = StartedMethodCheckListSerializer

    def _get_parent_filters(self):
        # NestedViewSet shouldn't continue if he got value from get_parent_filter.
        # else custom filtering on nesting with level deeper than 2 will broke queryset
        # for example in this case we can override started_method filter by defining get_parent_filter,
        # but filter for next parent will broke everything: started_method__visit
        filters = {
            'visit_task__visit_id': self.kwargs['visit_pk']
        }

        started_method = self.get_parent_object()
        filters['methods'] = started_method.method

        if started_method.method_type:
            filters['visit_task__cp_output_configs__recommended_method_types'] = started_method.method_type

        return filters


class CheckListValueViewSet(
    FMBaseViewSet,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = CheckListItemValue.objects.all()
    serializer_class = CheckListValueSerializer

    def _get_parent_filters(self):
        # we are too deep with custom parents filters, so should make it by hands
        # while NestedViewSetMixin is not updated
        filters = {
            'task_data__visit_task__visit_id': self.kwargs['visit_pk'],
            'task_data__started_method': self.kwargs['started_method_pk'],
        }
        return filters


class CheckListValueAttachmentsViewSet(FMBaseAttachmentsViewSet):
    serializer_class = BaseAttachmentSerializer
    related_model = CheckListItemValue

    def _get_parent_filters(self):
        return self.get_parent_filter()
