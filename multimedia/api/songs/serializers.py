from rest_framework import serializers

from multimedia.songs import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        fields = '__all__'


class SongSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='book',
        queryset=models.Book.objects.all(),)

    class Meta:
        model = models.Song
        fields = '__all__'


class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Verse
        fields = '__all__'
