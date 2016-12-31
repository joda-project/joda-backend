from django.contrib import admin

from joda_core.models import Author, File, Tag


class CommonCoreAdmin(admin.ModelAdmin):
    ordering = ('name',)


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ['added', 'file_type']
    search_fields = ['name', 'label']


admin.site.register(Author, CommonCoreAdmin)
admin.site.register(Tag, CommonCoreAdmin)
admin.site.register(File, FilesAdmin)
