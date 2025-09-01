from rest_framework.permissions import BasePermission, SAFE_METHODS


class SelfUserOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj): 
        return request.user == obj.user