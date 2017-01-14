from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet

from joda_core.files.models import File


class FilesFilterSet(FilterSet):
    document_count = NumberFilter(name="document__count")

    class Meta:
        model = File
        fields = ('document_count', 'file_type')
