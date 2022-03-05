from multimedia.api import routers
from multimedia.api.bible import views

router = routers.OptionalTrailingSlashRouter(trailing_slash=False)
router.register('langs', views.LanguageViewSet)
router.register('versions', views.VersionViewSet)
router.register('books', views.BookViewSet)
router.register('translations', views.BookTranslationViewSet)
router.register('verses', views.VerseViewSet)

urlpatterns = router.urls
