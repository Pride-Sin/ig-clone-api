""" Photos models. """

# Django
from django.db import models
# Utils
from ig_clone_api.utils.models import IGAPImodel


class Photo(IGAPImodel):
    """ Photos model.

    This model represents the photos uploaded.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    image = models.ImageField(
        'photo',
        upload_to='photos/',
    )
    description = models.CharField(
        'photo description',
        blank=True,
        max_length=255,
    )
    total_likes = models.PositiveIntegerField(default=0)
    total_comments = models.PositiveIntegerField(default=0)


class Like(IGAPImodel):
    """ Likes model.

    This model represents each like a user gives.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)


class Comment(IGAPImodel):
    """ Comments model.

    This model represent each comment writed.
    """

    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    photo = models.ForeignKey('Photo', on_delete=models.CASCADE)
    comment = models.CharField(
        'comment',
        max_length=255,
    )
