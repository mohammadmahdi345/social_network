from django.contrib.auth import get_user_model
from django.core.validators import validate_email

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator])

    password_1 = serializers.CharField(required=True, write_only=True)
    password_2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password_1', 'password_2', 'first_name', 'last_name')

    extra_kwargs = {
        'first_name': {'required': False},
        'last_name': {'required': False},
    }

    def validate(self, attrs):
        if attrs['password_1'] != attrs['password_2']:
            raise serializers.ValidationError
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password_1'],
        )
        return user