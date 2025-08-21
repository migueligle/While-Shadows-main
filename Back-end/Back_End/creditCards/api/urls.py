from django.urls import path
from rest_framework.routers import DefaultRouter
from .apis import PaymentProcessViewSet

router = DefaultRouter()
router.register(r'payment-process', PaymentProcessViewSet, basename='payment-process')

urlpatterns = []
urlpatterns += router.urls