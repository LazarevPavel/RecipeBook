from ..models.user import CustomUser
from ..models.user_profile import UserProfile
from ..models.user_settings import UserSettings


class RegistrationManager:
    """ Менеджер по регистрации новых пользователей """

    @classmethod
    def register(cls, user_data):
        #TODO: организовать создание дефолтных настроек профиля (скорее всего надо указать дефолты в моделях) и настроек
        profile = UserProfile.objects.create_profile(None)
        settings = UserSettings.objects.create_settings(None)

        username = user_data.get('username')
        password = user_data.get('password')
        email = user_data.get('email')

        created_user = CustomUser.objects.create_user(username=username,
                                                      password=password,
                                                      email=email,
                                                      profile=profile,
                                                      settings=settings)

        return created_user