from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "admin")


class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "user")


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # GET allowed for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write methods only for admin
        return bool(request.user and request.user.role == "admin")


class IsSelfOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # obj is a user instance
        return obj == request.user or request.user.role == "admin"
