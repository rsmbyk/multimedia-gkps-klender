"""Cross-corpus public search (spec 004).

Searches the whole reading corpus in one query:

- Bible - book names and aliases, ``Book chapter:verse`` references, and
  verse text (both translations, one hit per verse).
- Kidung - songbook names and abbreviations, song titles, and lyrics.
- Tata Ibadah - service names and public contents. End-of-section notes are
  never indexed.

Semantics mirror the accepted mockup: normalized (case- and diacritic-folded)
phrase matching, the same ranking ladder, and the same reference resolution -
``Kidung Jemaat 120`` and ``KJ 120`` resolve to the same song at the same
rank.

``search()`` returns a :class:`SearchResults`; each row is a plain dict with
``kind``, ``title``, ``meta``, ``excerpt``, ``target``, and ``score``. Views
turn ``target`` into URLs; templates render the rest.
"""

import re
import unicodedata

from django.db.models import Q

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models

MIN_KEYWORDS = 3

GROUP_ORDER = ('bible', 'songs', 'tatib')

MONTHS_SHORT = ('Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des')
MONTHS_LONG = ('Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')


def format_date_short(value):
    """The mockup's fmtDate: ``23 Agu 2026``."""
    return f'{value.day} {MONTHS_SHORT[value.month - 1]} {value.year}'


def format_month_long(value):
    """The mockup's long month head: ``Agustus 2026``."""
    return f'{MONTHS_LONG[value.month - 1]} {value.year}'


def normalize(text):
    """Case- and diacritic-folded comparison form."""
    text = unicodedata.normalize('NFD', str(text or ''))
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r'\s+', ' ', text).strip().casefold()


def keyword_length(text):
    """Count letters and digits (the mockup's ``[\\p{L}\\p{N}]``)."""
    return sum(1 for ch in str(text or '') if ch.isalnum())


def is_short_query(text):
    return keyword_length(text) < MIN_KEYWORDS


class SearchResults:
    """Query, validity, and rows grouped in display order."""

    def __init__(self, query='', valid=True):
        self.query = query
        self.valid = valid
        self.groups = {key: [] for key in GROUP_ORDER}

    def __getitem__(self, key):
        return self.groups[key]

    @property
    def total(self):
        return sum(len(rows) for rows in self.groups.values())


def _excerpt(body, phrase):
    """A window around the match, mockup-style (44 before, 172 wide)."""
    if not body:
        return ''
    text = re.sub(r'\s+', ' ', body).strip()
    position = normalize(text).find(phrase)
    start = 0 if position < 0 else max(0, position - 44)
    end = start + 172
    return ('\u2026' if start else '') + text[start:end] + ('\u2026' if end < len(text) else '')


def _entry(*, kind, title, target, meta='', lookup_title=None, lookup_meta='', refs=(), body=''):
    return {
        'kind': kind,
        'title': title,
        'meta': meta,
        'target': target,
        'body': body,
        'score': 0,
        'lookup_title': normalize(title if lookup_title is None else lookup_title),
        'lookup_meta': normalize(lookup_meta),
        'lookup_meta_exact': normalize(meta),
        'refs': [normalize(ref) for ref in refs],
        'lookup_body': normalize(body),
    }


def _match_score(entry, phrase, words):
    """The mockup's ladder: exact, prefix, substring, meta, body, all words."""
    title = entry['lookup_title']
    meta = entry['lookup_meta']
    exact_meta = entry['lookup_meta_exact']
    body = entry['lookup_body']
    if title == phrase or meta == phrase or exact_meta == phrase or phrase in entry['refs']:
        return 200
    if title.startswith(phrase):
        return 120
    if phrase in title:
        return 95
    if phrase in meta:
        return 70
    if phrase in body:
        return 35
    if len(words) > 1:
        combined = ' '.join((title, meta, exact_meta, body))
        if all(word in combined for word in words):
            return 16
    return 0


def _row(hit, phrase):
    return {
        'kind': hit['kind'],
        'title': hit['title'],
        'meta': hit['meta'],
        'excerpt': _excerpt(hit['body'], phrase),
        'target': hit['target'],
        'score': hit['score'],
    }


def _ranked_rows(hits, phrase):
    hits.sort(key=lambda hit: (-hit['score'], normalize(hit['title'])))
    return [_row(hit, phrase) for hit in hits]


_BIBLE_REF_RE = re.compile(
    r'^(?P<name>.+?)\s+(?P<chapter>\d{1,3})'
    r'(?:\s*:\s*(?P<verse>\d{1,3})(?:\s*[-\u2013]\s*(?P<end>\d{1,3}))?)?$')

_SONG_REF_RE = re.compile(r'^(?P<name>.+?)\s+(?P<number>\d{1,3})(?P<sub>[a-z])?$')


