from django.contrib import admin

from multimedia.bookmarks import models


@admin.register(models.SongBookmark)
class SongBookmarkAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(models.SongBookmarkItem)
class SongBookmarkItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['bookmark', 'song']
    search_fields = [
        'bookmark__name',
        'song__book__name',
        'song__book__short_name',
        'song__title',
        'song__number',
        'song__sub_number',
    ]
