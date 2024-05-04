
import json
from dataclasses import field

from lmcs.models import Chercheur
from .models import User
from rest_framework import serializers
from string import ascii_lowercase, ascii_uppercase
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import UntypedToken
from .utils import send_normal_email
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from rest_framework.exceptions import ValidationError




User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        # Role validation
        role = attrs.get('role')
        if role not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role specified")

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        user.assign_role(role)
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=155, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=20, read_only=True)
    id = serializers.IntegerField(read_only=True)  # Add id field
    chercheur_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token' , 'role','id', 'chercheur_id']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credentials. Please try again.")

        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])

        tokens = user.tokens()
        id = user.id
        chercheur_id = user.chercheur_id
        return {
            'email': user.email,
            'role': user.role,
            'full_name': user.get_full_name,  # Corrected usage
            "access_token": str(tokens.get('access')),
            "refresh_token": str(tokens.get('refresh')),
            'id': id,
            'chercheur_id': chercheur_id
        }


'''
class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        user.assign_role(role)
        return user
'''


class AddUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    password2 = serializers.CharField(max_length=68, min_length=6, write_only=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password2', 'role']

    def validate(self, attrs):
        password = attrs.get('password', '')
        password2 = attrs.get('password2', '')
        if password != password2:
            raise serializers.ValidationError("Passwords do not match")

        # Role validation
        role = attrs.get('role')
        if role not in dict(User.ROLE_CHOICES).keys():
            raise serializers.ValidationError("Invalid role specified")

        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        user.assign_role(role)
        return user

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
'''
class UserSerializer(serializers.HyperlinkedModelSerializer):
    bloquer_url = serializers.SerializerMethodField()
    is_active_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'role', 'is_active_display', 'bloquer_url']

    def get_bloquer_url(self, obj):
        return reverse('gestion-user', kwargs={'pk': obj.pk})

    def get_is_active_display(self, obj):
        return "Actif" if obj.is_active else "Bloqué"


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            current_site = get_current_site(request).domain
            relative_link = reverse('reset-password-confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{current_site}{relative_link}"
            print(abslink)
            email_body = f"Hi {user.first_name} Nous vous avons envoyé les codes pour réinitialiser votre mot de passe sous forme http://127.0.0.1:8000/api/v1/auth/password-reset-confirm/<code de confirmation>/<code de autorisation>/   copie code de confirmation et code de confirmation pour se identifier et confirmer la rénisialisation de mot de passe   {abslink}"
            data = {
                'email_body': email_body,
                'email_subject': "Réinitialiser votre mot de passe",
                'to_email': user.email
            }
            send_normal_email(data)

        return super().validate(attrs)


class SetNewPasswordSerializer(serializers.Serializer):
    password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    confirm_password=serializers.CharField(max_length=100, min_length=6, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            token=attrs.get('token')
            uidb64=attrs.get('uidb64')
            password=attrs.get('password')
            confirm_password=attrs.get('confirm_password')

            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Le lien de réinitialisation est invalide ou a expiré", 401)
            if password != confirm_password:
                raise AuthenticationFailed("Les mots de passe ne correspondent pas")
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            return AuthenticationFailed("Le lien est invalide ou a expiré")

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    error_messages = {
        'bad_token': 'Token is expired or invalid'
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
            return "Déconnexion réussie."  # Success message
        except TokenError:
            raise ValidationError(self.error_messages['bad_token'])


class ChercheurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chercheur
        fields = '__all__'
