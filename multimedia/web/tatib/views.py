from django.views.generic import TemplateView

from multimedia.tatib import models


class TatibListView(TemplateView):
    template_name = 'tatib/tatibs/index.html'


class TatibItemListView(TemplateView):
    template_name = 'tatib/items/index.html'

    def get_context_data(self, **kwargs):
        return {'tatib': models.TataIbadah.objects.get(id=kwargs['id'])}
