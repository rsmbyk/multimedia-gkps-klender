from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from multimedia.songs.models import Song


class SongBookmark(models.Model):
    name = models.CharField(max_length=32)
    date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.name} ({self.date})'

    class Meta:
        ordering = ('-date', '-created_at')


class SongBookmarkItem(models.Model):
    bookmark = models.ForeignKey(SongBookmark, models.PROTECT)
    song = models.ForeignKey(Song, models.PROTECT)
    verse = models.CharField(
        max_length=64,
        validators=[validate_comma_separated_integer_list])
    order_number = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f'{self.bookmark}: ({self.order_number} - {self.song})'

    class Meta:
        ordering = ('bookmark', 'order_number')
