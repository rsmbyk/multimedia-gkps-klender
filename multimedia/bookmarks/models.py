from django.db import models

from multimedia.songs.models import Song


class SongBookmark(models.Model):
    name = models.CharField(max_length=64, unique=True)
    date = models.DateField()

    def __str__(self):
        return self.name
