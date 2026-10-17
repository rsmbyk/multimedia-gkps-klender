"""Cross-corpus public search (spec 004).

Two matchers live here, deliberately apart:

- ``search_page()`` serves the public search page (specs 104 and 105). It matches
  only the listed content fields: a verse's text or title, a song's title or
  lyrics, a service's name, a row's title, and a text-entry body; book rows,
  songbook rows, references, dates, and section labels never match. Spec 105
  replaced its ranking ladder with the query grammar: tokens, quoted phrases,
  ``-`` exclusions, soft AND, coverage, then query order.
- ``search()`` is the projector Go To's free-text fallback. It keeps the original
  behaviour -- book names and references, songbook references, meta scores -- and
  must not change with the page (owner: "do not touch anything on goto").

``search()`` returns a :class:`SearchResults`; each row is a plain dict with
``kind``, ``title``, ``meta``, ``excerpt``, ``target``, and ``score``. Views
turn ``target`` into URLs; templates render the rest.
"""

import re
import unicodedata
from bisect import bisect_left
from dataclasses import dataclass

from django.db.models import Prefetch, Q

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models

GROUP_ORDER = ('bible', 'songs', 'tatib')

NOTICE_EXCLUSION_ONLY = (
    'Nothing to search \u2014 an exclusion like \u201c-Israel\u201d needs at least one other word.'
)
NOTICE_NO_WORDS = 'Nothing to search \u2014 add at least one word.'

MONTHS_SHORT = ('Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des')
MONTHS_LONG = ('Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember')


def format_date_short(value):
    """The mockup's fmtDate: ``23 Agu 2026``."""
    return f'{value.day} {MONTHS_SHORT[value.month - 1]} {value.year}'


def format_date_long(value):
    """Full month date header: ``23 Agustus 2026``."""
    return f'{value.day} {MONTHS_LONG[value.month - 1]} {value.year}'


def format_month_long(value):
    """The mockup's long month head: ``Agustus 2026``."""
    return f'{MONTHS_LONG[value.month - 1]} {value.year}'


def normalize(text):
    """Case- and diacritic-folded comparison form."""
    text = unicodedata.normalize('NFD', str(text or ''))
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r'\s+', ' ', text).strip().casefold()


@dataclass(frozen=True)
class QueryToken:
    """One query token: a bare word or a quoted phrase, maybe excluded."""

    words: tuple
    text: str
    excluded: bool = False
    phrase: bool = False

    @property
    def display(self):
        """The typed spelling, words joined by single spaces."""
        return ' '.join(self.words)

    def canonical(self):
        body = f"'{self.display}'" if self.phrase else self.display
        return f'-{body}' if self.excluded else body


def _is_word_char(char):
    return char.isalnum() or unicodedata.combining(char)


def parse_query(query):
    """Split a typed query into tokens and rebuild its canonical form (spec 105).

    Outside quotes ``\"`` opens or closes a phrase, a ``-`` before a word or a
    quote excludes the next token, and every other symbol separates words.
    Inside quotes only ``\"`` closes; every other symbol, the dash included,
    separates the phrase's words. Case and spelling stay as typed. Returns
    ``(tokens, canonical, notice)``.
    """
    tokens = []
    excluded = False
    index, length = 0, len(query)
    while index < length:
        char = query[index]
        if char == '"':
            index += 1
            words, word = [], []
            while index < length and query[index] != '"':
                current = query[index]
                if _is_word_char(current):
                    word.append(current)
                else:
                    if word:
                        words.append(''.join(word))
                        word = []
                index += 1
            if word:
                words.append(''.join(word))
            if index < length:
                index += 1                      # the closing quote
            if words:
                tokens.append(QueryToken(tuple(words), normalize(' '.join(words)),
                                         excluded=excluded, phrase=True))
            excluded = False
            continue
        if (char == '-' and index + 1 < length
                and (_is_word_char(query[index + 1]) or query[index + 1] == '"')):
            excluded = True
            index += 1
            continue
        if _is_word_char(char):
            word = []
            while index < length and _is_word_char(query[index]):
                word.append(query[index])
                index += 1
            bare = ''.join(word)
            tokens.append(QueryToken((bare,), normalize(bare), excluded=excluded))
            excluded = False
            continue
        excluded = False
        index += 1

    canonical = ' '.join(token.canonical() for token in tokens)
    if not tokens:
        notice = NOTICE_NO_WORDS
    elif not any(not token.excluded for token in tokens):
        notice = NOTICE_EXCLUSION_ONLY
    else:
        notice = None
    return tokens, canonical, notice


