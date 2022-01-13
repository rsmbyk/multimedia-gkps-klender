from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.reverse import reverse

from multimedia.api.songs import serializers
from multimedia.songs import models


@api_view(['GET'])
def songs_root(request, format=None):
    return Response({
        'books': reverse('book-list', request=request, format=format),
        'songs': reverse('song-list', request=request, format=format),
        'verses': reverse('verse-list', request=request, format=format),
    })


class BookList(ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class SongList(ListCreateAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer


class SongDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Song.objects.all()
    serializer_class = serializers.SongSerializer


class VerseList(ListCreateAPIView):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.VerseSerializer


class VerseDetail(RetrieveUpdateDestroyAPIView):
    queryset = models.Verse.objects.all()
    serializer_class = serializers.VerseSerializer
