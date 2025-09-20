from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerUser(BasePermission):
    """
    Custom permission to only allow customer users to access certain views.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user.is_authenticated and getattr(request.user, "type", None) == "customer"
        return False
    
class IsBusinessUser(BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        if request.method in ["PATCH", "DELETE"]:
            return request.user.is_authenticated and getattr(request.user, "type", None) == "business"
        return False
    
class IsStaffUser(BasePermission):
    """
    Custom permission to only allow staff users to access certain views.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff