from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user import UserRegisterSerializer
from ..logic.registration import RegistrationManager



class RegistrationView(APIView):
    """Представление для обращения с целью регистрации нового пользователя"""

    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.data.get('user', {})
        context = request.data.get('context', {})

        user_serializer = UserRegisterSerializer(data=user, context=context)
        if user_serializer.is_valid(raise_exception=True):
            user = user_serializer.create()
            RegistrationManager.register(user)

        user_serializer = UserRegisterSerializer(instance=user)
        return Response(user_serializer.data, status=status.HTTP_201_CREATED)