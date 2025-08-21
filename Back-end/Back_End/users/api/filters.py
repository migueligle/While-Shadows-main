from django_filters import rest_framework as filters
from users.models import User


class UserFilterSet(filters.FilterSet):
    email = filters.CharFilter(field_name='email', lookup_expr='icontains')
    is_staff = filters.BooleanFilter(field_name='is_staff')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['email', 'is_staff', 'is_active']