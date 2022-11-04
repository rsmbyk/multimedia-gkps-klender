from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('source', TemplateView.as_view(template_name='project/source/index.html'), name='obs-project-source'),
]