def _bible_book_map():
    """book pk -> display/other names, aliases, and the primary version."""
    books = {}
    queryset = (bible_models.Book.objects
                .prefetch_related('booktranslation_set__version')
                .order_by('id'))
    for book in queryset:
        translations = sorted(
            book.booktranslation_set.all(),
            key=lambda t: ((t.version.abbreviation or '').upper() != 'TB', t.pk))
        primary = translations[0] if translations else None
        books[book.pk] = {
            'book': book,
            'display': primary.translation if primary else book.name,
            'other': translations[1].translation if len(translations) > 1 else '',
            'aliases': [book.name] + [t.translation for t in translations],
            'version': (primary.version.abbreviation or primary.version.name).upper()
                       if primary else '',
        }
    return books


def _bible_reference(query, books):
    """A resolved ``Book chapter[:verse[-end]]`` reference row, or None."""
    match = _BIBLE_REF_RE.match(query.strip())
    if not match:
        return None
    name = normalize(match.group('name').rstrip('.'))
    info = next((candidate for candidate in books.values()
                 if any(normalize(alias) == name for alias in candidate['aliases'])), None)
    if not info:
        return None
    chapter = int(match.group('chapter'))
    verse = int(match.group('verse')) if match.group('verse') else None
    end = int(match.group('end')) if match.group('end') else verse
    if end is not None and end < verse:
        return None
    verses = bible_models.Verse.objects.filter(
        book_translation__book=info['book'], chapter=chapter)
    if verse is None:
        if not verses.exists():
            return None
    else:
        present = set(verses.filter(verse__gte=verse, verse__lte=end)
                      .values_list('verse', flat=True))
        if len(present) < end - verse + 1:
            return None
    citation = f"{info['display']} {chapter}"
    body = ''
    if verse is not None:
        citation += f':{verse}' + (f'\u2013{end}' if end != verse else '')
        rows = list(verses.filter(verse=verse).select_related('book_translation__version'))
        chosen = next((row for row in rows
                       if (row.book_translation.version.abbreviation or '').upper() == 'TB'), None)
        chosen = chosen or (rows[0] if rows else None)
        body = chosen.text if chosen else ''
    return _entry(
        kind='reference' if verse is not None else 'chapter',
        title=citation,
        meta=f"Alkitab reference \u00b7 {info['version']}",
        body=body,
        target={'book_id': info['book'].pk, 'chapter': chapter,
                'verse': verse, 'end_verse': end})


def _bible_hits(phrase, words, raw, books):
    hits = []
    for info in books.values():
        entry = _entry(
            kind='book', title=info['display'],
            lookup_title=' '.join(info['aliases']),
            meta=(f"{info['other']} \u00b7 Alkitab" if info['other'] else 'Alkitab'),
            target={'book_id': info['book'].pk, 'chapter': None,
                    'verse': None, 'end_verse': None})
        score = _match_score(entry, phrase, words)
        if score:
            entry['score'] = score
            hits.append(entry)
    criteria = Q(text__icontains=raw) | Q(title__icontains=raw)
    if len(words) > 1:
        all_words = Q()
        for word in words:
            all_words &= (Q(text__icontains=word) | Q(title__icontains=word))
        criteria |= all_words
    seen = {}
    candidates = (bible_models.Verse.objects.filter(criteria)
                  .select_related('book_translation__version', 'book_translation__book'))
    for verse in candidates:
        info = books[verse.book_translation.book_id]
        abbreviation = (verse.book_translation.version.abbreviation or '').upper()
        entry = _entry(
            kind='verse',
            title=f"{info['display']} {verse.chapter}:{verse.verse}",
            lookup_title=verse.title or '',
            meta=abbreviation + (f' \u00b7 {verse.title}' if verse.title else ''),
            body=verse.text,
            target={'book_id': info['book'].pk, 'chapter': verse.chapter,
                    'verse': verse.verse, 'end_verse': verse.verse})
        score = _match_score(entry, phrase, words)
        if not score:
            continue
        entry['score'] = score
        key = (verse.book_translation.book_id, verse.chapter, verse.verse)
        prior = seen.get(key)
        if (prior is None or score > prior['score']
                or (score == prior['score'] and abbreviation == info['version'])):
            seen[key] = entry
    hits.extend(seen.values())
    rows = _ranked_rows(hits, phrase)
    reference = _bible_reference(raw, books)
    if reference is not None:
        reference['score'] = 1000
        rows.insert(0, _row(reference, phrase))
    return rows


