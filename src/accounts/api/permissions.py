from rest_framework import permissions


class AnonPermissionOnly(permissions.BasePermission):
    message = "You are already authenticated, kindly logout and try again later"

    def has_permission(self, request, view):
        return not request.user.is_authenticated()


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view, obj):
        return obj.owner == request.user
