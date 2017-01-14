from django.contrib import admin

from joda_core.models import Author, Tag
from joda_core.files.models import File


class CommonCoreAdmin(admin.ModelAdmin):
    ordering = ('name',)


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['created_at', 'file_type']
    search_fields = ['name', 'label']


admin.site.register(Author, CommonCoreAdmin)
admin.site.register(Tag, CommonCoreAdmin)
admin.site.register(File, FilesAdmin)
