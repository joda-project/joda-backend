from django.contrib import admin


class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'created_by', 'changed_at', 'changed_by')
    list_filter = ['created_at', 'changed_at']
    search_fields = ['title', 'notes', 'tags']
    filter_horizontal = ['tags']
