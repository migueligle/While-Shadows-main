from django_filters import rest_framework as filters
from banners.models import Banners

class BannersFilter(filters.FilterSet):
    is_active = filters.BooleanFilter(field_name='is_active')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
   

    class Meta:
        model = Banners
        fields = ['name', 'is_active']