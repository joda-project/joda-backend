from django_filters import BaseInFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from joda_core.models import File

class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class FilesFilterSet(FilterSet):
    content_count = NumberFilter(name="content__count")

    class Meta:
        model = File
        fields = ['content_count']
