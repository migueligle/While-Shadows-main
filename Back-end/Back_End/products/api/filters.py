from django_filters import rest_framework as filters
from products.models import Products

class ProductFilterSet(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    mark = filters.NumberFilter(field_name='mark')
    category = filters.NumberFilter(field_name='category')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    is_stock = filters.BooleanFilter(field_name='is_stock')

    class Meta:
        model = Products
        fields = ['min_price', 'max_price', 'mark', 'category', 'name', 'is_stock','is_active']
