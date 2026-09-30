from django.urls import include, path

from multimedia.web.manage import views

urlpatterns = [
    path('', views.ManageRootView.as_view(), name='web-root'),
    path('songs/', include('multimedia.web.songs.urls')),
    path('tatib/', include('multimedia.web.tatib.urls')),
]
