""" Users models. """

# Django
from django.contrib.auth.models import AbstractUser

# Utils
from ig_clone_api.utils.models import IGAPImodel


class User(IGAPImodel, AbstractUser):
    ''' Custom User.

    Right now only the fields of AbstractUser class are used.
    '''
