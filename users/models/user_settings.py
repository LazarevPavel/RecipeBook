from django.db import models


class UserSettingsManager(models.Manager):
    """ Менеджер по работе с пользовательскими настройками """

    def create_settings(self, settings_data=None):
        settings = self.model()
        settings.save()
        return settings


class UserSettings(models.Model):
    """Класс информации о настройках, выставленных пользователем"""
    test_field = models.BooleanField(default=True) #тестовое поле

    objects = UserSettingsManager()