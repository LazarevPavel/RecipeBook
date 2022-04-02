from ..models.user import UserManager
from ..models.user_profile import UserProfile
from ..models.user_settings import UserSettings


class RegistrationManager:
    """ Регистрация новых пользователей """

    def register(self, user_data):
        #TODO: организовать создание дефолтных настроек профиля (скорее всего надо указать дефолты в моделях) и настроек
        #profile = UserProfileManager.create_profile()
        #settings = UserSettingsManager.create_settings()

        #ВРЕМЯНКИ ДЛЯ ТЕСТОВ (из-за того, что эти модели пока что пустые)
        profile = UserProfile().save()
        settings = UserSettings().save()

        username = user_data.get('username')
        password = user_data.get('password')
        email = user_data.get('email')

        created_user = UserManager.create_user(username=username,
                                               password=password,
                                               email=email,
                                               profile=profile,
                                               settings=settings)

        return created_user