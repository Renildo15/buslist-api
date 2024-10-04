from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Admin").exists():
            return True
        return False


class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Student").exists():
            return True
        return False


class IsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name="Driver").exists():
            return True
        return False


class IsAdminOrIsDriver(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user and (
            request.user.groups.filter(name="Admin").exists()
            or request.user.groups.filter(name="Driver").exists()
        ):
            return True
        return False
