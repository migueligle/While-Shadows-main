import base64
from rest_framework import serializers
from shoppingCart.models import ShoppingCarts, ShoppingCardCartItem
from django.db.models import Sum,F

class ShoppingCardCartItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(method_name='get_products')
    product_total=serializers.SerializerMethodField(method_name='get_products_total')
    def get_products(self, shopping_card_cart_item):
        try:
            product = shopping_card_cart_item.product
            return {
                "name": product.name,
                "id": product.id,
                "mark": product.mark.name,
                "price": product.price,
                "image": base64.b64encode(product.image).decode('utf-8')
            }
        except:
            return {"name": None, "id": None, "mark": None, "price": None}
    def get_products_total(self, shopping_card_cart_item):
        try:
            product = shopping_card_cart_item.product.price
            quantity=shopping_card_cart_item.quantity
            return product * quantity
        except:
            return None
        
    class Meta:
        model = ShoppingCardCartItem
        fields = '__all__'

class ShoppingCartsSerializer(serializers.ModelSerializer):
    items = ShoppingCardCartItemSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        total_price = obj.items.aggregate(
            total_price=Sum(F('product__price') * F('quantity'))
        )['total_price']
        return total_price or 0

    def get_product_count(self, obj):
        return obj.items.aggregate(total_count=Sum('quantity'))['total_count'] or 0

    class Meta:
        model = ShoppingCarts
        fields = '__all__'