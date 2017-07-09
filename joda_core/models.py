from urllib.parse import urlencode
from hashlib import md5

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from joda_core.organization.models import Section, UserGroup


class User(AbstractUser):
    user_groups = models.ManyToManyField(
        UserGroup, verbose_name=_('user groups'))
    remote_avatar = models.BooleanField(
        default=False, verbose_name=_('Gravatar'))

    class JSONAPIMeta:
        resource_name = 'users'

    def generate_gravatar(self):
        if not self.remote_avatar:
            return ''

        return 'https://www.gravatar.com/avatar/' + md5(self.email.lower().encode('utf-8')).hexdigest() + '?' + urlencode({'s': ''})


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('author')
        verbose_name_plural = _('authors')

    class JSONAPIMeta:
        resource_name = 'authors'


class Tag(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    class JSONAPIMeta:
        resource_name = 'tags'
