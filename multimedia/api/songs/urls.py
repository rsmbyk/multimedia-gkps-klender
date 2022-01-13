from django.urls import path, include

from multimedia.api.songs import views

urlpatterns = [
    path('', views.songs_root, name='songs-root'),
    path('books', views.BookList.as_view(), name='book-list'),
    path('books/<int:pk>', views.BookDetail.as_view(), name='book-detail'),
    path('songs', views.SongList.as_view(), name='song-list'),
    path('songs/<int:pk>', views.SongDetail.as_view(), name='song-detail'),
    path('verses', views.VerseList.as_view(), name='verse-list'),
    path('verses/<int:pk>', views.VerseDetail.as_view(), name='verse-detail'),
]
