from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from polymorphic.models import PolymorphicModel

from joda_core.models import Tag
from joda_core.files.models import File
from joda_core.organization.models import Section


class Document(PolymorphicModel):
    title = models.CharField(max_length=255)
    sections = models.ManyToManyField(Section, blank=False)
    files = models.ManyToManyField(File)
    verified = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+')
    changed_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+')
    tags = models.ManyToManyField(Tag, blank=True)
    notes = models.TextField(default='', blank=True)

    class JSONAPIMeta:
        resource_name = 'documents'

    def __str__(self):
        return self.title

    def get_document_type(self):
        return ContentType.objects.get_for_id(self.polymorphic_ctype_id)
