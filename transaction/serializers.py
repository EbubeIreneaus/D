from rest_framework import serializers
from .models import Transaction
from authentication.serializers import ProfileSerial


class TransactionSerializer(serializers.ModelSerializer):
    profile = ProfileSerial()

    class Meta:
        model = Transaction
        fields = '__all__'
