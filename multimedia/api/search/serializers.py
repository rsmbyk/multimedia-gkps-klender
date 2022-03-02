from rest_framework import serializers

from multimedia.api.songs import serializers as songs_serializers
from multimedia.songs import models


class SearchSerializer(serializers.Serializer):
    q = serializers.CharField(min_length=3)


class SongSearchResultSerializer(serializers.ModelSerializer):
    song = songs_serializers.SongSerializer(read_only=True)

    class Meta:
        model = models.Verse
        fields = '__all__'
