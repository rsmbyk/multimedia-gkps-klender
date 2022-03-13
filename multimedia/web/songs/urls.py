from django.urls import path
from django.views.generic import RedirectView

from multimedia.web.songs import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='web-books'), name='web-songs-root'),
    path('books', views.BookListView.as_view(), name='web-books'),
    path('books/<int:id>', views.SongListView.as_view(), name='web-songs'),
    path('songs/<int:id>', views.VerseListView.as_view(), name='web-verses'),
]
