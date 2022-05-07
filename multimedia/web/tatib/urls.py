from django.urls import path
from django.views.generic import RedirectView

from multimedia.web.tatib import views

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='web-tatib-tatibs'), name='web-tatib-root'),
    path('tatibs', views.TatibListView.as_view(), name='web-tatib-tatibs'),
    path('tatibs/<int:id>', views.TatibItemListView.as_view(), name='web-tatib-items'),
]
