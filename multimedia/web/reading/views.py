"""Public reading views (spec 004).

Server-rendered pages for the accepted mockup's shell: initial sidebar state,
the panel and second-list contents, and the reading stage. static/web/reading.js
owns the in-page transitions (open / mini / close, filters, theme, and the
search keeping its last result set).

URL map:
    /                                       maintenance (on) or the search-first home
    /home/                                  the search-first home (kept while maintenance is on)
    /search/?q=                             grouped results across Bible, Kidung, Tata Ibadah
    /bible/ /bible/<book>/ /bible/<book>/<chapter>/     Alkitab
    /songs/ /songs/book/<book>/ /songs/<song>/          Kidung
    /tatib/ /tatib/<service>/                           Tata Ibadah
"""

import re
from urllib.parse import quote

from django.db.models import Count
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models
from multimedia.web.reading import search as search_lib

TESTAMENTS = (('old', 'Perjanjian Lama'), ('new', 'Perjanjian Baru'))

SECTION_NAMES = {'alkitab': 'Alkitab', 'kidung': 'Kidung', 'tatib': 'Tata Ibadah'}

PANEL_META = {
    'alkitab': {'title': 'Books — Alkitab', 'label': 'Filter books',
                'placeholder': 'Filter books...', 'empty': 'No matching books.'},
    'kidung': {'title': 'Songbooks', 'label': 'Filter songbooks',
               'placeholder': 'Filter songbooks...', 'empty': 'No matching songbooks.'},
    'tatib': {'title': 'Tata Ibadah', 'label': 'Filter Tata Ibadah',
              'placeholder': 'Filter Tata Ibadah...', 'empty': 'No matching Tata Ibadah.'},
}

CH_META = {
    'alkitab': {'collapse': 'Close chapter list', 'empty': 'No matching songs.'},
    'kidung': {'collapse': 'Close song list', 'empty': 'No matching songs.'},
    'tatib': {'collapse': 'Close Tata Ibadah sections', 'empty': 'No matching sections.'},
}

SPEAKER_RE = re.compile(r'^\s*([LPJ][LPJ]?)\.\s+([\s\S]*)$')

SEARCH_GROUP_LABELS = (('bible', 'Alkitab'), ('songs', 'Kidung'), ('tatib', 'Tata Ibadah'))

DEFAULT_SHOWN = 8


def _shell(section, nav, ch, read_on, home_state, ch_mode='chapter'):
    """The state and copy every page's shell shares (pinned by spec 004)."""
    panel = PANEL_META[section]
    chmeta = CH_META[section]
    name = SECTION_NAMES[section]
    return {
        'section': section,
        'nav_state': nav,
        'ch_state': ch,
        'read_state': 'on' if read_on else 'off',
        'home_state': home_state,
        'ch_mode': ch_mode,
        'panel_title': panel['title'],
        'panel_filter_label': panel['label'],
        'panel_filter_placeholder': panel['placeholder'],
        'panel_empty_text': panel['empty'],
        'panel_collapse_label': (('Collapse ' if section == 'alkitab' else 'Close ') + name + ' panel')
            if nav == 'open' else f'Open {name} panel',
        'ch_collapse_label': chmeta['collapse'],
        'ch_empty_text': chmeta['empty'],
        'ch_filter_label': 'Filter sections' if section == 'tatib' else 'Filter songs',
        'ch_filter_placeholder': 'Filter sections...' if section == 'tatib' else 'Filter songs...',
        'show_song_filter': ch_mode == 'song' and section != 'alkitab',
        'show_song_sort': False,
    }


def _books_groups(selected_id=None):
    info_map = search_lib.bible_book_index()
    groups = []
    for testament, label in TESTAMENTS:
        rows = []
        for info in info_map.values():
            book = info['book']
            if book.testament != testament:
                continue
            rows.append({
                'id': book.pk,
                'display': info['display'],
                'other': info['other'],
                'abbr': book.name,
                'current': book.pk == selected_id,
            })
        groups.append({'testament': testament, 'label': label, 'books': rows})
    return groups


def _songbooks(selected_id=None):
    # Largest collections first: the accepted mockup's panel order (HAL, KJ,
    # PKJ, NKB, HARIAN, ANTIFON, AJAR) is exactly descending song count.
    books = (song_models.Book.objects.annotate(song_total=Count('song'))
             .order_by('-song_total', 'name', 'lang'))
    return [{'id': book.pk, 'name': book.name, 'short': book.short_name or '',
             'current': book.pk == selected_id} for book in books]


