from django.urls import path
from .apis import ProvincesModelViewSet

urlpatterns = [
    path('provinces/', ProvincesModelViewSet.as_view({'get': 'list'}), name='provinces'),
   
]
