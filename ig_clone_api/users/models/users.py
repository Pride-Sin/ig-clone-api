""" Users models. """

# Django
from django.contrib.auth.models import AbstractUser
from django.db import models
# Utils
from ig_clone_api.utils.models import IGAPImodel


class User(IGAPImodel, AbstractUser):
    ''' Custom User.

    It uses all the AbstractUser field
    (username, password, email, first_name, last_name, etc...)
    And the email_verified field.
    '''

    email_verified = models.BooleanField(
        'verified',
        default=False,
        help_text='Set to true when the user have verified its email address.'
    )
