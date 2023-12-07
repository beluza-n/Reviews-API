from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
                user.is_superuser or user.is_admin)


class AdminOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or (user.is_authenticated and user.is_admin))


class AuthorModeratorOrReadOnly(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.role.is_moderator
                or user.is_admin
                or obj.author == user)
