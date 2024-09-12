from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['wallet_address']

    def validate_wallet_address(self, value):
        if not value.startswith('0x') or len(value) != 42:
            raise serializers.ValidationError(
                "Invalid Ethereum address format")
        return value
