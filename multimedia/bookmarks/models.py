from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from multimedia.songs.models import Song


class SongBookmark(models.Model):
    name = models.CharField(max_length=64, unique=True)
    date = models.DateField()

    def __str__(self):
        return self.name


class SongBookmarkItem(models.Model):
    bookmark = models.ForeignKey(SongBookmark, models.PROTECT)
    song = models.ForeignKey(Song, models.PROTECT)
    verse = models.CharField(
        max_length=64,
        validators=[validate_comma_separated_integer_list])
    order_number = models.PositiveIntegerField(blank=True)

    def __str__(self):
        return f'{self.bookmark}: {self.song}'

    class Meta:
        ordering = ('bookmark', 'song')
        unique_together = (('bookmark', 'song'), ('bookmark', 'order_number'))
