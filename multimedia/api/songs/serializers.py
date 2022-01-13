from rest_framework import serializers

from multimedia.songs import models


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Verse
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Song
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    lang = serializers.ReadOnlyField(source='lang.name')

    class Meta:
        model = models.Book
        fields = '__all__'
