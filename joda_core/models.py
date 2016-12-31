from django.contrib.auth.models import User
from django.db import models
from djchoices import DjangoChoices, ChoiceItem
from polymorphic.models import PolymorphicModel


class File(models.Model):

    class FileType(DjangoChoices):
        PDF = ChoiceItem()
        JPEG = ChoiceItem()

    name = models.CharField(max_length=255)
    md5 = models.CharField(max_length=32, blank=True)
    file_type = models.CharField(max_length=5,
                                 choices=FileType.choices,
                                 validators=[FileType.validator])
    added = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    label = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Content(PolymorphicModel):
    title = models.CharField(max_length=255)
    files = models.ManyToManyField(File)
    added = models.DateTimeField(auto_now_add=True)
    validated = models.BooleanField(default=False)
    listed = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    user = models.ForeignKey(
        User, null=True, on_delete=models.SET_NULL, related_name='+')
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title
