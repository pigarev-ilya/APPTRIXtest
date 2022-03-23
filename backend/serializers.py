from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from backend.add_watemark import add_watermark
from backend.models import User
from django.core.exceptions import ValidationError as PasswordValidationError


class RegistrationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'avatar']

    extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            validate_password(validated_data['password'])
        except PasswordValidationError as error:
            raise serializers.ValidationError({'Status': False, 'Errors': f'{error}'})
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            avatar=validated_data['avatar'],
        )
        user.set_password(validated_data['password'])
        user.save()
        add_watermark(user.avatar)
        return user


class CustomAuthTokenSerializer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                raise serializers.ValidationError({'Status': False,
                                                   'Errors': 'Unable to log in with provided credentials.'})
        else:
            raise serializers.ValidationError({'Status': False,
                                               'Errors': 'Must include "username" and "password.'})

        data['user'] = user
        return data
