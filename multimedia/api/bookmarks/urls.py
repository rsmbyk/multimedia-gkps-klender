from multimedia.api.bookmarks import views
from multimedia.api import routers

router = routers.OptionalTrailingSlashRouter(trailing_slash=False)
router.register('songs/bookmarks', views.SongBookmarkViewSet)
router.register('songs/items', views.SongBookmarkItemViewSet)

urlpatterns = router.urls
