from django.db import models


class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name = 'sections'


class UserGroup(models.Model):
    name = models.CharField(max_length=255)
    readable_sections = models.ManyToManyField(
        Section, related_name='groups_can_read')
    writable_sections = models.ManyToManyField(
        Section, related_name='groups_can_write')

    def __str__(self):
        return self.name

    class JSONAPIMeta:
        resource_name = 'user-groups'
