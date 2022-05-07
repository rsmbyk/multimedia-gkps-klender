from rest_framework import viewsets, filters as rf_filters
from django_filters import rest_framework as django_filters

from multimedia.api.tatib import serializers, filters
from multimedia.tatib import models


class TataIbadahViewSet(viewsets.ModelViewSet):
    queryset = models.TataIbadah.objects.all()
    serializer_class = serializers.TataIbadahSerializer
    filterset_class = filters.TataIbadahFilterSet


class TataIbadahItemViewSet(viewsets.ModelViewSet):
    queryset = models.TataIbadahItem.objects.all()
    serializer_class = serializers.TataIbadahItemSerializer
    filter_backends = [django_filters.DjangoFilterBackend, rf_filters.OrderingFilter]
    ordering_fields = ['tatib', 'order_number']
    filterset_class = filters.TataIbadahItemFilterSet
