from django.views.generic import TemplateView


class WebRootView(TemplateView):
    template_name = 'index.html'
