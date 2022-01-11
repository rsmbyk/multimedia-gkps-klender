from django.db import models

from multimedia.songs.validators import BookShortNameUniqueValidator


class Language(models.Model):
    name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    lang = models.ForeignKey(Language, models.PROTECT)
    name = models.CharField(max_length=32)
    short_name = models.CharField(
        max_length=8,
        blank=True,
        validators=[BookShortNameUniqueValidator()])
    is_hymn_book = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} ({self.lang})'

    class Meta:
        ordering = ['-is_hymn_book', 'name']
        unique_together = ['lang', 'name']
