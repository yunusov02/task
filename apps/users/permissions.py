from rest_framework.permissions import BasePermission

from .models import UserRole


class ManagerRequiredPermission(BasePermission):
    message = "You must be a manager to access this endpoint."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == UserRole.MANAGER
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
