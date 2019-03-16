from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    message = "You are already authenticated, kindly logout and try again later"

    def has_object_permission(self, request, view, obj):
        return not request.user.is_authenticated()


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user
