from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_bulk import BulkCreateModelMixin
from unicef_attachments.models import Attachment, AttachmentLink
from unicef_restlib.pagination import DynamicPageNumberPagination
from unicef_restlib.views import MultiSerializerViewSetMixin, NestedViewSetMixin, SafeTenantViewSetMixin

from etools.applications.permissions2.metadata import BaseMetadata


class FMBaseViewSet(
    SafeTenantViewSetMixin,
    MultiSerializerViewSetMixin,
):
    metadata_class = BaseMetadata
    pagination_class = DynamicPageNumberPagination
    permission_classes = [IsAuthenticated, ]


class AttachmentFileTypesViewMixin:
    @action(detail=False, methods=['GET'], url_path='file-types', url_name='file-types')
    def file_types(self, request, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        declared_fields = serializer_class._declared_fields
        if 'file_type' not in declared_fields:
            raise Http404

        return Response(data=declared_fields['file_type'].choices)


class FMBaseAttachmentLinksViewSet(
    FMBaseViewSet,
    AttachmentFileTypesViewMixin,
    NestedViewSetMixin,
    BulkCreateModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    attachment_code = None  # fill `code` field in attachment to deal with coded generics
    related_model = None
    queryset = AttachmentLink.objects.prefetch_related('attachment')
    lookup_field = 'attachment_id'
    lookup_url_kwarg = 'pk'

    def get_parent_filter(self):
        parent = self.get_parent_object()
        if not parent:
            return {}

        content_type = ContentType.objects.get_for_model(self.related_model)

        # filter both for link and for attachment to be sure we'll use consistent object.
        filter_kwargs = {
            'content_type_id': content_type.id,
            'object_id': parent.pk,
            'attachment__content_type_id': content_type.id,
            'attachment__object_id': parent.pk,
        }
        if self.attachment_code:
            filter_kwargs['attachment__code'] = self.attachment_code
        return filter_kwargs

    def _get_parent_filters(self):
        # too deep inheritance is not supported in case of generic relations, so just use parent (content object)
        return self.get_parent_filter()

    def perform_create(self, serializer):
        parent = self.get_parent_object()
        serializer.save(content_object=parent)

        if isinstance(serializer, ListSerializer):
            links = serializer.instance
        else:
            links = [serializer.instance]

        for link in links:
            attachment = link.attachment
            attachment.content_object = parent
            if self.attachment_code:
                attachment.code = self.attachment_code
            attachment.save()

    def perform_destroy(self, instance):
        super().perform_destroy(instance)

        # also, unlink attachment from the target
        instance.attachment.content_object = None
        instance.attachment.save()