def _song_hits(phrase, words, raw, hymn_books):
    hits = []
    for book in hymn_books:
        entry = _entry(
            kind='songbook', title=book.name,
            lookup_title=f'{book.name} {book.short_name}',
            meta=f'Songbook \u00b7 {book.short_name}',
            target={'book_id': book.pk})
        score = _match_score(entry, phrase, words)
        if score:
            entry['score'] = score
            hits.append(entry)
    criteria = (Q(title__icontains=raw) | Q(book__name__icontains=raw)
                | Q(book__short_name__icontains=raw) | Q(verse__lyric__icontains=raw))
    if raw.isdigit():
        criteria |= Q(number__icontains=raw)
    if len(words) > 1:
        all_words = Q()
        for word in words:
            all_words &= (Q(title__icontains=word) | Q(book__name__icontains=word)
                          | Q(book__short_name__icontains=word)
                          | Q(verse__lyric__icontains=word))
        criteria |= all_words
    ids = set(song_models.Song.objects.filter(book__is_hymn_book=True)
              .filter(criteria).values_list('id', flat=True))
    match = _SONG_REF_RE.match(normalize(raw))
    if match:
        ref_book = next((book for book in hymn_books
                         if normalize(book.short_name or '') == match.group('name')
                         or normalize(book.name) == match.group('name')), None)
        if ref_book is not None:
            reference_songs = song_models.Song.objects.filter(
                book=ref_book, number=int(match.group('number')))
            if match.group('sub'):
                reference_songs = reference_songs.filter(
                    sub_number__iexact=match.group('sub'))
            ids.update(reference_songs.values_list('id', flat=True))
    if not ids:
        return _ranked_rows(hits, phrase)
    queryset = (song_models.Song.objects.filter(pk__in=ids)
                .select_related('book').prefetch_related('verse_set'))
    for song in queryset:
        citation = song.book_number if song.number else song.book.name
        entry = _entry(
            kind='song',
            title=song.title or citation,
            meta=citation,
            lookup_meta=f'{citation} {song.book.name} {song.number}' if song.number else '',
            refs=[citation, f'{song.book.name} {song.number}'] if song.number else [],
            body='\n'.join(verse.lyric for verse in song.verse_set.all()),
            target={'song_id': song.pk})
        score = _match_score(entry, phrase, words)
        if score:
            entry['score'] = score
            hits.append(entry)
    return _ranked_rows(hits, phrase)


def _tatib_hits(phrase, words, raw):
    item_match = Q(tataibadahitem__item_type=0, tataibadahitem__title__icontains=raw) \
        | Q(tataibadahitem__item_type=0, tataibadahitem__text__icontains=raw)
    criteria = Q(name__icontains=raw) | item_match
    if len(words) > 1:
        all_words = Q()
        for word in words:
            all_words &= (Q(name__icontains=word)
                          | Q(tataibadahitem__item_type=0,
                              tataibadahitem__title__icontains=word)
                          | Q(tataibadahitem__item_type=0,
                              tataibadahitem__text__icontains=word))
        criteria |= all_words
    services = (tatib_models.TataIbadah.objects.filter(is_active=True)
                .filter(criteria).prefetch_related('tataibadahitem_set').distinct())
    hits = []
    for service in services:
        items = [item for item in service.tataibadahitem_set.all()
                 if item.item_type == tatib_models.TataIbadahItemType.TEXT]
        if not items:
            continue
        meta = format_date_short(service.date) if service.date else 'Template'
        entry = _entry(kind='service', title=service.name, meta=meta,
                       target={'tatib_id': service.pk, 'item_order': None})
        score = _match_score(entry, phrase, words)
        if score:
            entry['score'] = score
            hits.append(entry)
        for number, item in enumerate(items, start=1):
            section = f'{service.name} \u00b7 Section {number}'
            item_entry = _entry(
                kind='item', title=item.title or section,
                lookup_title=item.title or '', meta=section, body=item.text,
                target={'tatib_id': service.pk, 'item_order': item.order_number})
            item_score = _match_score(item_entry, phrase, words)
            if item_score:
                item_entry['score'] = item_score
                hits.append(item_entry)
    return _ranked_rows(hits, phrase)


def search(query):
    """Search the whole corpus; see the module docstring for semantics."""
    raw = str(query or '').strip()
    result = SearchResults(query=raw)
    if is_short_query(raw):
        result.valid = False
        return result
    phrase = normalize(raw)
    if not phrase:
        result.valid = False
        return result
    words = phrase.split(' ')
    books = _bible_book_map()
    hymn_books = list(song_models.Book.objects.filter(is_hymn_book=True).order_by('id'))
    result.groups['bible'] = _bible_hits(phrase, words, raw, books)
    result.groups['songs'] = _song_hits(phrase, words, raw, hymn_books)
    result.groups['tatib'] = _tatib_hits(phrase, words, raw)
    return result