class SearchResults:
    """Query, validity, and rows grouped in display order."""

    def __init__(self, query='', valid=True):
        self.query = query
        self.valid = valid
        self.canonical = ''
        self.notice = ''
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


def bible_book_index():
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
            'by_version': {(t.version.abbreviation or '').upper(): t for t in translations},
            'display': primary.translation if primary else book.name,
            'other': translations[1].translation if len(translations) > 1 else '',
            'aliases': ([book.name] + [t.translation for t in translations]
                        + [t.abbreviation for t in translations if t.abbreviation]),
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


def _song_hits(phrase, words, raw, songbooks):
    hits = []
    for book in songbooks:
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
                | Q(book__short_name__icontains=raw)
                | Q(verse__is_deleted=False, verse__lyric__icontains=raw))
    if raw.isdigit():
        criteria |= Q(number__icontains=raw)
    if len(words) > 1:
        all_words = Q()
        for word in words:
            all_words &= (Q(title__icontains=word) | Q(book__name__icontains=word)
                          | Q(book__short_name__icontains=word)
                          | Q(verse__is_deleted=False, verse__lyric__icontains=word))
        criteria |= all_words
    active_songs = song_models.Song.objects.active().filter(book__is_deleted=False)
    ids = set(active_songs.filter(criteria).values_list('id', flat=True))
    match = _SONG_REF_RE.match(normalize(raw))
    if match:
        ref_book = next((book for book in songbooks
                         if normalize(book.short_name or '') == match.group('name')
                         or normalize(book.name) == match.group('name')), None)
        if ref_book is not None:
            reference_songs = active_songs.filter(
                book=ref_book, number=int(match.group('number')))
            if match.group('sub'):
                reference_songs = reference_songs.filter(
                    sub_number__iexact=match.group('sub'))
            ids.update(reference_songs.values_list('id', flat=True))
    if not ids:
        return _ranked_rows(hits, phrase)
    queryset = (active_songs.filter(pk__in=ids).select_related('book')
                .prefetch_related(Prefetch(
                    'verse_set',
                    queryset=song_models.Verse.objects.active().order_by('number'))))
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
    phrase = normalize(raw)
    if not phrase:
        result.valid = False
        return result
    words = phrase.split(' ')
    books = bible_book_index()
    songbooks = list(song_models.Book.objects.active().order_by('id'))
    result.groups['bible'] = _bible_hits(phrase, words, raw, books)
    result.groups['songs'] = _song_hits(phrase, words, raw, songbooks)
    result.groups['tatib'] = _tatib_hits(phrase, words, raw)
    return result


# --- The public search page (spec 104) -------------------------------------------------
#
# Built beside ``search()`` rather than inside it: the projector Go To reads
# ``search()``'s reference rows and meta scores, and the owner froze that path.
# These helpers therefore never touch the legacy functions above.


def _occurrences(text, token):
    """Every match offset of a folded token inside folded text (substrings count)."""
    start = text.find(token.text)
    while start >= 0:
        yield start
        start = text.find(token.text, start + 1)


