from rest_framework import permissions

class IsReviewOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a review to edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.reviewer == request.user


class IsCustomerUser(permissions.BasePermission):
    """
    Only allow users with type 'customer' to create reviews.
    """
    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated and getattr(request.user, "type", None) == "customer"
        return True