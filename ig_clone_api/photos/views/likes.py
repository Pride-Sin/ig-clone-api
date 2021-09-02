""" Like views. """

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
# Serializer
from ig_clone_api.photos.serializers.likes import LikeModelSerializer
# Models
from ig_clone_api.photos.models.photos import Like, Photo
# Permissions
from rest_framework.permissions import IsAuthenticated
from ig_clone_api.permissions import IsObjectOwner


class LikeViewSet(mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """ LikeViewSet

    Handle create, delete, list of photos.
    """

    serializer_class = LikeModelSerializer

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Like.objects.all()
        # ! May not be needed
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
        """ Show all the likes of a photo. """
        queryset = Like.objects.filter(photo=photo_pk)
        if not queryset:
            return Response(data={'detail': ["The photo doesn't exist."]}, status=status.HTTP_404_NOT_FOUND)
        serializer = LikeModelSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """ Creates a new like.

        The substraction in the total_likes is made in the serializer.
        """
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """ Deletes a like and substract 1 to total_likes of the photo. """
        photo = Photo.objects.get(id=self.kwargs['photo_pk'])
        photo.total_likes -= 1
        photo.save()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
