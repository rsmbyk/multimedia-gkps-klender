from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='web-songs-books'), name='web-root'),
    path('songs/', include('multimedia.web.songs.urls')),
]
