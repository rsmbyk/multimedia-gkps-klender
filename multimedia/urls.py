"""multimedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from multimedia.web.reading import views as reading_views
from multimedia.web.reading import offline as offline_views

urlpatterns = [
    path('service-worker.js', offline_views.service_worker, name='offline-worker'),
    path('offline/manifest/', offline_views.manifest, name='offline-manifest'),
    path('offline/chunk/<str:kind>/<int:pk>/', offline_views.chunk, name='offline-chunk'),
    path('offline/projector-shell/', offline_views.projector_shell, name='offline-projector-shell'),
    path('admin/', admin.site.urls),
    path('api/', include('multimedia.api.urls')),
    # The new service projector (spec 006, slice 4). A path of its own under /obs/,
    # beside the OBS routes rather than inside them: the current dock, its sources
    # and its pages keep serving the current data untouched.
    path('obs/service/<int:service_id>/', reading_views.service_projector,
         name='web-service-projector'),
    path('obs/service/<int:service_id>/lookup/', reading_views.projector_lookup,
         name='web-service-projector-lookup'),
    path('obs/service/<int:service_id>/detour/', reading_views.projector_detour,
         name='web-service-projector-detour'),
    path('obs/', include('multimedia.obs.urls')),
    path('', include('multimedia.web.urls')),
]
