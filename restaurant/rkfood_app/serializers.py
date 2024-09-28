from rest_framework import serializers
from django.contrib.auth.models import User
from rkfood_app.models import Customer


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['phone']

