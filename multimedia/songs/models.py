from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

from multimedia.songs.validators import BookShortNameUniqueValidator


class SoftDeleteQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)

    def delete(self):
        deleted = self.active().update(is_deleted=True, deleted_at=timezone.now())
        return deleted, {self.model._meta.label: deleted}


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    pass


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True, editable=False)
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, models.SET_NULL, null=True, blank=True,
        related_name='%(app_label)s_%(class)s_deleted', editable=False)
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def soft_delete(self, deleted_by=None, using=None):
        database = using or self._state.db or 'default'
        deleted_at = timezone.now()
        updates = {'is_deleted': True, 'deleted_at': deleted_at}
        if deleted_by is not None:
            updates['deleted_by'] = deleted_by
        deleted = type(self).objects.using(database).filter(
            pk=self.pk, is_deleted=False).update(**updates)
        self.is_deleted = True
        self.deleted_at = deleted_at
        if deleted_by is not None:
            self.deleted_by = deleted_by
        return deleted, {self._meta.label: deleted}

    def delete(self, using=None, keep_parents=False):
        return self.soft_delete(using=using)


class Book(SoftDeleteModel):
    name = models.CharField(max_length=32, unique=True)
    short_name = models.CharField(
        max_length=8,
        blank=True,
        validators=[BookShortNameUniqueValidator()])
    is_hymn_book = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-is_hymn_book', 'name']


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


class Song(SoftDeleteModel):
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


class Verse(SoftDeleteModel):
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
        constraints = [
            models.UniqueConstraint(fields=['song', 'number'], condition=models.Q(is_deleted=False),
                                    name='verse_live_number_unique'),
        ]
