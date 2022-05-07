from django.db.models import Max
from rest_framework import serializers

from multimedia.tatib import models


class TataIbadahItemSerializer(serializers.ModelSerializer):
    order_number = serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        tatib: models.TataIbadah = validated_data['tatib']
        max_order_number_aggr = tatib.tataibadahitem_set.aggregate(Max('order_number'))['order_number__max']
        max_order_number = max_order_number_aggr or 0
        data = {**validated_data, 'order_number': max_order_number + 1}
        return models.TataIbadahItem.objects.create(**data)

    class Meta:
        model = models.TataIbadahItem
        fields = '__all__'


class TataIbadahSerializer(serializers.ModelSerializer):
    date = serializers.DateField(allow_null=True, required=False, default=None)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = models.TataIbadah
        fields = '__all__'
