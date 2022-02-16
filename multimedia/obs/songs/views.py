from django.shortcuts import render

from multimedia.songs.models import Book


def dock(request, **kwargs):
    books = Book.objects.all()
    return render(request, 'dock/dock.html', context={'books': books})


def source(request, **kwargs):
    return render(request, '')
