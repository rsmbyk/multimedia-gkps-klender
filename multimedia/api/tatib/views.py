from rest_framework import viewsets

from multimedia.api.tatib import serializers, filters
from multimedia.tatib import models


class TataIbadahViewSet(viewsets.ModelViewSet):
    queryset = models.TataIbadah.objects.all()
    serializer_class = serializers.TataIbadahSerializer
    filterset_class = filters.TataIbadahFilterSet


class TataIbadahItemViewSet(viewsets.ModelViewSet):
    queryset = models.TataIbadahItem.objects.all()
    serializer_class = serializers.TataIbadahItemSerializer
