"""Users serializers."""

# Django
from django.conf import settings
from django.contrib.auth import authenticate, password_validation
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
# Django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
# Models
from ig_clone_api.users.models import User, Profile
# Serializers
from ig_clone_api.users.serializers.profiles import ProfileModelSerializer
# Utilities
import jwt
from datetime import timedelta


class UserModelSerializer(serializers.ModelSerializer):

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """ Meta class. """

        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'profile')


class UserSignUpSerializer(serializers.Serializer):
    """ Serializer for User sign up.

    Handle sign up data validation and user/profile creation.
    """

    username = serializers.CharField(
        min_length=3,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    # Name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    def validate(self, data):
        """Verify passwords match."""
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match.")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""
        data.pop('password_confirmation')
        user = User.objects.create_user(**data)
        Profile.objects.create(user=user)
        self.send_confirmation_email(user)
        return user

    def send_confirmation_email(self, user):
        """Send email verification link to given user."""
        verification_token = self.gen_verification_token(user)
        subject = f'Hello {user.username}! Please verify your account.'
        from_email = 'Instagram Clone <noreply@domain.com>'
        content = render_to_string(
            'emails/email_verification.html',
            {'token': verification_token, 'user': user}
        )
        msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
        msg.attach_alternative(content, "text/html")
        msg.send()

    def gen_verification_token(self, user):
        """Create JWT token that the user can use to verify its email."""
        exp_date = timezone.now() + timedelta(days=3)
        payload = {
            'user': user.username,
            'exp': int(exp_date.timestamp()),
            'type': 'email_confirmation'
        }
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        return token


class EmailVerificationSerializer(serializers.Serializer):
    """ Serializer for email validation.

    Handle the email validation.
    """

    token = serializers.CharField()

    def validate_token(self, data):
        """ Validate the verification token. """
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('token expired')
        except jwt.PyJWTError:
            raise serializers.ValidationError('token is invalid')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('token is invalid')

        self.context['payload'] = payload

        return data

    def save(self):
        """ Update user email_verified. """
        payload = self.context['payload']
        user = User.objects.get(username=payload['user'])
        user.email_verified = True
        user.save()


class UserLoginSerializer(serializers.Serializer):
    """ Serializer for User login.

    Handle the login request.
    """

    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)

    def validate(self, data):
        """ Validate login credentials. """
        user = authenticate(username=data['username'], password=data['password'])

        if not user:
            raise serializers.ValidationError('Incorrect credentials.')
        if not user.email_verified:
            raise serializers.ValidationError('Please verify your email before login.')
        self.context['user'] = user
        return data

    def create(self, data):
        """ Generate/retrieve token. """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
