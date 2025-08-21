from rest_framework import serializers
from ..models import marks

class MarksSerializers(serializers.ModelSerializer):
    
  class Meta:
        model = marks
        fields=('name',"id",'is_active')
