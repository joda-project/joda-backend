
"""
File model definition
"""
from django.conf import settings
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class File(models.Model):
    """ File model """
    class FileType(DjangoChoices):
        # pylint: disable = W0232
        """ File type definitions """
        PDF = ChoiceItem()
        JPEG = ChoiceItem()
        PNG = ChoiceItem()

    md5 = models.CharField(max_length=32, editable=False)
    size = models.IntegerField(editable=False)
    file_type = models.CharField(max_length=5,
                                 choices=FileType.choices,
                                 validators=[FileType.validator],
                                 editable=False)
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+')
    changed_at = models.DateTimeField(auto_now=True)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, editable=False,
        on_delete=models.SET_NULL, related_name='+')
    label = models.CharField(max_length=255, blank=True)

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
