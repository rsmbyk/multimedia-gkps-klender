from django.urls import path, include

from multimedia.api import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('songs/', include('multimedia.api.songs.urls')),
    path('bookmarks/', include('multimedia.api.bookmarks.urls')),
]
