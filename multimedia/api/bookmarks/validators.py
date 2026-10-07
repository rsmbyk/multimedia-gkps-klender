from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from multimedia.bookmarks import models


class UniqueForNullableDateValidator:
    message = _('This bookmark name already exists.')

    def __init__(self, field_name, date_field_name):
        self.field_name = field_name
        self.date_field_name = date_field_name
        self.instance = None

    def set_context(self, serializer):
        """DRF calls this so validators can exclude the instance on update."""
        self.instance = getattr(serializer, 'instance', None)

    def __call__(self, attrs):
        instance = self.instance
        name = attrs.get(
            self.field_name,
            getattr(instance, self.field_name, None) if instance else None,
        )
        date = attrs.get(
            self.date_field_name,
            getattr(instance, self.date_field_name, None) if instance else None,
        )

        query_params = {
            'is_active': True,
            self.field_name: name,
            self.date_field_name: date,
        }

        queryset = models.SongBookmark.objects.filter(**query_params)
        if instance is not None:
            queryset = queryset.exclude(pk=instance.pk)

        if queryset.exists():
            if date is None:
                message = 'This bookmark name already exists'
            else:
                message = 'This bookmark name on this date already exists'
            raise serializers.ValidationError({'name': message})
