from django.db import models
from products.models import Products
from users.models import User

class OrderStatus(models.Model):
    status = models.CharField(max_length=80)

    def __str__(self):
        return self.status
    class Meta:
        db_table = 'order_status'
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField(Products, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(db_index=True,null=False,blank=False,default=False)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=4.50)
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    class Meta:
        db_table = 'orders'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in order {self.order.id}"
    class Meta:
        db_table = 'orders_items'
