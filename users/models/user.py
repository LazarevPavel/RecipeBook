from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import django.contrib.auth.hashers as hasher

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



class CustomUser(AbstractUser):
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