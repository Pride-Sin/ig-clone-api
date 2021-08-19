""" Users model admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Models
from ig_clone_api.users.models import Profile, User


class CustomUserAdmin(UserAdmin):
    """ User model admin."""

    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'email_verified', 'is_active')
    list_filter = ('is_staff', 'created', 'modified', 'email_verified', 'is_active')


admin.site.register(User, CustomUserAdmin)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """ Profile model admin."""

    list_display = ('user', 'picture', 'biography')
    search_fields = ('user__username', 'user__email')
