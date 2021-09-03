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

    def validate(self, attrs):
        photo_pk = self.context['view'].kwargs["photo_pk"]
        try:
            photo = Photo.objects.get(id=photo_pk)
        except Photo.DoesNotExist:
            raise serializers.ValidationError({"detail": "The photo doesn't exist"})
        attrs["photo"] = photo
        return attrs

    def create(self, validated_data):
        # Get the photo pk from the view context (DRF-nested-routers) and
        # create the new comment with the validated_data
        photo = Photo.objects.get(pk=self.context["view"].kwargs["photo_pk"])
        validated_data["photo"] = photo
        photo.total_comments += 1
        photo.save()
        return Comment.objects.create(**validated_data)
