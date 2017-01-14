from rest_framework import filters, permissions, viewsets

from joda_core.pagination import DefaultPagination
from joda_core.permissions import IsPublic
from joda_core.content.models import Content
from joda_core.content.serializers import ContentSerializer


class ContentsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPublic)
    serializer_class = ContentSerializer
    pagination_class = DefaultPagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('tags', 'public', 'verified')
    search_fields = ('title', 'tags__name')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Content.objects.filter(public=True).order_by('-pk')
        return Content.objects.order_by('-pk')
