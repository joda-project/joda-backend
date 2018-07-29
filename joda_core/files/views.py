import base64
import os

from django.apps import apps
from django.db.models import Count
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, permissions, response, status, viewsets
from django_filters import rest_framework as django_filters

from joda.helpers import features
from joda_core.pagination import DefaultPagination
from joda_core.permissions import IsPublic
from joda_core.files import utils
from joda_core.files.filters import FilesFilterSet
from joda_core.files.models import File
from joda_core.files.serializers import FileSerializer
from joda_core.organization.models import Section


@csrf_exempt
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

    inline = 'inline' in request.POST and request.POST['inline']
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
    file_output = file_info.__str__()

    with open(file_name, 'rb') as f:
        if inline:
            encoded_file = base64.b64encode(f.read())
            r = HttpResponse(encoded_file)
            return r
        else:
            r = HttpResponse(f.read(), content_type=mime_type)
            r['Content-Disposition'] = 'attachment' + ';filename=' + file_output
            return r

    return HttpResponse(status=500)


class FilesViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsPublic)
    serializer_class = FileSerializer
    pagination_class = DefaultPagination
    filter_backends = (django_filters.DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter)
    filter_class = FilesFilterSet
    search_fields = ('md5', 'label')
    ordering_fields = ('created_at')

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return File.objects.filter(public=True).annotate(Count('document')).order_by('-pk')
        return File.objects.annotate(Count('document')).order_by('-pk')

    def create_child(self, document_type, file):
        if document_type == 'null':
            return

        features_dict = features()
        if document_type not in features_dict:
            return

        feature = features_dict[document_type]

        DocumentModel = apps.get_model(
            app_label=feature['module'], model_name=feature['model_name'])
        document = DocumentModel(
            title=feature['new_item_str'], created_by=self.request.user)
        document.save()
        document.sections.add(file.sections.first())
        document.files.add(file)
        document.save()
        return document

    def create(self, request, *args, **kwargs):
        document_type = self.request.data.get('document_type')
        section = Section.objects.order_by('pk').first()
        result = []
        for f, t in zip(self.request.FILES.getlist('file[]'),
                        self.request.data.get('file_types').split(',')):
            file_md5, file_size = utils.handle_uploaded_file(f, t)
            new_file = File(file_type=t, md5=file_md5,
                            size=file_size, created_by=self.request.user)
            new_file.save()
            new_file.sections.add(section)
            result.append(new_file)
            self.create_child(document_type, new_file)

        serializer = self.get_serializer(result, many=True)
        headers = self.get_success_headers(serializer.data)
        return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_update(self, serializer):
        serializer.save(changed_by=self.request.user)
