from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from serializers.user import UserSerializer
from logic.registration import RegistrationManager



class RegistrationView(APIView):
    """Представление для обращения с целью регистрации нового пользователя"""

    def post(self, request):
        user = request.data.get('user')

        serializer = UserSerializer(data=user)
        if serializer.is_valid(raise_exception=True):
            RegistrationManager.register(serializer.create())

        return Response(status=status.HTTP_200_OK)