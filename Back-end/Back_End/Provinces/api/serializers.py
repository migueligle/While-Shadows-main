from rest_framework import serializers
from ..models import provinces

class ProvincesSerializers(serializers.ModelSerializer):
    
  class Meta:
        model = provinces
        fields='__all__'
