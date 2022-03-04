from rest_framework import viewsets

from multimedia.api.bible import serializers, filters
from multimedia.bible import models


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer


class VersionViewSet(viewsets.ModelViewSet):
    queryset = models.Version.objects.all()
    serializer_class = serializers.VersionSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookTranslationViewSet(viewsets.ModelViewSet):
    queryset = models.BookTranslation.objects.all()
    serializer_class = serializers.BookTranslationSerializer
    filterset_class = filters.BookTranslationFilterSet


class VerseViewSet(viewsets.ModelViewSet):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.VerseSerializer
    filterset_class = filters.VerseFilterSet
