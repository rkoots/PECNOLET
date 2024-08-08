import django_filters
from .models import Stock, Customer

class StockFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Stock
        fields = ['name']

class CustomerFilter(django_filters.FilterSet):
    Name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Customer
        fields = ['Name']

