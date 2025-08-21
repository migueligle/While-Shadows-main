import base64
from rest_framework import serializers
from rest_framework import serializers
from creditCards.models import CreditCard

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'user', 'token', 'last_four_digits', 'mark']