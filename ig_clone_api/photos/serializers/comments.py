""" Comment serializer. """

# Django REST Framework
from rest_framework import serializers
# Models
from ig_clone_api.photos.models import Comment
from ig_clone_api.photos.models import Photo


class CommentModelSerializer(serializers.ModelSerializer):
    """ Comment model serializer. """

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """

        model = Comment
        fields = ('user', 'photo', 'comment')
        read_only_fields = ('user',)

    def create(self, validated_data):
        # Get the photo pk from the view context (DRF-nested-routers) and
        # create the new comment with the validated_data
        photo = Photo.objects.get(pk=self.context["view"].kwargs["photo_pk"])
        validated_data["photo"] = photo
        return Comment.objects.create(**validated_data)
