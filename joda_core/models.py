from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from djchoices import DjangoChoices, ChoiceItem
from polymorphic.models import PolymorphicModel


class File(models.Model):

    class FileType(DjangoChoices):
        PDF = ChoiceItem()
        JPEG = ChoiceItem()
        PNG = ChoiceItem()

    name = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32)
    file_type = models.CharField(max_length=5,
                                 choices=FileType.choices,
                                 validators=[FileType.validator])
    added = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    label = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

    def content_type(self):
        if self.file_type == File.FileType.PDF:
            return 'application/pdf'
        elif self.file_type == File.FileType.PNG:
            return 'image/png'
        elif self.file_type == File.FileType.JPEG:
            return 'image/jpeg'

    class JSONAPIMeta:
        resource_name = "files"


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name = "authors"


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name = "tags"


class Content(PolymorphicModel):
    title = models.CharField(max_length=255)
    files = models.ManyToManyField(File)
    added = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def get_content_type(self):
        return ContentType.objects.get_for_id(self.polymorphic_ctype_id)

    class JSONAPIMeta:
        resource_name = "contents"
