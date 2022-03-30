from rest_framework import serializers

from models.user import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['profile', 'settings']

    def create(self, validated_data):
        return CustomUser(**validated_data)
