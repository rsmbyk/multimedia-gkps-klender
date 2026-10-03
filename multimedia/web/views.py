from django.conf import settings
from django.shortcuts import render

from multimedia.web.reading.views import HomeView


class IndexView(HomeView):
    """Site root: a maintenance notice while MAINTENANCE_MODE is on, else home."""

    def get(self, request, *args, **kwargs):
        if settings.MAINTENANCE_MODE:
            response = render(request, 'reading/maintenance.html')
            response.status_code = 503
            response['Retry-After'] = '3600'
            return response
        return super().get(request, *args, **kwargs)
