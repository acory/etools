from __future__ import unicode_literals

from rest_framework.filters import BaseFilterBackend

from t2f.serializers.filters.action_points import SearchFilterSerializer, SortFilterSerializer,\
    FilterBoxFilterSerializer


class SearchFilter(BaseFilterBackend):
    _search_fields = ('action_point_number', 'trip_reference_number', 'description')

    def filter_queryset(self, request, queryset, view):
        serializer = SearchFilterSerializer(data=request.GET)
        if not serializer.is_valid():
            return queryset
        data = serializer.validated_data

        search_str = data['search']
        if search_str:
            q = Q()
            for field_name in self._search_fields:
                constructed_field_name = '{}__iexact'.format(field_name)
                q |= Q(**{constructed_field_name: search_str})
            queryset = queryset.filter(q)

        return queryset


class SortFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        serializer = SortFilterSerializer(data=request.GET)
        if not serializer.is_valid():
            return queryset
        data = serializer.validated_data

        prefix = '-' if data['reverse'] else ''
        sort_by = '{}{}'.format(prefix, data['sort_by'])
        return queryset.order_by(sort_by)


class FilterBoxFilter(BaseFilterBackend):
    """
    Does the filtering based on the filter parameters coming from the frontend
    """
    def filter_queryset(self, request, queryset, view):
        serializer = FilterBoxFilterSerializer(data=request.GET)
        if not serializer.is_valid():
            return queryset
        data = serializer.validated_data

        return queryset.filter(**data)
