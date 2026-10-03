from django.urls import include, path
from django.views.generic import RedirectView

from multimedia.web import views
from multimedia.web.reading import views as reading_views

urlpatterns = [
    # Site root: a maintenance notice while MAINTENANCE_MODE is on, else the home.
    path('', views.IndexView.as_view(), name='web-index'),
    # Search-first home; a temporary URL while maintenance is on.
    path('home/', views.HomeView.as_view(), name='web-home'),
    # Full-corpus search across Alkitab, Kidung, and Tata Ibadah.
    path('search/', reading_views.SearchView.as_view(), name='web-search'),

    # Alkitab reading.
    path('bible/', reading_views.BibleView.as_view(), name='web-bible'),
    path('bible/<int:book_id>/', reading_views.BibleView.as_view(), name='web-bible-book'),
    path('bible/<int:book_id>/<int:chapter>/', reading_views.BibleView.as_view(), name='web-bible-chapter'),

    # Kidung reading.
    path('songs/', include('multimedia.web.reading.urls')),

    # Tata Ibadah reading.
    path('tatib/', reading_views.TatibView.as_view(), name='web-tatib'),
    path('tatib/<int:service_id>/', reading_views.TatibView.as_view(), name='web-tatib-service'),

    # Content editor, moved off the public paths.
    path('manage/', include('multimedia.web.manage.urls')),

    # Legacy editor paths -> /manage/ equivalents.
    path('songs/books', RedirectView.as_view(pattern_name='web-songs-books', permanent=True)),
    path('songs/books/<int:id>', RedirectView.as_view(pattern_name='web-songs-songs', permanent=True)),
    path('songs/songs/<int:id>', RedirectView.as_view(pattern_name='web-songs-verses', permanent=True)),
]
