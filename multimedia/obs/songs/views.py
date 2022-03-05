from django.shortcuts import render


def dock(request, **kwargs):
    return render(request, 'songs/dock/index.html')


def source(request, **kwargs):
    return render(request, 'songs/source/index.html')
