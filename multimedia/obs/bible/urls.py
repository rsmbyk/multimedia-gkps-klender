from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('dock', TemplateView.as_view(template_name='bible/dock/index.html'), name='obs-bible-dock'),
    path('source', TemplateView.as_view(template_name='bible/source/index.html'), name='obs-bible-source'),
]
