from django.views.generic import TemplateView


class ManageRootView(TemplateView):
    """Editor landing page (content management)."""

    template_name = 'index.html'
