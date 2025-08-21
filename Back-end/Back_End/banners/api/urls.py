from django.urls import path
from banners.api.apis import BannersBaseViewSet, BannersViewSet


urlpatterns = [
path('banners/', BannersViewSet.as_view({'get': 'list', 'post': 'create'}), name='banner-list-create'),
path('banners-base/', BannersBaseViewSet.as_view({'get': 'list'}), name='banner-list-base'),
path('banners/<int:pk>/', BannersViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update',}), name='banner-detail'),
path('banners/<int:pk>/deactivate_banner/', BannersViewSet.as_view({'put': 'deactivate_banner'}), name='banner-deactivate'),
]
