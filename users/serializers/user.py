from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models.user import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'token']

    def create(self):
        return CustomUser(**self.validated_data)

    def validate_password(self, password):
        if self.context.get('password_retry', None):
            if self.initial_data['password'] != self.context['password_retry']:
                raise ValidationError("Passwords do not match")
        else:
            raise ValidationError("Password retry is required")
        return password
