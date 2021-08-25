""" Like serializer. """

# Django REST Framework
from rest_framework import serializers
# Models
from ig_clone_api.photos.models import Photo
from ig_clone_api.photos.models import Like


class LikeModelSerializer(serializers.ModelSerializer):
    """ Comment model serializer. """

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """

        model = Like
        fields = ('user', 'photo')
        read_only_fields = ('user', 'photo')

    def create(self, validated_data):
        # Get the photo pk from the view context (DRF-nested-routers) and
        # create the new like with the validated_data
        photo_pk = self.context['view'].kwargs["photo_pk"]
        photo = Photo.objects.get(pk=photo_pk)
        validated_data["photo"] = photo
        return Like.objects.get_or_create(**validated_data)
