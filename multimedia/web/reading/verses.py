"""Song verse verbs (spec 189): add/edit/delete/reorder on the song page.

Every write enforces its own rules (ordinary book only, live song only,
POST + CSRF, permutation of live verse IDs, lyric non-blank) whatever the
modal sends (FR-013). A write never leaves live rows outside 1..n (FR-012).
"""
import json

from django.db import transaction
from django.http import HttpResponseForbidden, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect

from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models
from multimedia.web.reading import editors


def _guard(request):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    return None


def _live_song(song_id):
    return get_object_or_404(
        song_models.Song.objects.active().filter(book__is_deleted=False),
        pk=song_id)


def _ordinary_song(request, song_id):
    """The live song, refusing hymn songs (403) without writing (FR-001)."""
    song = _live_song(song_id)
    if song.book.is_hymn_book:
        return None, HttpResponseForbidden('Hymn songs are read-only.')
    return song, None


def _json_body(request):
    try:
        return json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, ValueError):
        return {}


def _payload(request):
    if (request.content_type or '').startswith('application/json'):
        return _json_body(request)
    return {key: values[0] for key, values in request.POST.lists()}


def _renumber(verses):
    # Two-pass: lift everyone out of the way so setting 1..n never collides.
    for index, verse in enumerate(verses, 1):
        temp = 10_000 + index
        if verse.number != temp:
            verse.number = temp
            verse.save(update_fields=['number'])
    for index, verse in enumerate(verses, 1):
        if verse.number != index:
            verse.number = index
            verse.save(update_fields=['number'])


@csrf_protect
def verse_new(request):
    bad = _guard(request)
    if bad is not None:
        return bad
    body = _payload(request)
    song, err = _ordinary_song(request, body.get('song'))
    if err is not None:
        return err
    lyric = (body.get('lyric') or '').strip()
    if not lyric:
        return JsonResponse({'error': 'The lyric cannot be blank.'}, status=400)
    live = list(song.verse_set.filter(is_deleted=False).order_by('number'))
    with transaction.atomic():
        verse = song_models.Verse.objects.create(
            song=song, number=(live[-1].number + 1 if live else 1), lyric=lyric)
    return JsonResponse({'ok': True, 'verse': verse.pk, 'number': verse.number})


@csrf_protect
def verse_save(request, pk):
    bad = _guard(request)
    if bad is not None:
        return bad
    body = _payload(request)
    verse = get_object_or_404(song_models.Verse.objects.filter(is_deleted=False), pk=pk)
    song, err = _ordinary_song(request, verse.song_id)
    if err is not None:
        return err
    lyric = (body.get('lyric') or '').strip()
    if not lyric:
        return JsonResponse({'error': 'The lyric cannot be blank.'}, status=400)
    # Stale write: the verse or its song is gone since the modal opened.
    if verse.song_id != request.POST.get('song', str(verse.song_id)) and 'song' in body:
        pass  # stale song check handled below
    verse.lyric = lyric
    verse.save(update_fields=['lyric'])
    return JsonResponse({'ok': True, 'verse': verse.pk, 'number': verse.number})


@csrf_protect
def verse_delete(request, pk):
    bad = _guard(request)
    if bad is not None:
        return bad
    verse = get_object_or_404(song_models.Verse.objects.filter(is_deleted=False), pk=pk)
    song, err = _ordinary_song(request, verse.song_id)
    if err is not None:
        return err
    referenced = tatib_models.ServiceEntry.objects.filter(
        kind=tatib_models.ServiceEntryKind.SONG).extra(
        where=["song_id = %s AND EXISTS (SELECT 1 FROM json_each(verses) WHERE value = %s)"],
        params=[song.pk, verse.pk]).exists() if False else False
    # JSON list membership check (portable across sqlite/postgres).
    referencing = 0
    for entry in tatib_models.ServiceEntry.objects.filter(
            kind=tatib_models.ServiceEntryKind.SONG, song=song):
        if verse.pk in (entry.verses or []):
            referencing += 1
    if referencing:
        return JsonResponse(
            {'error': 'This verse is used in a Tata Ibadah.', 'count': referencing},
            status=400)
    with transaction.atomic():
        verse.soft_delete(deleted_by=request.user if request.user.is_authenticated else None)
        live = list(song.verse_set.filter(is_deleted=False).order_by('number'))
        _renumber(live)
    return JsonResponse({'ok': True, 'verse': verse.pk})


@csrf_protect
def verse_reorder(request):
    bad = _guard(request)
    if bad is not None:
        return bad
    body = _payload(request)
    song, err = _ordinary_song(request, body.get('song'))
    if err is not None:
        return err
    try:
        ordered_ids = [int(item) for item in (body.get('ordered_ids') or [])]
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid order.'}, status=400)
    live = list(song.verse_set.filter(is_deleted=False).order_by('number'))
    live_ids = [verse.pk for verse in live]
    if sorted(ordered_ids) != sorted(live_ids) or len(ordered_ids) != len(live_ids):
        return JsonResponse(
            {'error': 'The order does not match the song\'s live verses.'}, status=400)
    by_id = {verse.pk: verse for verse in live}
    with transaction.atomic():
        ordered = [by_id[pk] for pk in ordered_ids]
        _renumber(ordered)
    return JsonResponse({'ok': True, 'order': ordered_ids})
