from django.urls import path, include

from multimedia.web import views

urlpatterns = [
    path('', views.WebRootView.as_view(), name='web-root'),
    path('songs/', include('multimedia.web.songs.urls')),
    path('tatib/', include('multimedia.web.tatib.urls')),
]
