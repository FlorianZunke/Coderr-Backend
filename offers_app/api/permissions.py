from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUser(BasePermission):
    """
    Custom permission to only allow business users to access certain views.
    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.
        """
        if request.method in SAFE_METHODS:
            return True
        if request.method == "POST":
            return request.user and request.user.type == 'business'
        

class IsOfferOwner(BasePermission):
    """
    Custom permission to only allow owners of an offer to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the offer.
        """
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user
