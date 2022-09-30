from ..models.user import CustomUser


class RegistrationManager:
    """ Менеджер по регистрации новых пользователей """

    @classmethod
    def register(cls, user):
        created_user = CustomUser.objects.create_user(username=user.username,
                                                      password=user.password,
                                                      email=user.email,
                                                      )

        return created_user
