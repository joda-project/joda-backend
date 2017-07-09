"""
File model definition
"""
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djchoices import DjangoChoices, ChoiceItem

from joda_core.organization.models import Section


class File(models.Model):
    """ File model """
    class FileType(DjangoChoices):
        # pylint: disable = W0232
        """ File type definitions """
        PDF = ChoiceItem()
        JPEG = ChoiceItem()
        PNG = ChoiceItem()

    sections = models.ManyToManyField(
        Section, blank=False, verbose_name=_('sections'))
    md5 = models.CharField(max_length=32, editable=False,
                           verbose_name=_('MD5'))
    size = models.IntegerField(editable=False, verbose_name=_('size'))
    file_type = models.CharField(max_length=5,
                                 choices=FileType.choices,
                                 validators=[FileType.validator],
                                 editable=False,
                                 verbose_name=_('file type'))
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
    label = models.CharField(
        max_length=255, blank=True, verbose_name=_('label'))

    class Meta:
        verbose_name = _('file')
        verbose_name_plural = _('files')

    class JSONAPIMeta:
        """ JSON API meta information """
        resource_name = 'files'

    def __str__(self):
        """ String representation of file is a the name """
        return self.md5 + '_' + str(int(self.created_at.timestamp())) + self.get_extension(self.file_type)

    def mime_type(self):
        """ File mime type """
        if self.file_type == File.FileType.PDF:
            return 'application/pdf'
        elif self.file_type == File.FileType.PNG:
            return 'image/png'
        elif self.file_type == File.FileType.JPEG:
            return 'image/jpeg'

    @staticmethod
    def get_extension(file_type):
        """ File extension """
        if file_type == File.FileType.PDF:
            return '.pdf'
        elif file_type == File.FileType.PNG:
            return '.png'
        elif file_type == File.FileType.JPEG:
            return '.jpg'
