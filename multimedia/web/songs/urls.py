from django.urls import path

from multimedia.web.songs import views

urlpatterns = [
    path('books', views.BookListView.as_view(), name='web-books'),
    path('books/<int:id>', views.SongListView.as_view(), name='web-songs'),
    path('songs/<int:id>', views.VerseListView.as_view(), name='web-verses'),
]
