from rest_framework import serializers

class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


class LoginResponseSerializer(serializers.Serializer):
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
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()
