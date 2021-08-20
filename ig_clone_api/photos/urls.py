""" Photos URLs. """

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import photos as photos_views

router = DefaultRouter()
router.register(r'photos', photos_views.PhotoViewSet, basename='photos')

urlpatterns = [
    path('', include(router.urls))
]
