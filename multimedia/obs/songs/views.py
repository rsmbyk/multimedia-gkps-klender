from django.shortcuts import render


def dock(request, **kwargs):
    return render(request, 'dock/index.html')


def source(request, **kwargs):
    return render(request, 'source/index.html')
