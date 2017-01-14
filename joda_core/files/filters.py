from django_filters import NumberFilter
from django_filters.rest_framework import FilterSet

from joda_core.files.models import File


class FilesFilterSet(FilterSet):
    content_count = NumberFilter(name="content__count")

    class Meta:
        model = File
        fields = ('content_count', 'file_type')
