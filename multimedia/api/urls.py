from django.urls import path, include

from multimedia.api import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('bible/', include('multimedia.api.bible.urls')),
    path('songs/', include('multimedia.api.songs.urls')),
    path('bookmarks/', include('multimedia.api.bookmarks.urls')),
    path('search/', include('multimedia.api.search.urls')),
]
