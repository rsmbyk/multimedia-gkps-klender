from django.urls import path

from multimedia.obs.songs import views

urlpatterns = [
    path('dock', views.dock),
    path('source', views.source),
]
