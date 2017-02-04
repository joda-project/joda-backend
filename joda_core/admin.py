from django.contrib import admin
from django.contrib.auth.models import Group

from joda_core.models import Author, Tag, User
from joda_core.files.models import File
from joda_core.organization.admin import SectionAdmin, UsersAdmin, UserGroupsAdmin
from joda_core.organization.models import Section, UserGroup


class CommonCoreAdmin(admin.ModelAdmin):
    ordering = ('name',)


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    list_filter = ['created_at', 'file_type']
    search_fields = ['__str__', 'label']


admin.site.unregister(Group)

admin.site.register(Author, CommonCoreAdmin)
admin.site.register(File, FilesAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Tag, CommonCoreAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(UserGroup, UserGroupsAdmin)
