"""  Photos model admin."""

# Django
from django.contrib import admin

# Models
from ig_clone_api.photos.models import Photo, Comment, Like


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo model admin."""

    list_display = ('user', 'image', 'description', 'total_likes', 'total_likes')
    search_fields = ('user',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    """ Like model admin."""

    list_display = ('user', 'photo')
    search_fields = ('user', 'photo')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Comment model admin."""

    list_display = ('user', 'photo', 'comment')
    search_fields = ('user', 'photo', 'comment')