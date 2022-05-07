from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('dock', TemplateView.as_view(template_name='tatib/dock/index.html'), name='obs-tatib-dock'),
    path('source', TemplateView.as_view(template_name='tatib/source/index.html'), name='obs-tatib-source'),
]
