from django.urls import path
from django.views.generic import TemplateView

from multimedia.web.songs import views

urlpatterns = [
    path('books', TemplateView.as_view(template_name='songs/books/index.html')),
    path('books/<int:id>', TemplateView.as_view(template_name='songs/songs/index.html')),
    path('songs/<int:id>', views.VerseListView.as_view()),
]
