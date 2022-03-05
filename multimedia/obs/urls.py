from django.urls import include, path

urlpatterns = [
    path('bible/', include('multimedia.obs.bible.urls')),
    path('songs/', include('multimedia.obs.songs.urls')),
]
