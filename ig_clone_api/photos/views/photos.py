""" Photos views. """

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response
# Serializer
from ig_clone_api.photos.serializers.photos import PhotoModelSerializer, UpdateDescriptionSerializer
# Models
from ig_clone_api.photos.models.photos import Photo


class PhotoViewSet(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """ PhotoViewSet

    Handle upload (create) and delete of photos.
    """

    queryset = Photo.objects.all()
    serializer_class = PhotoModelSerializer

    def perfom_create(self, serializer):
        """ Upload a new photo. """
        serializer.save()

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
        return Response(data=serializer2.data, status=status.HTTP_202_ACCEPTED)
