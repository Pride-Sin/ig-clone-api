"""Main URLs module."""

# Django imports
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# Django REST Framework
from rest_framework.authtoken import views

urlpatterns = [
    # Django Admin
    path(settings.ADMIN_URL, admin.site.urls),
    # DRF get user token
    path('api-token-auth/', views.obtain_auth_token),
    # Views
    path('', include(('ig_clone_api.users.urls', 'users'), namespace='users')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
