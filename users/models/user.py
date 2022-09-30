from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
import django.contrib.auth.hashers as hasher


class UserManager(BaseUserManager):
    """ Менеджер для оперирования Пользователем """

    def create_user(self, username, email, password):
        """ Создает и возвращает пользователя с емэйлом, паролем и именем """
        user = self.model(username=username,
                          email=email,
                          password=hasher.make_password(password),
                          )
        user.save()
        return user

    def create_superuser(self, username, email, password):
        """ Создает и возввращет пользователя с привилегиями суперадмина """

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                )
        user.is_superuser = True
        user.save()
        return user

    @property
    def active(self):
        return CustomUser.objects.filter(is_active=True)


class CustomUser(AbstractUser, PermissionsMixin):
    """ Пользователь """
    classname = 'user'

    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(max_length=255, unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.username
