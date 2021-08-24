""" Comment serializer. """

# Django REST Framework
from rest_framework import serializers
# Models
from ig_clone_api.photos.models import Comment


class CommentModelSerializer(serializers.ModelSerializer):
    """ Comment model serializer. """

    user = serializers.CharField(default=serializers.CurrentUserDefault())

    class Meta:
        """ Meta class. """

        model = Comment
        fields = ('user', 'photo', 'comment')
        read_only_fields = ('user',)
