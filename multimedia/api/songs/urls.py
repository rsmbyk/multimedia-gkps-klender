from multimedia.api.songs import views
from multimedia.api import routers

router = routers.OptionalTrailingSlashRouter(trailing_slash=False)
router.register('books', views.BookViewSet, basename='book')
router.register('songs', views.SongViewSet, basename='song')
router.register('verses', views.VerseViewSet, basename='verse')

urlpatterns = router.urls