def _song_rows(book, current_id=None):
    rows = []
    for song in book.song_set.order_by('number', 'sub_number', 'title'):
        numbered = book.is_hymn_book and song.number is not None
        rows.append({
            'id': song.pk,
            'number_display': song.book_number if numbered else '',
            'title': song.title or '(untitled)',
            'current': song.pk == current_id,
        })
    return rows


def _tatib_groups(mode, selected_id=None):
    services = (tatib_models.TataIbadah.objects.filter(is_active=True)
                .filter(tataibadahitem__item_type=tatib_models.TataIbadahItemType.TEXT)
                .distinct())
    if mode == 'template':
        # Mirrors the mockup's Indonesian locale collation for these names:
        # case- and diacritic-folded, with the '|' separator ignored.
        templates = sorted(services.filter(date__isnull=True),
                           key=lambda service: search_lib.normalize(service.name).replace('|', ''))
        rows = [{'id': service.pk, 'name': service.name, 'date_display': '',
                 'current': service.pk == selected_id}
                for service in templates]
        return [{'label': 'Templates', 'key': '', 'services': rows}]
    groups = []
    current = None
    for service in services.filter(date__isnull=False).order_by('-date', '-created_at'):
        key = f'{service.date.year}-{service.date.month:02d}'
        if current is None or current['key'] != key:
            current = {'label': search_lib.format_month_long(service.date),
                       'key': key, 'services': []}
            groups.append(current)
        current['services'].append({
            'id': service.pk, 'name': service.name,
            'date_display': search_lib.format_date_short(service.date),
            'current': service.pk == selected_id,
        })
    return groups


def _bible_verses(translation, chapter, target=None):
    if translation is None or chapter is None:
        return []
    rows = []
    for verse in (bible_models.Verse.objects
                  .filter(book_translation=translation, chapter=chapter)
                  .order_by('verse')):
        rows.append({
            'n': verse.verse,
            'title': verse.title or '',
            'text': verse.text,
            'target': bool(target and target[0] <= verse.verse <= target[1]),
        })
    return rows


def _first_line(text):
    line = (text or '').split('\n')[0]
    line = SPEAKER_RE.sub(lambda match: match.group(2), line)
    return line.strip()


def _tatib_stage(service):
    items, toc = [], []
    text_count = 0
    for item in service.tataibadahitem_set.order_by('order_number'):
        anchor = item.order_number
        if item.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
            items.append({'eos': True, 'anchor': anchor, 'note': item.text})
            toc.append({'eos': True, 'anchor': anchor})
            continue
        text_count += 1
        paras = []
        for line in item.text.split('\n'):
            match = SPEAKER_RE.match(line)
            if match:
                paras.append({'speaker': match.group(1), 'text': match.group(2)})
            else:
                paras.append({'speaker': '', 'text': line})
        items.append({'eos': False, 'anchor': anchor, 'title': item.title, 'paras': paras})
        label = item.title or _first_line(item.text)
        if len(label) > 60:
            label = label[:60] + '…'
        toc.append({'eos': False, 'anchor': anchor, 'n': text_count,
                    'label': label or f'Section {text_count}',
                    'titled': bool(item.title),
                    'txt': f'{item.title} {item.text}'})
    return items, toc


def _search_row(row):
    target = row['target']
    kind = row['kind']
    if kind == 'book':
        url = reverse('web-bible-book', args=[target['book_id']])
    elif kind in ('chapter', 'reference', 'verse'):
        url = reverse('web-bible-chapter', args=[target['book_id'], target['chapter']])
        if target.get('verse'):
            url += f"?v={target['verse']}&to={target['end_verse']}"
    elif kind == 'song':
        url = reverse('web-song', args=[target['song_id']])
    elif kind == 'songbook':
        url = reverse('web-book', args=[target['book_id']])
    elif kind == 'service':
        url = reverse('web-tatib-service', args=[target['tatib_id']])
    elif kind == 'item':
        url = reverse('web-tatib-service', args=[target['tatib_id']])
        if target.get('item_order'):
            url += f"#ti-{target['item_order']}"
    else:  # pragma: no cover - defensive
        url = ''
    title = row['title']
    if len(title) > 105:
        title = title[:105] + '…'
    return {'url': url, 'title': title, 'meta': row['meta'], 'excerpt': row['excerpt']}


def _shown_counts(request):
    counts = {}
    for kind, _label in SEARCH_GROUP_LABELS:
        try:
            value = int(request.GET.get(kind, ''))
        except (TypeError, ValueError):
            value = DEFAULT_SHOWN
        counts[kind] = max(DEFAULT_SHOWN, value)
    return counts


