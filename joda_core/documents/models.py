from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from polymorphic.models import PolymorphicModel

from joda_core.models import Tag
from joda_core.files.models import File
from joda_core.organization.models import Section


class Document(PolymorphicModel):
    title = models.CharField(max_length=255, verbose_name=_('title'))
    sections = models.ManyToManyField(
        Section, blank=False, verbose_name=_('sections'))
    files = models.ManyToManyField(File, verbose_name=_('files'))
    verified = models.BooleanField(default=False, verbose_name=_('verified'))
    public = models.BooleanField(
        default=False, verbose_name=_('publicly visible'))
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('created at'))
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+', verbose_name=_('created by'))
    changed_at = models.DateTimeField(
        auto_now=True, verbose_name=_('changed at'))
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+', verbose_name=_('changed by'))
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))
    notes = models.TextField(default='', blank=True, verbose_name=_('notes'))

    class Meta:
        verbose_name = _('document')
        verbose_name_plural = _('documents')

    class JSONAPIMeta:
        resource_name = 'documents'

    def __str__(self):
        return self.title

    def get_document_type(self):
        return ContentType.objects.get_for_id(self.polymorphic_ctype_id)
