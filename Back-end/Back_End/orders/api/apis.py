from django.db import transaction

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from orders.api.filters import OrderFilterSet
from orders.api.serializers import OrderListSerializer, OrderSerializer, OrderStatusSerializer
from orders.models import Order, OrderItem, OrderStatus
from shoppingCart.models import ShoppingCarts
from base.pagination import smallPagination
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings

class OrderStatusViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    queryset = OrderStatus.objects.all()
    serializer_class= OrderStatusSerializer
    filter_class = OrderFilterSet

    def list(self, request, *args, **kwargs):
        queryset = OrderStatus.objects.all()
        filterset = self.filter_class(request.query_params, queryset=queryset)
        queryset = filterset.qs
        serializer = OrderStatusSerializer(queryset, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    filter_class = OrderFilterSet
    queryset = Order.objects.select_related('status').all()
    pagination_class = smallPagination
    
   
    def list(self, request):
        if request.user.is_staff:
            orders = Order.objects.select_related('status').all()
        else:
            orders = Order.objects.select_related('status').filter(user=request.user)
        filterset = self.filter_class(request.query_params, queryset=orders)
        orders = filterset.qs
        paginator = self.pagination_class()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderListSerializer(paginated_orders, many=True)
        
        return paginator.get_paginated_response(serializer.data)
    def update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({"error": "El pedido especificado no existe"}, status=status.HTTP_404_NOT_FOUND)
        new_status_id = request.data['status'].get('id', None)
        if not request.user.is_staff and request.user != order.user:
            return Response({"error": "No tienes permisos para actualizar el estado de este pedido"}, status=status.HTTP_403_FORBIDDEN)
        if new_status_id is None:
            return Response({"error": "Se debe proporcionar un nuevo estado para actualizar el pedido"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_status = OrderStatus.objects.get(pk=new_status_id)
        except OrderStatus.DoesNotExist:
            return Response({"error": "El estado proporcionado no es válido"}, status=status.HTTP_400_BAD_REQUEST)
        if order.status == new_status:
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        order.status = new_status
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def create_order(self, request):
        cart = ShoppingCarts.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)
        
        total_amount = sum(item.product.price * item.quantity for item in cart.items.all())
        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_amount=total_amount,status_id=1)
            for cart_item in cart.items.all():
                OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            cart.items.all().delete()
            cart.delete()
        
        subject = 'Pedido realizado correctamente'
        message = 'Su pedido ha sido realizado correctamente. Puede ver el estado de su pedido en su sección de pedidos.'
        email_from = request.user.email
        recipient_list = [request.user.email]
        send_mail(subject, message, email_from, recipient_list)
        
        serializer = OrderSerializer(order)
        return Response(serializer.data)
   
    
    def cancel_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if request.user == order.user or request.user.is_staff:
            if order.status.id in [1, 2]:
                try:
                    cancel_status = OrderStatus.objects.get(id=4) 
                except OrderStatus.DoesNotExist:
                    return Response({"error": "El estado de cancelación no existe"}, status=status.HTTP_400_BAD_REQUEST)
                
                with transaction.atomic():
                    order.status = cancel_status
                    order.save()
                
                serializer = OrderSerializer(order)
                return Response(serializer.data)
            else:
                return Response({"error": "El pedido no se puede cancelar porque  ya ha sido enviado"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No tienes permiso para cancelar este pedido"}, status=status.HTTP_403_FORBIDDEN)
        
    def return_order(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)
        if order.status.id != 3:
            return Response({"error": "El pedido no ha sido  enviado, por lo que no se puede devolver"}, status=status.HTTP_400_BAD_REQUEST)
        if request.user == order.user or request.user.is_staff:
            try:
                return_status = OrderStatus.objects.get(id=5) 
            except OrderStatus.DoesNotExist:
                return Response({"error": "El estado de devolución no existe"}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                order.status = return_status
                order.save()
            
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"error": "No tienes permiso para devolver este pedido"}, status=status.HTTP_403_FORBIDDEN)
        
class OrderBaseViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    filter_class = OrderFilterSet
    queryset = Order.objects.select_related('status').all()
    pagination_class = smallPagination

    def list(self, request):
        orders = Order.objects.select_related('status').filter(user=request.user)
        filterset = self.filter_class(request.query_params, queryset=orders)
        orders = filterset.qs
        paginator = self.pagination_class()
        paginated_orders = paginator.paginate_queryset(orders, request)
        serializer = OrderListSerializer(paginated_orders, many=True)
        return paginator.get_paginated_response(serializer.data)