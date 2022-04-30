from rest_framework import serializers

from multimedia.tatib import models


class TataIbadahItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TataIbadahItem
        fields = '__all__'


class TataIbadahSerializer(serializers.ModelSerializer):
    date = serializers.DateField(allow_null=True, required=False, default=None)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = models.TataIbadah
        fields = '__all__'
