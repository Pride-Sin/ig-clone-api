""" Photos serializer. """

# Django REST Framework
from rest_framework import serializers
# Models
from ig_clone_api.photos.models import Photo


class PhotoModelSerializer(serializers.ModelSerializer):
    """ Photo model serializer. """

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """

        model = Photo
        fields = ('user', 'image', 'description', 'total_likes', 'total_comments')
        #! May need to delete image from read_only_fields if creating an account dont work.
        read_only_fields = ('user', 'image', 'total_likes', 'total_comments')


class UpdateDescriptionSerializer(serializers.ModelSerializer):
    """ Update description serializer. """

    description = serializers.CharField(max_length=255)

    class Meta:
        """ Meta class. """

        model = Photo
        fields = ('description',)
