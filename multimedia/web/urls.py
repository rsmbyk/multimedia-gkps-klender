from django.urls import include, path
from django.views.generic import RedirectView

from multimedia.web import views

urlpatterns = [
    # Public reading experience (top level).
    path('', views.HomeView.as_view(), name='web-home'),
    path('songs/', include('multimedia.web.reading.urls')),

    # Content editor, moved off the public paths.
    path('manage/', include('multimedia.web.manage.urls')),

    # Legacy editor paths -> /manage/ equivalents.
    path('songs/books', RedirectView.as_view(pattern_name='web-songs-books', permanent=True)),
    path('songs/books/<int:id>', RedirectView.as_view(pattern_name='web-songs-songs', permanent=True)),
    path('songs/songs/<int:id>', RedirectView.as_view(pattern_name='web-songs-verses', permanent=True)),
]
