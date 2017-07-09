from django.db import models
from django.utils.translation import ugettext_lazy as _


class Section(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('section')
        verbose_name_plural = _('sections')

    class JSONAPIMeta:
        resource_name = 'sections'


class UserGroup(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))
    readable_sections = models.ManyToManyField(
        Section, related_name='groups_can_read', verbose_name=_('visible sections'))
    writable_sections = models.ManyToManyField(
        Section, related_name='groups_can_write', verbose_name=_('editable sections'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('user group')
        verbose_name_plural = _('user groups')

    class JSONAPIMeta:
        resource_name = 'user-groups'
