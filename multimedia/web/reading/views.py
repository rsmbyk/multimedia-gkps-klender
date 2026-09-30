from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from multimedia.songs import models


class BookIndexView(ListView):
    """All hymn books."""

    template_name = 'reading/book_index.html'
    context_object_name = 'books'

    def get_queryset(self):
        return models.Book.objects.select_related('lang').order_by('-is_hymn_book', 'name', 'lang')


class BookDetailView(DetailView):
    """Songs within one hymn book."""

    template_name = 'reading/book.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Book.objects.select_related('lang'), id=self.kwargs['book_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['songs'] = self.object.song_set.order_by('number', 'sub_number', 'title')
        return context


class SongDetailView(DetailView):
    """A single song and its lyrics."""

    template_name = 'reading/song.html'
    context_object_name = 'song'

    def get_object(self, queryset=None):
        return get_object_or_404(models.Song.objects.select_related('book'), id=self.kwargs['song_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['verses'] = self.object.verse_set.order_by('number')
        siblings = list(
            models.Song.objects.filter(book=self.object.book).order_by('number', 'sub_number', 'title')
        )
        index = siblings.index(self.object)
        context['previous_song'] = siblings[index - 1] if index > 0 else None
        context['next_song'] = siblings[index + 1] if index < len(siblings) - 1 else None
        return context
