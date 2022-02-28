from drf_dynamic_fields import DynamicFieldsMixin
from rest_framework import serializers

import multimedia.songs.models
from multimedia.api.bookmarks import validators
from multimedia.bookmarks import models


class SongBookmarkSerializer(serializers.ModelSerializer):
    date = serializers.DateField(allow_null=True, required=False, default=None)
    is_active = serializers.BooleanField(required=False, default=True)

    class Meta:
        model = models.SongBookmark
        fields = '__all__'
        validators = [validators.UniqueForNullableDateValidator('name', 'date')]


class SongBookmarkItemSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    verse_info = serializers.SerializerMethodField(read_only=True)
    song_info = serializers.SerializerMethodField(read_only=True)

    def get_verse_info(self, obj):
        verse_numbers = list(map(int, obj.verse.split(',')))
        verses = obj.song.verse_set.filter(number__in=verse_numbers)
        return map(lambda x: {'number': x.number, 'lyric': x.lyric}, verses)

    def get_song_info(self, obj):
        book_number = None \
            if not obj.song.book.is_hymn_book \
            else f'{obj.song.book.short_name} {obj.song.number}{obj.song.sub_number}'

        return {
            'book_number': book_number,
            'title': obj.song.title,
            'is_untitled': obj.song.is_untitled,
        }

    class Meta:
        model = models.SongBookmarkItem
        fields = '__all__'
