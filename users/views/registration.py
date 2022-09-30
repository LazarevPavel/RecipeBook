from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.user import UserRegisterSerializer
from unwolfable.base.base_renderer import BaseJSONRenderer

from ..logic.registration import RegistrationManager


class RegistrationView(APIView):
    """Представление для обращения с целью регистрации нового пользователя"""

    permission_classes = (AllowAny,)
    renderer_classes = (BaseJSONRenderer,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user = request.data.get('user', {})
        context = request.data.get('context', {})

        serializer = self.serializer_class(data=user, context=context)
        if serializer.is_valid(raise_exception=True):
            user = serializer.create()
            RegistrationManager.register(user)

        serializer = self.serializer_class(instance=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
