# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    Section = apps.get_model('joda_core', 'Section')
    section = Section.objects.using(db_alias).create(name='Default section')

    UserGroup = apps.get_model('joda_core', 'UserGroup')
    editors = UserGroup.objects.using(db_alias).create(name='Default editors')
    editors.readable_sections.add(section)
    editors.writable_sections.add(section)

    readers = UserGroup.objects.using(db_alias).create(name='Default readers')
    readers.readable_sections.add(section)


def reverse_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias

    UserGroup = apps.get_model('joda_core', 'UserGroup')
    UserGroup.objects.using(db_alias).filter(name='Default editors').delete()
    UserGroup.objects.using(db_alias).filter(name='Default readers').delete()

    Section = apps.get_model('joda_core', 'Section')
    Section.objects.using(db_alias).filter(name='Default section').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('joda_core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func),
    ]
