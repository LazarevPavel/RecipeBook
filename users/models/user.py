from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
import django.contrib.auth.hashers as hasher

import jwt
from datetime import datetime, timedelta


from rest_framework.settings import api_settings
from .user_profile import UserProfile
from .user_settings import UserSettings


class UserManager(BaseUserManager):
    """ Менеджер для оперирования Пользователем """

    def create_user(self, username, email, password, profile=None, settings=None):
        """ Создает и возвращает пользователя с емэйлом, паролем и именем """
        user = self.model(username=username,
                          email=email,
                          password=hasher.make_password(password),
                          profile=profile,
                          settings=settings)
        user.save()
        return user

    def create_superuser(self, username, email, password, profile=None, settings=None):
        """ Создает и возввращет пользователя с привилегиями суперадмина """

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                profile=profile,
                                settings=settings)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user



class CustomUser(AbstractUser, PermissionsMixin):
    """ Пользователь """

    username = models.CharField(max_length=50, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    confirmed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')
    settings = models.OneToOneField(UserSettings, on_delete=models.CASCADE, related_name='user')

    objects = UserManager()

    def __str__(self):
        return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self, days_to_expire=1):
        dt = datetime.now() + timedelta(days=days_to_expire)

        token = jwt.encode(
            {'id': self.pk, 'exp': int(dt.strftime('%S'))},
            api_settings.SECRET_KEY,
            algorithm='HS256')

        return token.decode('utf-8')