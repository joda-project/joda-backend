from django.contrib import admin, messages


class SectionAdmin(admin.ModelAdmin):
    ordering = ('name',)

    def has_delete_permission(self, request, obj=None):
        queryset = self.model.objects.all()

        # If we're running the bulk delete action, estimate the number
        # of objects after we delete the selected items
        selected = request.POST.getlist(admin.helpers.ACTION_CHECKBOX_NAME)
        if selected:
            queryset = queryset.exclude(pk__in=selected)

        if (selected or obj is not None) and queryset.count() <= 1:
            message = 'The last section can not be deleted.'
            self.message_user(request, message, messages.INFO)
            return False

        return super(SectionAdmin, self).has_delete_permission(request, obj)


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',
                    'email', 'is_superuser', 'is_staff', 'is_active', 'date_joined', 'last_login')
    list_filter = ('is_superuser', 'is_staff', 'is_active',
                   'date_joined', 'last_login')
    search_fields = ('username', 'first_name', 'last_name', 'email')


class UserGroupsAdmin(admin.ModelAdmin):
    ordering = ('name',)
    filter_horizontal = ('readable_sections', 'writable_sections')
