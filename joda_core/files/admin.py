from django.contrib import admin


class FilesAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'created_at',
                    'created_by', 'changed_at', 'changed_by')
    list_filter = ['file_type', 'created_at', 'changed_at']
    search_fields = ['__str__', 'label']
