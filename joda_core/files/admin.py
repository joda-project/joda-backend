from django.contrib import admin
from joda_core.files.models import File


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_at',
                    'created_by', 'changed_at', 'changed_by')
    list_filter = ['file_type', 'created_at', 'changed_at']
    search_fields = ['__str__', 'label']

admin.site.register(File, FilesAdmin)
