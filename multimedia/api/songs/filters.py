from django_filters import rest_framework as django_filters

from multimedia.songs import models


class SongFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Song
        fields = ('book',)


class VerseFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Verse
        fields = ('song',)
