""" User views. """

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
# Serializers
from ig_clone_api.users.serializers.users import (
    UserSignUpSerializer,
    UserModelSerializer,
    UserLoginSerializer,
    EmailVerificationSerializer,
    )


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """ UserViewSet
    Handle sign up, login and account verification
    """

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

