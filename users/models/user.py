from django.contrib.auth.models import AbstractUser
from django.db import models

from user_profile import UserProfile
from user_settings import UserSettings




class CustomUser(AbstractUser):
    """Класс пользователя"""
    email = models.EmailField(max_length=255, unique=True, null=False)
    confirmed = models.BooleanField(default=False)
    profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='user')
    settings = models.OneToOneField(UserSettings, on_delete=models.CASCADE, related_name='user')