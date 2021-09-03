""" Comment views. """

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
# Serializer
from ig_clone_api.photos.serializers.comments import CommentModelSerializer
# Models
from ig_clone_api.photos.models.photos import Comment, Photo
# Permissions
from rest_framework.permissions import IsAuthenticated
from ig_clone_api.permissions import IsObjectOwner
# Exceptions
from django.core.exceptions import ObjectDoesNotExist


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """ CommentViewSet

    Handle create, delete, list and retrieve of comments.
    """

    serializer_class = CommentModelSerializer

    def get_queryset(self):
        queryset = Comment.objects.all()
        if self.action == 'destroy':
            return queryset.filter(id=self.kwargs['pk'])
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['destroy']:
            permissions = [IsAuthenticated, IsObjectOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def list(self, request, photo_pk=None):
        """ Show all the comments of a photo. """
        queryset = Comment.objects.filter(photo=photo_pk)
        serializer = CommentModelSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, photo_pk=None):
        """ Show a specific comment of a photo. """
        try:
            queryset = Comment.objects.get(pk=pk, photo=photo_pk)
        except ObjectDoesNotExist:
            data = {'detail': ["The comment doesn't exist in this photo."]}
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentModelSerializer(queryset)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer, photo_pk=None):
        """ Create a new comment. """
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """ Delete a comment. """
        photo = Photo.objects.get(id=self.kwargs['photo_pk'])
        photo.total_comments -= 1
        photo.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


