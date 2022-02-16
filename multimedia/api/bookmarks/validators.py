from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from multimedia.bookmarks import models


class UniqueForNullableDateValidator:
    message = _('This bookmark name already exists.')

    def __init__(self, field_name, date_field_name):
        self.field_name = field_name
        self.date_field_name = date_field_name

    def __call__(self, attrs):
        name = attrs.get(self.field_name)
        date = attrs.get(self.date_field_name)

        query_params = {
            'is_active': True,
            self.field_name: name,
            self.date_field_name: date,
        }

        queryset = models.SongBookmark.objects.filter(**query_params)

        if queryset.exists():
            if date is None:
                message = 'This bookmark name already exists'
            else:
                message = 'This bookmark name on this date already exists'
            raise serializers.ValidationError({'name': message})
