from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.translation import ugettext_lazy as _

from joda_core.files.admin import FilesAdmin
from joda_core.files.models import File
from joda_core.models import Author, Tag, User
from joda_core.organization.admin import SectionAdmin, UsersAdmin, UserGroupsAdmin
from joda_core.organization.models import Section, UserGroup


class CommonCoreAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.unregister(Group)

admin.site.register(Author, CommonCoreAdmin)
admin.site.register(File, FilesAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Tag, CommonCoreAdmin)
admin.site.register(User, UsersAdmin)
admin.site.register(UserGroup, UserGroupsAdmin)

admin.site.site_header = _('Joda Administration')
admin.site.site_title = _('Joda Administration')
admin.site.index_title = _('Administration')
