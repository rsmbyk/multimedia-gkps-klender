from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from multimedia.songs import models


class BookListView(TemplateView):
    template_name = 'songs/books/index.html'


class SongListView(TemplateView):
    template_name = 'songs/songs/index.html'

    def get_context_data(self, **kwargs):
        book = get_object_or_404(models.Book.objects.active(), id=kwargs['id'])
        return {'book': book}


class VerseListView(TemplateView):
    template_name = 'songs/verses/index.html'

    def get_context_data(self, **kwargs):
        song = get_object_or_404(
            models.Song.objects.active().filter(book__is_deleted=False), id=kwargs['id'])
        return {'song': song}

