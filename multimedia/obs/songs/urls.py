from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('dock', TemplateView.as_view(template_name='songs/dock/index.html'), name='obs-songs-dock'),
    path('source', TemplateView.as_view(template_name='songs/source/index.html'), name='obs-songs-source'),
]
