""" Photos URLs. """

# Django
from django.urls import include, path
# DRF Nested routers
from rest_framework_nested import routers
# Views
from .views import photos as photos_views
from .views import comments as comments_views

router = routers.SimpleRouter()

router.register(r'photos', photos_views.PhotoViewSet, basename='photos')

# DRF Nested routers
photos_router = routers.NestedSimpleRouter(router, r'photos', lookup='photo')
photos_router.register(r'comments', comments_views.CommentViewSet, basename='photos-comments')

urlpatterns = [
    path(r'', include(router.urls)),
    path(r'', include(photos_router.urls)),
]
