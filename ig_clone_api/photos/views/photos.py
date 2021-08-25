""" Photos views. """

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
# Serializer
from ig_clone_api.photos.serializers.photos import PhotoModelSerializer, UpdateDescriptionSerializer
# Models
from ig_clone_api.photos.models.photos import Photo
# Permissions
from rest_framework.permissions import IsAuthenticated
from ig_clone_api.permissions import IsObjectOwner


class PhotoViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ PhotoViewSet

    Handle create, delete, list, partial update and retrieve of photos.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoModelSerializer

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['partial_update', 'destroy']:
            permissions = [IsAuthenticated, IsObjectOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    def perfom_create(self, serializer):
        """ Upload a new photo. """
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """ Delete a photo. """
        return super().perform_destroy(instance)

    def retrieve(self, request, *args, **kwargs):
        """ Retrieve photo information. """
        response = super(PhotoViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'photo': response.data,
        }
        response.data = data
        return response

    def partial_update(self, request, pk=None):
        instance = self.get_object()
        serializer = UpdateDescriptionSerializer(
            instance,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer2 = PhotoModelSerializer(instance)
        return Response(data=serializer2.data, status=status.HTTP_200_OK)
