from django_filters import rest_framework as django_filters

from multimedia.bible import models


class BookTranslationFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.BookTranslation
        fields = ('version', 'version__abbreviation', 'book__name')


class VerseFilterSet(django_filters.FilterSet):
    class Meta:
        model = models.Verse
        fields = (
            'book_translation__version__abbreviation',
            'book_translation__book__name',
            'book_translation',
            'chapter',
            'verse',
        )
