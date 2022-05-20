from rest_framework import viewsets, filters as rf_filters
from django_filters import rest_framework as django_filters
from rest_framework.decorators import action
from rest_framework.response import Response

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

    @action(methods=['POST'], detail=False, url_name='reorder')
    def reorder(self, request):
        serializer = serializers.TataIbadahReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for item in serializer.validated_data['items']:
            bookmark_item = models.TataIbadahItem.objects.get(id=item['item'].id)
            bookmark_item.order_number = item['order_number']
            bookmark_item.save()
        return Response(serializer.data)
