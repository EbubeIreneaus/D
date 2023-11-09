from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User


class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileSerial(serializers.ModelSerializer):
    user = UserSerial()

    class Meta:
        model = Profile
        fields = "__all__"
