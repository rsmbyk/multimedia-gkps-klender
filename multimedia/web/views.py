from django.conf import settings
from django.shortcuts import render
from django.views.generic import ListView

from multimedia.songs import models
from multimedia.songs.search import search_songs


class HomeView(ListView):
    """Public home: songbook browsing plus song search."""

    template_name = 'reading/home.html'
    context_object_name = 'books'

    def get_queryset(self):
        return models.Book.objects.select_related('lang').order_by('-is_hymn_book', 'name', 'lang')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['query'] = query
        context['results'] = search_songs(query) if query else None
        return context


class IndexView(HomeView):
    """Site root: a maintenance notice while MAINTENANCE_MODE is on, else home."""

    def get(self, request, *args, **kwargs):
        if settings.MAINTENANCE_MODE:
            response = render(request, 'reading/maintenance.html')
            response.status_code = 503
            response['Retry-After'] = '3600'
            return response
        return super().get(request, *args, **kwargs)
