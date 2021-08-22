""" Photo permissions. """

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsPhotoOwner(BasePermission):
    """ Give permission only to user who uploaded the photo. """

    def has_object_permission(self, request, view, obj):
        """ Check user and obj are the same. """
        return request.user == obj.user

