from django.contrib.postgres import search
from rest_framework.generics import ListAPIView

from multimedia.api.search import pagination, serializers
from multimedia.songs import models


class SongSearchView(ListAPIView):
    queryset = models.Verse.objects.active().filter(
        song__is_deleted=False, song__book__is_deleted=False)
    serializer_class = serializers.SongSearchResultSerializer
    pagination_class = pagination.SearchPagination

    def filter_queryset(self, queryset):
        serializer = serializers.SearchSerializer(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)

        search_query = serializer.data['q']
        vector = search.SearchVector('lyric')
        query = search.SearchQuery(search_query, search_type='phrase')
        rank = search.SearchRank(vector, query)
        search_result = queryset \
            .annotate(search=vector, rank=rank) \
            .filter(search=query) \
            .order_by('-rank')
        return search_result
