from django.contrib import admin
from django.utils import timezone

from multimedia.songs import models


class SoftDeleteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_deleted', 'deleted_at', 'deleted_by')
    list_filter = ('is_deleted',)
    readonly_fields = ('is_deleted', 'deleted_at', 'deleted_by')

    def get_deleted_objects(self, objs, request):
        # Soft deletion affects only the selected row; protected references remain intact.
        objects = list(objs)
        return ([str(obj) for obj in objects],
                {self.opts.verbose_name_plural: len(objects)}, set(), [])

    def delete_model(self, request, obj):
        obj.soft_delete(deleted_by=request.user)

    def delete_queryset(self, request, queryset):
        queryset.active().update(
            is_deleted=True, deleted_at=timezone.now(), deleted_by=request.user)


@admin.register(models.Song)
class SongAdmin(SoftDeleteAdmin):
    list_filter = ['is_deleted', 'book']
    search_fields = [
        'book__name',
        'book__short_name',
        'title',
        'number',
        'sub_number',
    ]


@admin.register(models.Verse)
class VerseAdmin(SoftDeleteAdmin):
    list_filter = ['is_deleted', 'song__book']
    autocomplete_fields = ['song']
    search_fields = [
        'song__book__name',
        'song__book__short_name',
        'song__title',
        'song__number',
        'lyric',
    ]


class BookAdmin(SoftDeleteAdmin):
    list_filter = ['is_deleted', 'is_hymn_book']
    search_fields = ['name', 'short_name']


admin.site.register(models.Book, BookAdmin)
