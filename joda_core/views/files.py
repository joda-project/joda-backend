import importlib
import os

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import filters, response, status, viewsets

from joda_core import files
from joda_core.filters import FilesFilterSet
from joda_core.models import File
from joda_core.pagination import DefaultPagination
from joda_core.serializers import FileSerializer


def get_file_view(request, file_id):
    """Get file view

    Proxy uploaded files by either initiating download (default) or by
    displaying them inline (requires `inline=true` GET parameter).

    Args:
        request (HttpRequest)
        file_id (int)

    Returns:
        HttpResponse: file if everything OK
                      401 if needs authentication
                      404 if file missing
    """

    inline = 'inline' in request.GET and request.GET['inline']
    file_info = File.objects.get(id=int(file_id))

    # File with this index does not exist
    if not file_info:
        return HttpResponse(status=404)

    # If file is not public, require login
    if not request.user.is_authenticated and not file_info.public:
        return HttpResponse(status=401)

    # If file is missing, this is an error, but we should still return 404
    file_name = os.path.join(files.upload_path(), file_info.name)
    if not file_name or not os.path.exists(file_name):
        return HttpResponse(status=404)

    # Generate and return the response
    content_type = file_info.content_type()
    render_type = 'inline' if inline else 'attachment'
    file_output = file_info.name

    with open(file_name, 'rb') as f:
        r = HttpResponse(f.read(), content_type=content_type)
        r['Content-Disposition'] = render_type + ';filename=' + file_output
        return r

    return HttpResponse(status=500)


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
