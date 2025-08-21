from django.db import models

from products.models import Products

class ShoppingCarts(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Products, through='ShoppingCardCartItem')
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=4.50)

    class Meta:
        db_table = 'shopping_carts'
        verbose_name = "shopping_cart"
        verbose_name_plural = "shopping_carts"

class ShoppingCardCartItem(models.Model):
    cart = models.ForeignKey(ShoppingCarts, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        db_table = 'shopping_card_cartItem'
