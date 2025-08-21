
from django_filters import rest_framework as filters
from orders.models import Order


class OrderFilterSet(filters.FilterSet):
    email = filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    user_id=filters.NumberFilter(field_name='user__id')
    status = filters.CharFilter(field_name='status__id', lookup_expr='icontains')
    date_start = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    date_end = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    is_paid = filters.BooleanFilter(field_name='is_paid')
    class Meta:
        model = Order
        fields = ['email', 'status', 'date_end', 'date_start','user_id']

