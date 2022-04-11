from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models.user import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password_retry = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email', 'password_retry']

    def validate_password_retry(self, password_retry):
        if self.initial_data['password'] != password_retry:
            raise ValidationError("Passwords do not match")