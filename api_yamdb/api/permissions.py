from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser or user.role == 'admin'


class AdminOrReadOnly(permissions.BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        user = request.user
        return (request.method in permissions.SAFE_METHODS
                or user.role == 'admin'
                or user.is_superuser)


class AuthorOrModerator(permissions.BasePermission):
    message = 'Изменение чужого контента запрещено!'

    def has_object_permission(self, request, view, obj):
        user = request.user
        return (user.role == 'moderator'
                or user.role == 'admin'
                or user.is_superuser
                or obj.author == user)
