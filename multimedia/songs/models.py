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


class Key(models.TextChoices):
    C = 'c'
    Db = 'des'
    D = 'd'
    Eb = 'es'
    E = 'e'
    F = 'f'
    Gb = 'ges'
    G = 'g'
    Ab = 'as'
    A = 'a'
    Bb = 'bes'
    B = 'b'


class Song(models.Model):
    book = models.ForeignKey(Book, models.PROTECT)
    number = models.PositiveIntegerField(blank=True, null=True)
    sub_number = models.CharField(max_length=1, blank=True)
    title = models.CharField(max_length=64)
    key = models.CharField(max_length=4, blank=True, choices=Key.choices)

    @property
    def book_number(self):
        return f'{self.book.short_name} {self.number}{self.sub_number.upper()}'

    def __str__(self):
        if self.book.is_hymn_book:
            return f'{self.book_number} ({self.title})'
        return f'{self.title} ({self.book}'

    class Meta:
        ordering = ['book', 'number', 'sub_number']
        unique_together = ['book', 'number', 'sub_number']
