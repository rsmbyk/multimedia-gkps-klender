from rest_framework import viewsets

from multimedia.api.songs import serializers, filters
from multimedia.songs import models


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class SongViewSet(viewsets.ModelViewSet):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer
    filterset_class = filters.SongFilterSet


class VerseViewSet(viewsets.ModelViewSet):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.VerseSerializer
    filterset_class = filters.VerseFilterSet