def _order_score(fields, tokens):
    """The longest run of matched tokens that keeps the query's order in one field.

    Offsets must increase; matches need not be adjacent, and a token that occurs
    several times may take any occurrence. Computed as a longest increasing
    subsequence over the occurrences, so the best configuration wins rather than
    the first one a greedy walk would take.
    """
    best = 0
    for text in fields:
        events = []
        for index, token in enumerate(tokens):
            for position in _occurrences(text, token):
                events.append((position, -index))
        if not events:
            continue
        events.sort()                 # equal offsets: the higher token index first
        tails = []
        for _position, negative in events:
            index = -negative
            place = bisect_left(tails, index)
            if place == len(tails):
                tails.append(index)
            else:
                tails[place] = index
        best = max(best, len(tails))
    return best


def _page_metrics(entry, tokens):
    """(coverage, order) for the row, or None when an excluded token matches it.

    Coverage counts distinct include tokens, once each however many fields or
    occurrences they hit; order is the best in-order run across the fields.
    """
    fields = (entry['lookup_title'], entry['lookup_body'])
    matched = []
    for token in tokens:
        if token.excluded:
            if any(token.text in field for field in fields):
                return None
            continue
        if any(token.text in field for field in fields):
            matched.append(token)
    if not matched:
        return 0, 0
    return len(matched), _order_score(fields, matched)


def _page_excerpt(body, tokens):
    """The window around the first matched include token in the body."""
    folded = normalize(body)
    if folded:
        for token in tokens:
            if not token.excluded and token.text in folded:
                return _excerpt(body, token.text)
    return _excerpt(body, '')


def _page_row(hit, tokens):
    return {
        'kind': hit['kind'],
        'title': hit['title'],
        'meta': hit['meta'],
        'excerpt': _page_excerpt(hit['body'], tokens),
        'target': hit['target'],
        'score': hit['coverage'],
    }


def _page_ranked_rows(hits, tokens):
    """Coverage first, then the order score, then the existing title tie-break."""
    hits.sort(key=lambda hit: (-hit['coverage'], -hit['order'], normalize(hit['title'])))
    return [_page_row(hit, tokens) for hit in hits]


def _page_bible_hits(tokens, books):
    """Verse text and title only (spec 104); never a book or reference row."""
    include = [token for token in tokens if not token.excluded]
    if not include:
        return []
    criteria = Q()
    for token in include:
        for word in token.words:
            criteria |= Q(text__icontains=word) | Q(title__icontains=word)
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
        metrics = _page_metrics(entry, tokens)
        if metrics is None:
            continue
        coverage, order = metrics
        if not coverage:
            continue
        entry['coverage'], entry['order'] = coverage, order
        key = (verse.book_translation.book_id, verse.chapter, verse.verse)
        prior = seen.get(key)
        if (prior is None or (coverage, order) > (prior['coverage'], prior['order'])
                or ((coverage, order) == (prior['coverage'], prior['order'])
                    and abbreviation == info['version'])):
            seen[key] = entry
    return _page_ranked_rows(list(seen.values()), tokens)


def _page_song_hits(tokens):
    """Song title and live lyrics only (spec 104); never a songbook or number row."""
    include = [token for token in tokens if not token.excluded]
    if not include:
        return []
    criteria = Q()
    for token in include:
        for word in token.words:
            criteria |= (Q(title__icontains=word)
                         | Q(verse__is_deleted=False, verse__lyric__icontains=word))
    active_songs = song_models.Song.objects.active().filter(book__is_deleted=False)
    ids = set(active_songs.filter(criteria).values_list('id', flat=True))
    if not ids:
        return []
    queryset = (active_songs.filter(pk__in=ids).select_related('book')
                .prefetch_related(Prefetch(
                    'verse_set',
                    queryset=song_models.Verse.objects.active().order_by('number'))))
    hits = []
    for song in queryset:
        citation = song.book_number if song.number else song.book.name
        entry = _entry(
            kind='song',
            title=song.title or citation,
            lookup_title=song.title or '',
            meta=citation,
            body=chr(10).join(verse.lyric for verse in song.verse_set.all()),
            target={'song_id': song.pk})
        metrics = _page_metrics(entry, tokens)
        if metrics is None:
            continue
        coverage, order = metrics
        if not coverage:
            continue
        entry['coverage'], entry['order'] = coverage, order
        hits.append(entry)
    return _page_ranked_rows(hits, tokens)


