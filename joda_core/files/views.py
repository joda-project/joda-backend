import importlib
import os

from django.conf import settings
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import filters, permissions, response, status, viewsets

from joda_core.pagination import DefaultPagination
from joda_core.permissions import IsPublic
from joda_core.files import utils
from joda_core.files.filters import FilesFilterSet
from joda_core.files.models import File
from joda_core.files.serializers import FileSerializer


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
    file_name = os.path.join(utils.upload_path(), file_info.__str__())
    if not file_name or not os.path.exists(file_name):
        return HttpResponse(status=404)

    # Generate and return the response
    mime_type = file_info.mime_type()
    render_type = 'inline' if inline else 'attachment'
    file_output = file_info.__str__()

    with open(file_name, 'rb') as f:
        r = HttpResponse(f.read(), document_type=mime_type)
        r['Content-Disposition'] = render_type + ';filename=' + file_output
        return r

    return HttpResponse(status=500)


class FilesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPublic)
    serializer_class = FileSerializer
    pagination_class = DefaultPagination
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter)
    filter_class = FilesFilterSet
    search_fields = ('name', 'label')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return File.objects.filter(public=True).annotate(Count('document')).order_by('-pk')
        return File.objects.annotate(Count('document')).order_by('-pk')

    def create_child(self, document_type, file):
        if document_type == 'null':
            return

        if document_type not in settings.JODA_FEATURES and \
            'joda_' + document_type not in settings.JODA_FEATURES:
            return

        if not 'joda_' in document_type:
            document_type = 'joda_' + document_type

        module = importlib.import_module('.helpers', document_type)
        module.create_from_upload(file, self.request.user)

    def create(self, request, *args, **kwargs):
        document_type = self.request.data.get('document_type')
        result = []
        for f, t in zip(self.request.FILES.getlist('file[]'), self.request.data.get('file_types').split(',')):
            file_md5, file_size = utils.handle_uploaded_file(f, t)
            new_file = File(file_type=t, md5=file_md5, size=file_size, created_by=self.request.user)
            new_file.save()
            result.append(new_file)
            self.create_child(document_type, new_file)

        serializer = self.get_serializer(result, many=True)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(changed_by=self.request.user)
