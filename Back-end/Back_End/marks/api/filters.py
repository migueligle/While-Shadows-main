from django_filters import rest_framework as filters
from marks.models import marks

class MarkFilterSet(filters.FilterSet):
    is_stock = filters.BooleanFilter(field_name='is_stock')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = marks
        fields = ['is_active','name']