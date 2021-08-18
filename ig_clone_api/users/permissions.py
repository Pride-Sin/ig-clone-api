""" User permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):
    """ Give permission only to objects owners. """

    def has_object_permission(self, request, view, obj):
        """ Check user and obj are the same. """
        return request.user == obj

