from django.views.generic import TemplateView

from multimedia.songs import models


class VerseListView(TemplateView):
    template_name = 'songs/verses/index.html'

    def get_context_data(self, **kwargs):
        return {'song': models.Song.objects.get(id=kwargs['id'])}

