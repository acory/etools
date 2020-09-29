from django.core.exceptions import PermissionDenied
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response

from etools.applications.partners.serializers.agreements_v2 import (
    AgreementCreateUpdateSerializer,
    AgreementDetailSerializer,
    AgreementListSerializer,
)
from etools.applications.partners.serializers.exports.agreements import (
    AgreementExportFlatSerializer,
    AgreementExportSerializer,
)
from etools.applications.partners.views.agreements_v2 import AgreementDetailAPIView, AgreementListAPIView
from etools.applications.partners.views.v3 import PMPBaseViewMixin


class PMPAgreementViewMixin(PMPBaseViewMixin):
    SERIALIZER_OPTIONS = {
        "list": (AgreementListSerializer, AgreementListSerializer),
        "create": (AgreementCreateUpdateSerializer, AgreementCreateUpdateSerializer),
        "csv": (AgreementExportSerializer, AgreementExportSerializer),
        "csv_flat": (AgreementExportFlatSerializer, AgreementExportFlatSerializer),
        "update": (AgreementCreateUpdateSerializer, AgreementCreateUpdateSerializer),
        "detail": (AgreementDetailSerializer, AgreementDetailSerializer),
    }

    def get_queryset(self, format=None):
        qs = super().get_queryset()
        # if partner, limit to agreements that they are associated with
        if self.is_partner_staff():
            qs = qs.filter(partner__in=self.partners())
        return qs


class PMPAgreementListCreateAPIView(
        PMPAgreementViewMixin,
        AgreementListAPIView,
):
    filters = AgreementListAPIView.filters + [
        ('partner_id', 'partner__pk'),
    ]

    def get_serializer_class(self, format=None):
        if self.request.method == "GET":
            query_params = self.request.query_params
            if "format" in query_params.keys():
                if query_params.get("format") in ['csv', 'csv_flat']:
                    return self.get_serializer(query_params.get("format"))
        elif self.request.method == "POST":
            return self.map_serializer("create")
        return self.map_serializer("list")

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if self.is_partner_staff():
            raise PermissionDenied
        super().create(request, *args, **kwargs)
        return Response(
            self.map_serializer("detail")(
                self.instance,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
            headers=self.headers)


class PMPAgreementDetailUpdateAPIView(
        PMPAgreementViewMixin,
        AgreementDetailAPIView,
):
    def get_serializer_class(self, format=None):
        if self.request.method in ["PATCH"]:
            return self.map_serializer("update")
        return self.map_serializer("detail")

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        super().update(self, request, *args, **kwargs)
        return Response(
            self.map_serializer("detail")(
                self.instance,
                context=self.get_serializer_context(),
            ).data,
        )
