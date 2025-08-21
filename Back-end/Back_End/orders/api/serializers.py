import base64
from rest_framework import serializers
from orders.models import Order, OrderItem, OrderStatus

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        
class OrderItemListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name='get_product_name')
    image=serializers.SerializerMethodField(method_name='get_product_image')
    mark = serializers.SerializerMethodField(method_name='get_product_mark')
    id = serializers.SerializerMethodField(method_name='get_product_id')
    quantity=serializers.SerializerMethodField(method_name='get_product_quantity')
    price=serializers.SerializerMethodField(method_name='get_product_price')
    total=serializers.SerializerMethodField(method_name='get_product_total')
    def get_product_price(self, order_item):
        try:
            price=order_item.product.price
            return price
        except:
           return None
    
    def get_product_total(self, order_item):
        try:
            total=int(order_item.product.price) * int(order_item.quantity)
            return total
        except:
           return None
    def get_product_name(self, order_item):
        try:
            return order_item.product.name
        except:
            return None
    def get_product_image(self, order_item):
        try:
            image= order_item.product.image
            if image:
                encoded_string = base64.b64encode(image).decode('utf-8')
                return encoded_string
            else:
                return None
        except:
            return None
    
    def get_product_quantity(self, order_item):
        try:
            return order_item.quantity
        except:
            return None

    def get_product_mark(self, order_item):
        try:
            return order_item.product.mark.name 
        except:
            return None
    def get_product_id(self, order_item):
        try:
            return order_item.product.id 
        except:
            return None
     
    class Meta:
        model = OrderItem
        fields = ('id', 'name', 'mark','quantity','price','total','image')  

class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True, read_only=True)
    user=serializers.SerializerMethodField(method_name='get_user')
    status=serializers.SerializerMethodField(method_name='get_status')
    def get_status(self, order):
        try:
           status=order.status
           return{"id":status.id,"status":status.status}
        except:
             return{"id":None,"name":None}
    def get_user(self, order):
        try:
           user=order.user
           return{"id":user.id,"name":user.name,"last_name":user.last_name,"email":user.email}
        except:
             return{"id":None,"name":None,"email":None,"last_name":None,}
    class Meta:
        model = Order
        fields = '__all__'
