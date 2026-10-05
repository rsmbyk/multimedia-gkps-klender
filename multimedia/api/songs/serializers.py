from rest_framework import serializers

from multimedia.songs import models


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Book
        exclude = ('is_deleted', 'deleted_at', 'deleted_by')


class SongSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        source='book',
        queryset=models.Book.objects.active(),)

    class Meta:
        model = models.Song
        exclude = ('is_deleted', 'deleted_at', 'deleted_by')


class VerseSerializer(serializers.ModelSerializer):
    song = serializers.PrimaryKeyRelatedField(
        queryset=models.Song.objects.active().filter(book__is_deleted=False))

    class Meta:
        model = models.Verse
        exclude = ('is_deleted', 'deleted_at', 'deleted_by')
