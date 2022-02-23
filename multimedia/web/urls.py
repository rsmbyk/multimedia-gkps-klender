from django.urls import path, include

urlpatterns = [
    path('songs/', include('multimedia.web.songs.urls')),
]
