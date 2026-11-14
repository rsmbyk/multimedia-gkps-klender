from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from multimedia.api.bookmarks import serializers, filters
from multimedia.bookmarks import models


class SongBookmarkViewSet(viewsets.ModelViewSet):
    queryset = models.SongBookmark.objects.all()
    serializer_class = serializers.SongBookmarkSerializer
    filterset_class = filters.SongBookmarkFilterSet
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('name',)


class SongBookmarkItemViewSet(viewsets.ModelViewSet):
    queryset = models.SongBookmarkItem.objects.filter(
        song__is_deleted=False, song__book__is_deleted=False)
    serializer_class = serializers.SongBookmarkItemSerializer
    filterset_class = filters.SongBookmarkItemFilterSet

    @action(methods=['POST'], detail=False, url_name='reorder')
    def reorder(self, request):
        serializer = serializers.SongBookmarkReorderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        for item in serializer.validated_data['items']:
            bookmark_item = models.SongBookmarkItem.objects.get(id=item['item'].id)
            bookmark_item.order_number = item['order_number']
            bookmark_item.save()
        return Response(serializer.data)
