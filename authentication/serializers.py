from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User



class UserSerial(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]


class ProfileSerial(serializers.ModelSerializer):
    user = UserSerial()
    referred_by = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = "__all__"

    def get_referred_by(self, obj):
        if obj.referred_by:
            serialize_ref = ProfileSerial(obj.referred_by)
            return serialize_ref.data
        return None
