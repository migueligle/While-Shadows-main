from rest_framework import serializers
from ..models import Categories

class CategoriesSerializers(serializers.ModelSerializer):
    
  class Meta:
        model = Categories
        fields=('name',"id","image",'is_active')
