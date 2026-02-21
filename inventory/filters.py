import django_filters
from .models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    brand = django_filters.CharFilter(lookup_expr='icontains')
    fuel_type = django_filters.CharFilter()
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Vehicle
        fields = ['brand', 'fuel_type', 'is_available']
