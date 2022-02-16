from rest_framework import routers


class OptionalTrailingSlashRouter(routers.DefaultRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.trailing_slash = '/?'
