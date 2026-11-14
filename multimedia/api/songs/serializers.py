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
    # These are read-only on the API: managed elsewhere (hymn books auto-number,
    # free songs leave them unset). Kept here so consumers that display the song
    # (OBS projection, verse index) still get their values.
    number = serializers.IntegerField(read_only=True)
    sub_number = serializers.CharField(read_only=True)
    key = serializers.CharField(read_only=True)

    class Meta:
        model = models.Song
        fields = ['id', 'title', 'is_untitled', 'modified', 'book', 'book_id',
                  'number', 'sub_number', 'key']
        read_only_fields = ['number', 'sub_number', 'key']


class VerseSerializer(serializers.ModelSerializer):
    song = serializers.PrimaryKeyRelatedField(
        queryset=models.Song.objects.active().filter(book__is_deleted=False))

    class Meta:
        model = models.Verse
        exclude = ('is_deleted', 'deleted_at', 'deleted_by')
