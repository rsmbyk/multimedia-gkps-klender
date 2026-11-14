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
from django.urls import path, re_path, include

from multimedia import retirement
from multimedia.web.reading import views as reading_views
from multimedia.web.reading import goto as goto_views

urlpatterns = [
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
    # The projector's Go To payloads (spec 136): the page-memory index, and the
    # chapter or song a selection fetches.
    path('projector/goto/index/', goto_views.index, name='web-projector-goto-index'),
    path('projector/goto/chapter/<int:book_id>/<int:chapter>/', goto_views.chapter,
         name='web-projector-goto-chapter'),
    path('projector/goto/song/<int:song_id>/', goto_views.song,
         name='web-projector-goto-song'),
    # The operator dock and the OBS caption overlay (spec 119).
    path('obs/dock', reading_views.obs_dock, name='web-obs-dock'),
    path('obs/source/overlay', reading_views.obs_overlay, name='web-obs-overlay'),
    # spec 193 — where an old OBS source lands: transparent, one watermark note.
    # A live surface that outlives the retirement, so it is registered here beside
    # /obs/dock, not in multimedia/obs/, and next release does not delete it.
    path('obs/blank', reading_views.obs_blank, name='web-obs-blank'),
    # spec 193 — the old version, reachable for one release. One root route, so
    # every retired address has an /archive/ twin; the view answers one 302 to
    # successor(). Delete this route and multimedia/retirement.py next release.
    re_path(r'^archive(?:/(?P<rest>.*))?$', retirement.archive, name='web-archive'),
    path('obs/', include('multimedia.obs.urls')),
    path('', include('multimedia.web.urls')),
]
