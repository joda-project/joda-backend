from rest_framework import filters, permissions, viewsets
from django_filters import rest_framework as django_filters

from joda_core.pagination import DefaultPagination
from joda_core.permissions import IsPublic
from joda_core.documents.models import Document
from joda_core.documents.serializers import DocumentSerializer


class DocumentsViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPublic)
    serializer_class = DocumentSerializer
    pagination_class = DefaultPagination
    filter_backends = (django_filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_fields = ('tags', 'public', 'verified')
    search_fields = ('title', 'tags__name', 'notes')
    ordering_fields = ('title', 'created_at')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Document.objects.filter(public=True).order_by('-pk')
        return Document.objects.order_by('-pk')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, changed_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(changed_by=self.request.user)
