from django.contrib import admin

from multimedia.songs import models


@admin.register(models.Song)
class SongAdmin(admin.ModelAdmin):
    list_filter = ['book']
    search_fields = [
        'book__name',
        'book__short_name',
        'title',
        'number',
        'sub_number',
    ]


@admin.register(models.Verse)
class VerseAdmin(admin.ModelAdmin):
    list_filter = ['song__book']
    autocomplete_fields = ['song']
    search_fields = [
        'song__book__name',
        'song__book__short_name',
        'song__title',
        'song__number',
        'lyric',
    ]


admin.site.register(models.Language)
admin.site.register(models.Book)
