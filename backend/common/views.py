from rest_framework.permissions import SAFE_METHODS, BasePermission


class CreatedUserMixin:
    """
    Добавление поля created_by в request.data
    """

    def post(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.pk
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        request.data["created_by"] = request.user.pk
        return super().create(request, *args, **kwargs)


class StaffPermission(BasePermission):
    """
    Разрешение only staff
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff is True:
            return True
        return False
