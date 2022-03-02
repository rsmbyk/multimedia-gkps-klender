from django.urls import path

from multimedia.api.search import views

urlpatterns = [
    path('songs', views.SongSearchView.as_view(), name='api-search-songs'),
]
