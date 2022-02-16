from multimedia.api.songs import views
from multimedia.api import routers

router = routers.OptionalTrailingSlashRouter(trailing_slash=False)
router.register('books', views.BookViewSet)
router.register('songs', views.SongViewSet)
router.register('verses', views.VerseViewSet)

urlpatterns = router.urls
