from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from multimedia.api.bookmarks import serializers, filters
from multimedia.bookmarks import models


class SongBookmarkViewSet(viewsets.ModelViewSet):
    queryset = models.SongBookmark.objects.all()
    serializer_class = serializers.SongBookmarkSerializer
    filterset_class = filters.SongBookmarkFilterSet
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('name',)


class SongBookmarkItemViewSet(viewsets.ModelViewSet):
    queryset = models.SongBookmarkItem.objects.all()
    serializer_class = serializers.SongBookmarkItemSerializer
    filterset_class = filters.SongBookmarkItemFilterSet
