from django_filters import rest_framework as filters
from categories.models import Categories

class CategoriesFilterSet(filters.FilterSet):
    is_stock = filters.BooleanFilter(field_name='is_stock')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Categories
        fields = ['is_active','name']
        
        
        