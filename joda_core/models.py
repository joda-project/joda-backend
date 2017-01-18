from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.CharField(max_length=255, blank=True)


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