def _search_groups(results, shown, base_path):
    groups = []
    for kind, label in SEARCH_GROUP_LABELS:
        rows = results[kind]
        if not rows:
            continue
        visible = rows[:shown[kind]]
        more_url = None
        if len(rows) > len(visible):
            counts = dict(shown)
            counts[kind] += DEFAULT_SHOWN
            query = '&'.join([f'q={quote(results.query)}'] +
                             [f'{key}={counts[key]}' for key, _ in SEARCH_GROUP_LABELS])
            more_url = f'{base_path}?{query}'
        groups.append({
            'kind': kind,
            'label': label,
            'count_text': f'{len(rows)} result' if len(rows) == 1 else f'{len(rows)} results',
            'rows': [_search_row(row) for row in visible],
            'more_url': more_url,
        })
    return groups


class HomeView(TemplateView):
    """Search-first home: the landing state with the books panel ready."""

    template_name = 'reading/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_shell('alkitab', 'closed', 'closed', False, 'landing'))
        context.update({
            'page_title': 'GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah',
            'books_groups': _books_groups(),
        })
        return context


class SearchView(TemplateView):
    """Grouped full-corpus results; a bad/missing query keeps the landing."""

    template_name = 'reading/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        query = request.GET.get('q', '').strip()
        has_param = 'q' in request.GET
        context.update(_shell('alkitab', 'closed', 'closed', False, 'landing'))
        context.update({
            'query': query,
            'books_groups': _books_groups(),
            'query_invalid': False,
            'result_groups': [],
        })
        if not has_param:
            context['page_title'] = 'GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah'
            return context
        results = search_lib.search(query)
        if not results.valid:
            context['query_invalid'] = True
            context['page_title'] = 'Search — GKPS Klender'
            return context
        context['home_state'] = 'results'
        context['page_title'] = f'Results for “{query}” — GKPS Klender'
        context['result_groups'] = _search_groups(results, _shown_counts(request), request.path)
        return context


class BibleView(TemplateView):
    """Alkitab: books panel, chapter tiles, and a chapter on the stage."""

    template_name = 'reading/bible.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = search_lib.bible_book_index()
        book_id = self.kwargs.get('book_id')
        chapter = self.kwargs.get('chapter')
        info = None
        if book_id is not None:
            info = books.get(book_id)
            if info is None:
                raise Http404('Unknown book')
        editions = {'tb': None, 'sim': None}
        if info:
            editions['tb'] = info['by_version'].get('TB')
            editions['sim'] = info['by_version'].get('SIM')
        requested = self.request.GET.get('ed', 'tb')
        if requested not in ('tb', 'sim'):
            requested = 'tb'
        target = None
        raw_v = self.request.GET.get('v', '')
        raw_to = self.request.GET.get('to', '')
        if raw_v.isdigit():
            start = int(raw_v)
            end = int(raw_to) if raw_to.isdigit() and int(raw_to) >= start else start
            target = (start, end)
        verses = {'tb': [], 'sim': []}
        read_on = False
        if chapter is not None:
            if not info or not 1 <= chapter <= info['book'].number_of_chapters:
                raise Http404('Unknown chapter')
            for key, translation in editions.items():
                verses[key] = _bible_verses(translation, chapter, target)
            if not verses['tb'] and not verses['sim']:
                raise Http404('No text for this chapter')
            if not verses[requested]:
                requested = 'tb' if verses['tb'] else 'sim'
            read_on = True

        def edition_url(edition):
            parts = [f'ed={edition}']
            if target:
                parts += [f'v={target[0]}', f'to={target[1]}']
            return '?' + '&'.join(parts)

        chapters = []
        if info:
            def text_chapters(translation):
                if translation is None:
                    return set()
                return set(bible_models.Verse.objects
                           .filter(book_translation=translation)
                           .values_list('chapter', flat=True))
            tb_chapters = text_chapters(editions['tb'])
            sim_chapters = text_chapters(editions['sim'])
            for number in range(1, info['book'].number_of_chapters + 1):
                chapters.append({'n': number, 'current': number == chapter,
                                 'has_text': number in tb_chapters,
                                 'has_sim': number in sim_chapters})
        context.update(_shell('alkitab', 'open', 'open' if info else 'closed',
                              read_on, 'reading' if read_on else 'landing'))
        if info and info['other']:
            ch_title = f"Chapters — {info['display']} ({info['other']})"
        elif info:
            ch_title = f"Chapters — {info['display']}"
        else:
            ch_title = 'Chapters'
        if read_on:
            page_title = f"{info['display']} {chapter} — GKPS Klender"
        elif info:
            page_title = f"{info['display']} — GKPS Klender"
        else:
            page_title = 'Alkitab — GKPS Klender'
        context.update({
            'page_title': page_title,
            'books_groups': _books_groups(book_id),
            'book_id': book_id,
            'book_display': info['display'] if info else '',
            'chapters': chapters,
            'ch_title': ch_title,
            'tb_verses': verses['tb'],
            'sim_verses': verses['sim'],
            'read_lang': requested,
            'read_kind': 'bible' if read_on else '',
            'read_show_lang': read_on,
            'read_name': info['display'] if info else '',
            'read_no': chapter or '',
            'has_sim': bool(verses['sim']),
            'lang_tb_url': edition_url('tb'),
            'lang_sim_url': edition_url('sim'),
        })
        return context


