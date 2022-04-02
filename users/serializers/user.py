from rest_framework import serializers
from rest_framework.serializers import ValidationError

from ..models.user import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password_retry = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'email']

    def validate_password_retry(self):
        if self.data['password'] != self.password_retry:
            raise ValidationError("Passwords do not match")