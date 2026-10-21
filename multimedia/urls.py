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
    # The service projector (specs 006, 091, 119). One page, /projector, outside the
    # legacy /obs/ routes: the dock and the overlay carry the state; ?service=<id>
    # adopts that service on load as an act of projection.
    path('projector', reading_views.service_projector,
         name='web-projector'),
    path('projector/lookup/', reading_views.projector_lookup,
         name='web-projector-lookup'),
    path('projector/detour/', reading_views.projector_detour,
         name='web-projector-detour'),
    # The operator dock and the OBS caption overlay (spec 119).
    path('obs/dock', reading_views.obs_dock, name='web-obs-dock'),
    path('obs/source/overlay', reading_views.obs_overlay, name='web-obs-overlay'),
    path('obs/', include('multimedia.obs.urls')),
    path('', include('multimedia.web.urls')),
]
