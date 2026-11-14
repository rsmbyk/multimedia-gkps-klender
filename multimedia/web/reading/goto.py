"""The projector's Go To payloads (spec 136).

The projector page keeps no library: it reads three JSON payloads instead.

- ``index()`` is the panel's search data, fetched once when the page loads and held in
  page memory. It carries what the lookup matches on — book names, editions, chapter
  and verse counts, songbooks and song titles — and no verse text or lyric, so it
  cannot paint anything by itself.
- ``chapter()`` is what a chosen passage paints: one chapter in both editions, so a
  verse step inside it is local and the TB/SIM flip needs no request.
- ``song()`` is what a chosen song paints: every bait's screens and the bait ranges.

Nothing here is cached: each response is ``no-store``, because the page's freshness is
the page's own load.
"""

from collections import defaultdict

from django.db.models import Count
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models
from multimedia.web.reading.views import _line_pairs

EDITIONS = ('TB', 'SIM')


def _respond(payload):
    """A JSON response small enough for the index's byte budget and never cached.

    ``JsonResponse`` serialises with ``json.dumps``' default separators, which add
    roughly a third to the payload; the index is measured in bytes, so they are pinned.
    """
    response = JsonResponse(
        payload, json_dumps_params={'ensure_ascii': False, 'separators': (',', ':')})
    response['Cache-Control'] = 'no-store'
    return response


def _edition_code(translation):
    return (translation.version.abbreviation or translation.version.name or '').upper()


def index(request):
    """Every book with its editions' chapter/verse counts, the songbooks and the songs."""
    # ``[chapter, verse count]`` pairs rather than a positional list: a chapter number is
    # data, and a book whose chapters do not start at 1 must still describe itself.
    counts = defaultdict(list)
    rows = (bible_models.Verse.objects
            .values('book_translation_id', 'chapter')
            .annotate(total=Count('pk'))
            .order_by('book_translation_id', 'chapter'))
    for row in rows:
        counts[row['book_translation_id']].append([row['chapter'], row['total']])

    books = []
    translations = (bible_models.BookTranslation.objects
                    .select_related('version')
                    .order_by('pk'))
    by_book = defaultdict(list)
    for translation in translations:
        code = _edition_code(translation)
        if code not in EDITIONS:
            continue
        by_book[translation.book_id].append({
            'v': code,
            'name': translation.translation,
            'abbr': translation.abbreviation or '',
            'verses': counts.get(translation.pk, []),
        })
    for book in bible_models.Book.objects.order_by('pk'):
        editions = by_book.get(book.pk, [])
        if editions:
            books.append({'id': book.pk, 'name': book.name, 'editions': editions})

    songbooks = [{'id': book.pk, 'name': book.name, 'short_name': book.short_name or '',
                  'is_hymn_book': bool(book.is_hymn_book)}
                 for book in song_models.Book.objects.active().order_by('pk')]
    # One array per song — [id, songbook id, number, sub-number, title]. The index is a
    # byte budget (SC-005) and a row is repeated once per song, so the keys would cost
    # more than the data they name.
    songs = [[song.pk, song.book_id,
              song.number if song.number is not None else '',
              song.sub_number or '', song.title or '']
             for song in (song_models.Song.objects.active()
                          .filter(book__is_deleted=False).order_by('pk'))]
    return _respond({'schema': 1, 'books': books, 'songbooks': songbooks, 'songs': songs})


def chapter(request, book_id, chapter):
    """One chapter in both editions; ``404`` when no edition holds it."""
    editions = {}
    translations = (bible_models.BookTranslation.objects
                    .filter(book_id=book_id)
                    .select_related('version')
                    .order_by('pk'))
    for translation in translations:
        code = _edition_code(translation)
        if code not in EDITIONS or code in editions:
            continue
        rows = list(bible_models.Verse.objects
                    .filter(book_translation=translation, chapter=chapter)
                    .order_by('verse')
                    .values('verse', 'title', 'text'))
        if not rows:
            continue
        editions[code] = {
            'name': translation.translation,
            'verses': [{'n': row['verse'], 'title': row['title'] or '',
                        'text': row['text']} for row in rows],
        }
    if not editions:
        raise Http404('No such chapter')
    preferred = editions.get('TB') or editions[next(iter(editions))]
    return _respond({'schema': 1, 'book_id': int(book_id), 'chapter': int(chapter),
                     'label': f"{preferred['name']} {chapter}", 'editions': editions})


def _song_label(song):
    if song.book.is_hymn_book:
        label = f'{song.book.short_name or song.book.name} {song.number or ""}'
        label += (song.sub_number or '').upper()
        return (label + ' ' + song.title) if song.title else label
    return (song.title or '') + ' · ' + song.book.name


def song(request, song_id):
    """One song's screens and bait ranges, grouped exactly as the projector paints them."""
    chosen = get_object_or_404(
        song_models.Song.objects.active().filter(book__is_deleted=False).select_related('book'),
        pk=song_id)
    screens, baits = [], []
    for verse in chosen.verse_set.filter(is_deleted=False).order_by('number'):
        start = len(screens)
        groups = _line_pairs(verse.lyric)
        for split, lines in enumerate(groups, 1):
            screens.append({'blank': False, 'header': '', 'lines': lines,
                            'bait': verse.number, 'split': split,
                            'split_total': len(groups)})
        screens.append({'blank': True, 'header': '', 'lines': [],
                        'bait': verse.number, 'bait_rest': True})
        baits.append({'number': verse.number, 'start': start, 'end': len(screens) - 1})
    return _respond({'schema': 1, 'id': chosen.pk, 'label': _song_label(chosen),
                     'screens': screens, 'baits': baits})
