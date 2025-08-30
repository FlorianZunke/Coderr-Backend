from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUser(BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_business