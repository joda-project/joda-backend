
"""
File model definition
"""
from django.contrib.auth.models import User
from django.db import models
from djchoices import DjangoChoices, ChoiceItem


class File(models.Model):
    """ File model """
    class FileType(DjangoChoices):
        # pylint: disable = R0903, W0232
        """ File type definitions """
        PDF = ChoiceItem()
        JPEG = ChoiceItem()
        PNG = ChoiceItem()

    name = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32)
    size = models.IntegerField()
    file_type = models.CharField(max_length=5,
                                 choices=FileType.choices,
                                 validators=[FileType.validator])
    public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    label = models.CharField(max_length=255, blank=True)

    def __str__(self):
        """ String representation of file is a the name """
        return self.name

    def mime_type(self):
        """ File mime type """
        if self.file_type == File.FileType.PDF:
            return 'application/pdf'
        elif self.file_type == File.FileType.PNG:
            return 'image/png'
        elif self.file_type == File.FileType.JPEG:
            return 'image/jpeg'
