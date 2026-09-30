from django.urls import path

from multimedia.web.reading import views

urlpatterns = [
    path('', views.BookIndexView.as_view(), name='web-books'),
    path('book/<int:book_id>/', views.BookDetailView.as_view(), name='web-book'),
    path('<int:song_id>/', views.SongDetailView.as_view(), name='web-song'),
]
