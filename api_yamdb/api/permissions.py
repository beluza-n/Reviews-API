from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        user = request.user
        return (user.is_authenticated
                and (user.is_superuser or user.is_admin))


class ReviewCommentPermissions(BasePermission):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            obj.author == request.user
            or request.user.is_admin
            or request.user.is_moderator
        )


class IsAdminUserOrReadOnly(IsAdmin):
    message = 'Недостаточно прав для этого действия!'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return super().has_permission(request, view)
