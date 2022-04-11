from django.db import models


class UserProfileManager(models.Manager):
    """ Менеджер по работе с пользовательским профилем """

    def create_profile(self, profile_data=None):
        profile = self.model()
        profile.save()
        return profile



class UserProfile(models.Model):
    """Класс информации о пользователе"""
    test_field = models.BooleanField(default=True) #тестовое поле

    objects = UserProfileManager()