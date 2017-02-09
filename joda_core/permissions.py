from rest_framework import permissions


class IsPublic(permissions.BasePermission):
    """Common permission which checks that document is public"""

    def has_object_permission(self, request, view, obj):
        if not obj.public:
            return request.user.is_authenticated
        return True


class UserPermission(permissions.BasePermission):
    """Users permissions"""

    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE']:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            return obj == request.user
        return True
