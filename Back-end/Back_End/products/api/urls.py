from django.urls import path
from rest_framework.routers import DefaultRouter
from products.api.apis import ProductsViewSet, ProductsBaseViewSet

router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'products-base', ProductsBaseViewSet, basename='products-base')

urlpatterns = [
    path('products-base/', ProductsBaseViewSet.as_view({'get': 'list'}), name='products-base-list')
]

urlpatterns += router.urls