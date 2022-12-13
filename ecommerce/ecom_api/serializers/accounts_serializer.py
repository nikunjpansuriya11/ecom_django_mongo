from datetime import datetime
from rest_framework import serializers
from core.models import User


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    city = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        return User.objects.create(**validated_data)


class UserResponseSerializer(serializers.Serializer):
    user_id = serializers.CharField() 
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    city = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.EmailField()
    phone_number = serializers.CharField()
    is_phone_verified = serializers.BooleanField()
    is_email_verified = serializers.BooleanField()
    is_active = serializers.BooleanField()