from django.urls import include, path

urlpatterns = [
    path('songs/', include('multimedia.obs.songs.urls'))
]
