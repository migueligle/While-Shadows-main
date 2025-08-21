from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .apis import OrderBaseViewSet, OrderViewSet,OrderStatusViewSet

urlpatterns = [
    path('orders/', OrderViewSet.as_view({'get': 'list'}), name='order-list'),
      path('orders_base/', OrderBaseViewSet.as_view({'get': 'list'}), name='order-list'),
    path('orders_status/', OrderStatusViewSet.as_view({'get': 'list'}), name='order-status-list'),
    path('orders/create/', OrderViewSet.as_view({'post': 'create_order'}), name='order-create'),
    path('orders/<int:pk>/update/', OrderViewSet.as_view({'put': 'update'}), name='order-update'),
    path('orders/<int:pk>/cancel/', OrderViewSet.as_view({'post': 'cancel_order'}), name='order-cancel'),
    path('orders/<int:pk>/return/', OrderViewSet.as_view({'post': 'return_order'}), name='order-return'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
