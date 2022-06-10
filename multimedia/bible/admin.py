from django.contrib import admin

from multimedia.bible import models

admin.site.register(models.Language)
admin.site.register(models.Version)
admin.site.register(models.Book)


@admin.register(models.BookTranslation)
class BookTranslationAdmin(admin.ModelAdmin):
    search_fields = ('translation',)
    list_filter = ('version',)


@admin.register(models.Verse)
class VerseAdmin(admin.ModelAdmin):
    autocomplete_fields = ('book_translation',)
    search_fields = ('title', 'text')
    list_filter = ('book_translation__version', 'book_translation__book', 'chapter')
