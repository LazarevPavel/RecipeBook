import django.contrib.auth.hashers as hasher

from models.user import CustomUser
from models.user_profile import UserProfile
from models.user_settings import UserSettings

class RegistrationManager:
    """Класс, хранящий логику регистрации новых пользователей"""

    def register(self, user):
        user.password = hasher.make_password(user.password)

        #TODO: организовать создание дефолтных настроек профиля (скорее всего надо указать дефолты в моделях) и настроек
        # и сопоставление их с регистрируемым пользователем
        #profile = UserProfile().save()
        #settings = UserSettings().save()

        #user.profile = profile
        #user.settings = settings

        return user.save()