def _page_service_public_rows(service):
    """The service's public rows: legacy text rows and non-break entries."""
    legacy = [row for row in service.tataibadahitem_set.all()
              if row.item_type == tatib_models.TataIbadahItemType.TEXT]
    entries = [entry for entry in service.service_entries.all()
               if entry.kind != tatib_models.ServiceEntryKind.SECTION_BREAK]
    return legacy, entries


def _page_tatib_rows(service):
    """The matchable rows in the service's shared order.

    Legacy rows and entries interleave by ``order_number`` (legacy first on a tie),
    exactly as the contents pane orders them. Only legacy text rows and text entries
    carry a matchable title or body.
    """
    legacy, entries = _page_service_public_rows(service)
    rows = [(row.order_number, 0, row.pk, 'legacy', row) for row in legacy]
    rows += [(entry.order_number, 1, entry.pk, 'entry', entry) for entry in entries
             if entry.kind == tatib_models.ServiceEntryKind.TEXT]
    return [(kind, row) for _number, _kind, _pk, kind, row in sorted(rows)]


def _page_tatib_hits(tokens):
    """Service name, legacy text-row title/body, entry title, text-entry body."""
    include = [token for token in tokens if not token.excluded]
    if not include:
        return []
    text_item = Q(tataibadahitem__item_type=tatib_models.TataIbadahItemType.TEXT)
    text_entry = Q(service_entries__kind=tatib_models.ServiceEntryKind.TEXT)
    criteria = Q()
    for token in include:
        for word in token.words:
            criteria |= (
                Q(name__icontains=word)
                | Q(text_item, tataibadahitem__title__icontains=word)
                | Q(text_item, tataibadahitem__text__icontains=word)
                | Q(service_entries__title__icontains=word)
                | Q(text_entry, service_entries__text__icontains=word))
    services = (tatib_models.TataIbadah.objects.filter(is_active=True)
                .filter(criteria)
                .prefetch_related('tataibadahitem_set', 'service_entries')
                .distinct())
    hits = []
    for service in services:
        legacy, entries = _page_service_public_rows(service)
        if not legacy and not entries:
            continue
        meta = format_date_short(service.date) if service.date else 'Template'
        entry = _entry(kind='service', title=service.name, meta=meta,
                       target={'tatib_id': service.pk, 'item_order': None})
        metrics = _page_metrics(entry, tokens)
        if metrics is not None:
            coverage, order = metrics
            if coverage:
                entry['coverage'], entry['order'] = coverage, order
                hits.append(entry)
        for number, (kind, row) in enumerate(_page_tatib_rows(service), start=1):
            section = f'{service.name} · Section {number}'
            item_entry = _entry(
                kind='item', title=row.title or section, lookup_title=row.title or '',
                meta=section, body=row.text,
                target={'tatib_id': service.pk,
                        'item_order': row.order_number if kind == 'legacy' else f'e{row.pk}'})
            item_metrics = _page_metrics(item_entry, tokens)
            if item_metrics is None:
                continue
            item_coverage, item_order = item_metrics
            if item_coverage:
                item_entry['coverage'], item_entry['order'] = item_coverage, item_order
                hits.append(item_entry)
    return _page_ranked_rows(hits, tokens)


def search_page(query):
    """The public search page's matcher (specs 104 and 105); see the module docstring."""
    raw = str(query or '').strip()
    result = SearchResults(query=raw)
    if not raw:
        result.valid = False
        return result
    tokens, canonical, notice = parse_query(raw)
    result.canonical = canonical
    result.notice = notice or ''
    include = [token for token in tokens if not token.excluded]
    if not include:
        # An exclusion-only or symbols-only query lists nothing; the notice says why.
        return result
    books = bible_book_index()
    result.groups['bible'] = _page_bible_hits(tokens, books)
    result.groups['songs'] = _page_song_hits(tokens)
    result.groups['tatib'] = _page_tatib_hits(tokens)
    return result
