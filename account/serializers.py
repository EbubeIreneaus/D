from rest_framework import serializers
from .models import Account
from authentication.serializers import ProfileSerial


class AccountSerial(serializers.ModelSerializer):
    profile = ProfileSerial()

    class Meta:
        model = Account
        fields = "__all__"

class CryptoSerial(serializers.ModelSerializer):
    profile = ProfileSerial()

    class Meta:
        model = Account
        fields = ['profile', 'balance','btc', 'eth', 'ltc', 'bnb', 'link', 'xrp','ada', 'aave', 'bch', 'usdt', 'xlm']