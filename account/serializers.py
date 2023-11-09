from rest_framework import serializers
from .models import Account
from authentication.serializers import ProfileSerial


class AccountSerial(serializers.ModelSerializer):
    profile = ProfileSerial()

    class Meta:
        model = Account
        fields = "__all__"
