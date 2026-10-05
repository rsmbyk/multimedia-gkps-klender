from django.core.validators import MinValueValidator
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
        ordering = ['-is_hymn_book', 'name', 'lang']
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
    is_untitled = models.BooleanField(default=False)
    key = models.CharField(max_length=4, blank=True, choices=Key.choices)
    modified = models.DateTimeField(
        null=True, auto_now=True,
        help_text='Stamped on every save; rows that predate tracking share '
                  'the migration timestamp.')

    @property
    def book_number(self):
        return f'{self.book.short_name} {self.number}{self.sub_number.upper()}'

    def __str__(self):
        if self.book.is_hymn_book:
            return f'{self.book_number} ({self.title})'
        return f'{self.title} ({self.book})'

    class Meta:
        ordering = ['book', 'number', 'sub_number', 'title']
        unique_together = ['book', 'number', 'sub_number']


class Verse(models.Model):
    song = models.ForeignKey(Song, models.CASCADE)
    number = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    lyric = models.TextField()

    @property
    def song_name(self):
        if self.song.book.is_hymn_book:
            return self.song.book_number
        return self.song

    def __str__(self):
        trailing_verse = f' : {self.number}' if self.song.verse_set.count() > 1 else ''
        return f'{self.song_name}{trailing_verse}'

    class Meta:
        ordering = ['song', 'number']
        unique_together = ['song', 'number']
