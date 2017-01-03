import importlib
from django.conf import settings
from django.db.models import Count
from rest_framework import filters, response, status, viewsets

from joda_core import files
from joda_core.filters import FilesFilterSet
from joda_core.models import File
from joda_core.pagination import DefaultPagination
from joda_core.serializers import FileSerializer


class FilesViewSet(viewsets.ModelViewSet):
    queryset = File.objects.annotate(Count('content')).order_by('pk')
    serializer_class = FileSerializer
    pagination_class = DefaultPagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = FilesFilterSet

    def create_child_resource(self, resource_type, file):
        if resource_type == 'null':
            return

        if resource_type not in settings.JODA_FEATURES and 'joda_' + resource_type not in settings.JODA_FEATURES:
            return

        if not 'joda_' in resource_type:
            resource_type = 'joda_' + resource_type

        module = importlib.import_module('.helpers', resource_type)
        module.create_from_upload(file)


    def create(self, request, *args, **kwargs):
        result = []
        for f, t in zip(self.request.FILES.getlist('file[]'), self.request.data.get('file_types').split(',')):
            file_name, file_md5 = files.handle_uploaded_file(f)
            result.append({
                'name': file_name,
                'file_type': t,
                'md5': file_md5,
                'user': {
                    'type': 'User',
                    'id': self.request.user.id
                },
                'content_set': {}
            })

        serializer = self.get_serializer(data=result, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        resource_type = self.request.data.get('resource_type')

        result = serializer.save()

        for r in result:
            self.create_child_resource(resource_type, r)
