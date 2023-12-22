from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.is_admin
                or request.user.is_moderator
                or request.user == obj.author
            )
        )


class IsAdminOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.is_admin
            )
        )


class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
