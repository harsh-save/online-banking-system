import django_filters
from .models import AccountDetails, User
from django_filters import CharFilter


class userFilter(django_filters.FilterSet):
    name = CharFilter(field_name="full_name",
                      lookup_expr='icontains', label="Full Name:")
    account = CharFilter(field_name='account_number',
                         lookup_expr='icontains', label="Account Number:")

    class Meta:
        model = AccountDetails
        fields = ['account', 'name']
