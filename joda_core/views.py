from rest_framework import viewsets

from joda_core.models import Author, Tag
from joda_core.serializers import AuthorSerializer, TagSerializer


class AuthorsViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all().order_by('name')
    serializer_class = AuthorSerializer


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
