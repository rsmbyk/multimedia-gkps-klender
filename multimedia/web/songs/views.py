from django.views.generic import TemplateView

from multimedia.songs import models


class BookListView(TemplateView):
    template_name = 'songs/books/index.html'


class SongListView(TemplateView):
    template_name = 'songs/songs/index.html'

    def get_context_data(self, **kwargs):
        return {'book': models.Book.objects.get(id=kwargs['id'])}


class VerseListView(TemplateView):
    template_name = 'songs/verses/index.html'

    def get_context_data(self, **kwargs):
        return {'song': models.Song.objects.get(id=kwargs['id'])}

