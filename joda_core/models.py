from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    remote_avatar = models.BooleanField(default=False)

    class JSONAPIMeta:
        resource_name = 'users'


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
