from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from products.models import Products
from shoppingCart.api.serializers import ShoppingCartsSerializer
from shoppingCart.models import ShoppingCardCartItem, ShoppingCarts

class ShoppingCartsViewSet(viewsets.ViewSet):

    permission_classes = [IsAuthenticated]

    def get_ShoppingCart(self, user):
        shoppingcart, _ = ShoppingCarts.objects.get_or_create(user=user)
        return shoppingcart

    def list(self, request):
        shoppingcart = self.get_ShoppingCart(request.user)
        serializer = ShoppingCartsSerializer(shoppingcart)
        return Response(serializer.data)

    def add_to_shopping_cart(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Products, id=product_id)
        shoppingcart = self.get_ShoppingCart(request.user)
        cart_item = shoppingcart.items.filter(product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = ShoppingCardCartItem.objects.create(cart=shoppingcart, product=product, quantity=quantity)
        serializer = ShoppingCartsSerializer(shoppingcart)
        return Response(serializer.data)
    
    def remove_product(self, request):
        product_id = request.data.get('product_id')
        product = get_object_or_404(Products, id=product_id)
        shoppingcart = self.get_ShoppingCart(request.user)
        cart_item = get_object_or_404(ShoppingCardCartItem, cart=shoppingcart, product=product)
        cart_item.delete()
        serializer = ShoppingCartsSerializer(shoppingcart)
        return Response(serializer.data)

    def increment_product_quantity(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Products, id=product_id)
        shoppingcart = self.get_ShoppingCart(request.user)
        cart_item = shoppingcart.items.filter(product=product).first()
        if cart_item:
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = ShoppingCardCartItem.objects.create(cart=shoppingcart, product=product, quantity=quantity)
        serializer = ShoppingCartsSerializer(shoppingcart)
        return Response(serializer.data)

    def decrement_product_quantity(self, request):
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        product = get_object_or_404(Products, id=product_id)
        shoppingcart = self.get_ShoppingCart(request.user)
        cart_item = shoppingcart.items.filter(product=product).first()
        if cart_item:
            new_quantity = cart_item.quantity - quantity
            if new_quantity >= 0:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return JsonResponse({'error': 'No puede disminuir la cantidad por debajo de cero.'}, status=400)
        serializer = ShoppingCartsSerializer(shoppingcart)
        return Response(serializer.data)