class BookIndexView(TemplateView):
    """Kidung root: songbooks beside the rail."""

    template_name = 'reading/book_index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(_shell('kidung', 'open', 'closed', False, 'landing', ch_mode='song'))
        context.update({
            'page_title': 'Kidung — GKPS Klender',
            'songbooks': _songbooks(),
        })
        return context


class BookDetailView(TemplateView):
    """One songbook: its songs fill the wide second pane."""

    template_name = 'reading/book.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = get_object_or_404(
            song_models.Book.objects.select_related('lang'), pk=self.kwargs['book_id'])
        context.update(_shell('kidung', 'open', 'open', False, 'landing', ch_mode='song'))
        context.update({
            'page_title': f'{book.name} — GKPS Klender',
            'songbooks': _songbooks(book.pk),
            'songs': _song_rows(book),
            'ch_title': f'Song list — {book.name}',
            'book_name': book.name,
        })
        return context


class SongDetailView(TemplateView):
    """A song on stage with its songbook list restored beside it."""

    template_name = 'reading/song.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = get_object_or_404(
            song_models.Song.objects.select_related('book'), pk=self.kwargs['song_id'])
        book = song.book
        if book.is_hymn_book and song.number is not None:
            citation = f'{book.name} {song.number}{song.sub_number.upper()}'
        else:
            citation = book.name
        verses = [verse.lyric for verse in song.verse_set.order_by('number')]
        context.update(_shell('kidung', 'open', 'open', True, 'reading', ch_mode='song'))
        context.update({
            'page_title': f'{citation} — GKPS Klender',
            'songbooks': _songbooks(book.pk),
            'songs': _song_rows(book, song.pk),
            'ch_title': f'Song list — {book.name}',
            'verses': verses,
            'read_kind': 'song',
            'read_eyebrow': citation,
            'read_name': song.title or citation,
            'read_no': '',
        })
        return context


class TatibView(TemplateView):
    """Tata Ibadah: services panel (dated / templates) and a service order."""

    template_name = 'reading/tatib.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_id = self.kwargs.get('service_id')
        service = None
        if service_id is not None:
            service = get_object_or_404(tatib_models.TataIbadah, pk=service_id, is_active=True)
        override = self.request.GET.get('mode', '')
        if override in ('dated', 'template'):
            mode = override
        elif service is not None:
            mode = 'dated' if service.date else 'template'
        else:
            mode = 'dated'
        items, toc = [], []
        if service is not None:
            items, toc = _tatib_stage(service)
        other_mode = 'dated' if mode == 'template' else 'template'
        context.update(_shell('tatib', 'open', 'open' if service else 'closed',
                              service is not None, 'reading' if service else 'landing',
                              ch_mode='song'))
        context.update({
            'page_title': f'{service.name} — GKPS Klender' if service else 'Tata Ibadah — GKPS Klender',
            'tatib_groups': _tatib_groups(mode, service.pk if service else None),
            'show_tatib_mode': True,
            'tatib_mode_url': f'?mode={other_mode}',
            'tatib_mode_pressed': 'true' if mode == 'template' else 'false',
            'tatib_mode_label': ('Show dated Tata Ibadah' if mode == 'template'
                                 else 'Show Tata Ibadah templates'),
            'service_id': service.pk if service else None,
            'toc_items': toc,
            'items': items,
            'read_kind': 'tatib' if service else '',
            'read_name': service.name if service else '',
            'read_no': '',
        })
        if service is not None:
            context['read_eyebrow'] = (search_lib.format_date_short(service.date)
                                       if service.date else 'Tata Ibadah')
        return context
