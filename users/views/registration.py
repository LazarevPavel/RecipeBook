from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user import UserRegisterSerializer
from ..logic.registration import RegistrationManager



class RegistrationView(APIView):
    """Представление для обращения с целью регистрации нового пользователя"""

    def post(self, request):
        user = request.data.get('user')

        serializer = UserRegisterSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            RegistrationManager.register(serializer.validated_data)

        return Response(status=status.HTTP_200_OK)