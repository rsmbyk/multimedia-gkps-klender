from django.db.models import Max
from rest_framework import serializers

from multimedia.tatib import models


class TataIbadahItemSerializer(serializers.ModelSerializer):
    order_number = serializers.IntegerField(read_only=True)
    insert_after = serializers.IntegerField(required=False)

    def create(self, validated_data):
        tatib: models.TataIbadah = validated_data['tatib']

        insert_after = validated_data.pop('insert_after', None)
        if insert_after is None:
            max_order_number_aggr = tatib.tataibadahitem_set.aggregate(Max('order_number'))['order_number__max']
            max_order_number = max_order_number_aggr or 0
        else:
            max_order_number = insert_after
            items = models.TataIbadahItem.objects.filter(order_number__gt=insert_after)
            for item in items:
                item.order_number += 1
            models.TataIbadahItem.objects.bulk_update(items, ['order_number'])

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


class TataIbadahItemReorderSerializer(serializers.Serializer):
    item = serializers.PrimaryKeyRelatedField(queryset=models.TataIbadahItem.objects.all())
    order_number = serializers.IntegerField()


class TataIbadahReorderSerializer(serializers.Serializer):
    items = TataIbadahItemReorderSerializer(many=True)
