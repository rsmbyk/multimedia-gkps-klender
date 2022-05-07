from multimedia.api import routers
from multimedia.api.tatib import views

router = routers.OptionalTrailingSlashRouter(trailing_slash=False)

router.register('tatibs', views.TataIbadahViewSet)
router.register('items', views.TataIbadahItemViewSet)

urlpatterns = router.urls
