''' Django models utilities. '''

# Django
from django.db import models


class IGAPImodel(models.Model):
    ''' Base model for other classes.

    Adds 2 attributes to the tables which inherits it:
        - created (Datetime): Saves datetime of creation
        - modified (Datetime): Saves datetime of the last time it was modified
    '''

    created = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        help_text='Date time on which the object was created.'
        )

    modified = models.DateTimeField(
        'Last modified at',
        auto_now_add=True,
        help_text='Date time of the last time the object was modified.'
    )

    class Meta:
        """Meta option."""

        abstract = True

        get_latest_by = 'created'
        ordering = ['-created', '-modified']
