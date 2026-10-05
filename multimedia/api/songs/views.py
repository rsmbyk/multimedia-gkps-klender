from rest_framework import viewsets

from multimedia.api.songs import serializers, filters
from multimedia.songs import models


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookSerializer

    def get_queryset(self):
        return models.Book.objects.active()


class SongViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SongSerializer
    filterset_class = filters.SongFilterSet

    def get_queryset(self):
        return models.Song.objects.active().filter(book__is_deleted=False)


class VerseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.VerseSerializer
    filterset_class = filters.VerseFilterSet

    def get_queryset(self):
        return models.Verse.objects.active().filter(
            song__is_deleted=False, song__book__is_deleted=False)
