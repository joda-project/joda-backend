from django.http import Http404
from rest_framework import filters, permissions, viewsets

from joda_core.models import Author, Content, Tag
from joda_core.pagination import DefaultPagination
from joda_core.serializers import AuthorSerializer, ContentSerializer, TagSerializer, UserSerializer


class ContentsViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all().order_by('title')
    serializer_class = ContentSerializer
    pagination_class = DefaultPagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_fields = ('tags', 'verified')
    search_fields = ('title',)


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer


class UsersViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        return [self.request.user]

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        required = self.kwargs[lookup_url_kwarg]

        if required != 'me':
            raise Http404

        return self.request.user