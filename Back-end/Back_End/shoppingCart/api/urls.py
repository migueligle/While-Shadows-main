from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .apis import ShoppingCartsViewSet

urlpatterns = [
    path('shopping-carts/', ShoppingCartsViewSet.as_view({'get': 'list'}), name='shopping-cart-list'),
     path('shopping-carts/add/', ShoppingCartsViewSet.as_view({'post': 'add_to_shopping_cart'}), name='shopping-cart-add'),
    path('shopping-carts/remove/', ShoppingCartsViewSet.as_view({'post': 'remove_from_shopping_cart'}), name='shopping-cart-remove'),
    path('shopping-carts/increment/', ShoppingCartsViewSet.as_view({'post': 'increment_product_quantity'}), name='shopping-cart-increase'),
    path('shopping-carts/decrement/', ShoppingCartsViewSet.as_view({'post': 'decrement_product_quantity'}), name='shopping-cart-decrease'),
    path('shopping-carts/remove-product/', ShoppingCartsViewSet.as_view({'post': 'remove_product'}), name='remove_product'),
]

urlpatterns = format_suffix_patterns(urlpatterns)