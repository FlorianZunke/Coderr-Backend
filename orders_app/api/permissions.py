from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """
    Custom permission to only allow customer users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_customer