""" Profile model. """

# Django
from django.db import models
# Utils
from ig_clone_api.utils.models import IGAPImodel


class Profile(IGAPImodel):
    """" User Profile Model. """

    user = models.OneToOneField('users.User', on_delete=models.CASCADE)

    picture = models.ImageField(
        'profile picture',
        upload_to='users/pictures/',
        blank=True,
        null=True,
    )

    biography = models.CharField(
        'profile biography',
        blank=True,
        max_length=255,
    )

    def __str__(self):
        """Return user's str representation."""
        return str(self.user)
