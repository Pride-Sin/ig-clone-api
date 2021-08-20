""" User views. """

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from ig_clone_api.users.permissions import IsAccountOwner
# Filters
import django_filters.rest_framework
# Serializers
from ig_clone_api.users.serializers.users import (
    UserSignUpSerializer,
    UserModelSerializer,
    UserLoginSerializer,
    EmailVerificationSerializer,
    )
from ig_clone_api.users.serializers.profiles import ProfileModelSerializer
# Models
from ig_clone_api.users.models import User


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    """ UserViewSet

    Handle sign up, account verification, login,
    profile and user update, retrieve and destroy.
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    lookup_field = 'username'
    # Filters
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ('username', 'email', 'first_name', 'last_name')

    def get_permissions(self):
        """Assign permissions based on action."""
        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'destroy', 'u', 'p']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """ User Sign up """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """ User login """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def verify(self, request):
        """" User email verification """
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Your account is now verified.'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def p(self, request, *args, **kwargs):
        """ Profile update. """
        user = self.get_object()
        profile = user.profile
        partial = request.method == "PATCH"
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['PUT', 'PATCH'])
    def u(self, request, *args, **kwargs):
        """ Profile update. """
        user = self.get_object()
        partial = request.method == "PATCH"
        serializer = UserModelSerializer(
            user,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """ Retrieve user information. """
        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        data = {
            'user': response.data,
        }
        response.data = data
        return response

    def list(self, request):
        """ List all the users. """
        serializer = UserModelSerializer(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        """Disable user instead of deleting."""
        instance.is_active = False
        instance.save()
