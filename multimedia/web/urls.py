from django.urls import include, path
from django.views.generic import RedirectView

from multimedia.web import views
from multimedia.web.reading import views as reading_views
from multimedia.web.reading import verses as verse_views

urlpatterns = [
    # Site root: a maintenance notice while MAINTENANCE_MODE is on, else the home.
    path('', views.IndexView.as_view(), name='web-index'),
    # Search-first home; a temporary URL while maintenance is on.
    path('home/', views.HomeView.as_view(), name='web-home'),
    # Full-corpus search across Alkitab, Kidung, and Tata Ibadah.
    path('search', reading_views.SearchView.as_view(), name='web-search'),
    path('search/', RedirectView.as_view(url='/search', query_string=True), name='web-search-legacy'),

    # Alkitab reading.
    path('bible/', reading_views.BibleView.as_view(), name='web-bible'),
    path('bible/<int:book_id>/', reading_views.BibleView.as_view(), name='web-bible-book'),
    path('bible/<int:book_id>/<int:chapter>/', reading_views.BibleView.as_view(), name='web-bible-chapter'),

    # Kidung reading.
    path('songs/', include('multimedia.web.reading.urls')),

    # Tata Ibadah reading.
    path('tatib/', reading_views.TatibView.as_view(), name='web-tatib'),
    path('tatib/<int:service_id>/', reading_views.TatibView.as_view(), name='web-tatib-service'),
    path('tatib/<int:service_id>/generate/', reading_views.tatib_generate, name='web-tatib-generate'),
    path('tatib/<int:service_id>/copy-as-template/', reading_views.tatib_copy_as_template,
         name='web-tatib-copy'),
    path('media-library/', reading_views.media_library, name='web-media-library'),
    path('media-library/references/', reading_views.media_references, name='web-media-references'),
    path('media-library/cloud/status/', reading_views.media_cloud_status, name='web-media-cloud-status'),
    path('media-library/cloud/manifest/', reading_views.media_manifest, name='web-media-manifest'),
    path('media-library/cloud/cleanup/', reading_views.media_cleanup, name='web-media-cleanup'),
    path('media-library/cloud/<str:sha>/download/', reading_views.media_download, name='web-media-download'),
    path('media-library/cloud/<str:sha>/complete/', reading_views.media_complete, name='web-media-complete'),
    path('media-library/cloud/<str:sha>/<str:operation>/', reading_views.media_share, name='web-media-share'),

    # Service entries (spec 006, slice 2): the content pane's own editor. These come
    # BEFORE the generic editor patterns below: 'editor/<str:kind>/new/' would otherwise
    # swallow 'editor/entry/new/' with kind='entry', and the old view would 404.
    path('editor/entry/new/', reading_views.entry_form, name='web-entry-new'),
    path('editor/media/register/', reading_views.media_register, name='web-media-register'),
    path('editor/entry/validate/', reading_views.entry_validate, name='web-entry-validate'),
    path('editor/entry/new/save/', reading_views.entry_save, name='web-entry-save-new'),
    path('editor/entry/<int:pk>/edit/', reading_views.entry_form, name='web-entry-edit'),
    path('editor/entry/<int:pk>/save/', reading_views.entry_save, name='web-entry-save'),
    path('editor/entry/<int:pk>/screen-breaks/', reading_views.entry_screen_breaks,
         name='web-entry-screen-breaks'),
    path('editor/entry/<int:pk>/delete/', reading_views.entry_delete, name='web-entry-delete'),
    path('editor/entry/reorder/', reading_views.entry_reorder, name='web-entry-reorder'),
    path('editor/entry/songs/', reading_views.entry_song_options,
         name='web-entry-song-options'),
    path('editor/entry/song/<int:pk>/verses/', reading_views.entry_song_verses,
         name='web-entry-song-verses'),
    path('editor/verse/new/save/', verse_views.verse_new, name='web-verse-new'),
    path('editor/verse/<int:pk>/save/', verse_views.verse_save, name='web-verse-save'),
    path('editor/verse/<int:pk>/delete/', verse_views.verse_delete, name='web-verse-delete'),
    path('editor/verse/reorder/', verse_views.verse_reorder, name='web-verse-reorder'),
    path('editor/entry/chapter/<int:pk>/<int:chapter>/', reading_views.entry_chapter_verses,
         name='web-entry-chapter-verses'),

    # Legacy TataIbadahItem editing (spec 007, slice 1). Keep the old rows and API intact.
    path('editor/item/<int:pk>/edit/', reading_views.old_item_form, name='web-old-item-edit'),
    path('editor/item/<int:pk>/save/', reading_views.old_item_save, name='web-old-item-save'),
    path('editor/item/<int:pk>/delete/', reading_views.old_item_delete, name='web-old-item-delete'),

    # Sidebar editors (spec 005).
    path('editor/<str:kind>/new/', reading_views.editor_form, name='web-editor-new'),
    path('editor/<str:kind>/new/save/', reading_views.editor_save, name='web-editor-save-new'),
    path('editor/<str:kind>/<int:pk>/', reading_views.editor_form, name='web-editor-edit'),
    path('editor/<str:kind>/<int:pk>/save/', reading_views.editor_save, name='web-editor-save'),

    # Content editor, moved off the public paths.
    path('manage/', include('multimedia.web.manage.urls')),

    # Legacy editor paths -> /manage/ equivalents.
    path('songs/books', RedirectView.as_view(pattern_name='web-songs-books', permanent=True)),
    path('songs/books/<int:id>', RedirectView.as_view(pattern_name='web-songs-songs', permanent=True)),
    path('songs/songs/<int:id>', RedirectView.as_view(pattern_name='web-songs-verses', permanent=True)),
]
