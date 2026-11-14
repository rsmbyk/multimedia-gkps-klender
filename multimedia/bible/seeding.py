"""Helpers for maintaining reference data during Bible seeding."""

from multimedia.bible import models


def apply_book_abbreviations(version, abbreviations):
    """Update short codes on already seeded book translation rows, in place."""
    for book_name, abbreviation in abbreviations.items():
        translation = (models.BookTranslation.objects
                       .filter(version=version, book__name=book_name)
                       .order_by('pk').first())
        if translation is None:
            raise models.BookTranslation.DoesNotExist(
                f'Missing {version.abbreviation} translation row for {book_name}')
        if translation.abbreviation != abbreviation:
            translation.abbreviation = abbreviation
            translation.save(update_fields=['abbreviation'])
