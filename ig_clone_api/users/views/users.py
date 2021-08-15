""" User views. """

# Django REST Framework
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
# Serializers
from ig_clone_api.users.serializers.users import UserSignUpSerializer, UserModelSerializer


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """ UserViewSet
    Handle SignUp
    """

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """ User SignUp """
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)
