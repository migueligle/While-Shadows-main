import base64
from rest_framework import serializers
from products.models import Products

class ProductsListSerializer(serializers.ModelSerializer):
    mark = serializers.SerializerMethodField(method_name='marks_products')
    category = serializers.SerializerMethodField(method_name='category_products')

    def marks_products(self, Products):
        try:
            mark = Products.mark
            return {"id": mark.id, "name": mark.name}
        except:
            return {"id": None, "name": None}

    def category_products(self, Products):
        try:
            category = Products.category
            return {"id": category.id, "name": category.name}
        except:
            return {"id": None, "name": None}

    class Meta:
        model = Products
        fields = ('id', 'name', 'price', 'before_price', 'characteristics', 'description', 'is_stock', 'is_active', 'image', 'image_two', 'image_three', 'mark', 'category', 'video')


class ProductsCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'price', 'before_price', 'characteristics', 'description', 'is_stock', 'is_active', 'image', 'image_two', 'image_three', 'mark', 'category', 'video']
