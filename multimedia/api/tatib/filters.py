from django_filters import rest_framework as django_filters

from multimedia.tatib import models


class TataIbadahFilterSet(django_filters.FilterSet):
    month = django_filters.NumberFilter(field_name='date', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='date', lookup_expr='year')
    has_date = django_filters.BooleanFilter(field_name='date', lookup_expr='isnull', exclude=True)

    class Meta:
        model = models.TataIbadah
        fields = ('month', 'year', 'is_active', 'has_date')


class TataIbadahItemFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.TataIbadahItem
        fields = ('tatib',)
