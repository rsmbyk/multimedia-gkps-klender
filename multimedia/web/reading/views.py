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

import json
import re
from urllib.parse import quote

from django.db.models import Count, F, Q
from django.http import (Http404, HttpResponseForbidden, HttpResponseNotAllowed,
                         JsonResponse)
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import TemplateView

from multimedia.bible import models as bible_models
from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models
from multimedia.web.reading import editors
from multimedia.web.reading import entries as entry_forms
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


# ---------- sidebar editors (spec 005) ----------
# GET renders the modal's form (empty, or prefilled when editing); POST validates
# and saves, answering JSON on success and the re-rendered form on error. Both are
# server-authoritative: the rules hold even when the modal is bypassed.


def _editor_fragment_context(kind, form, pk):
    kwargs = {'kind': kind, 'pk': pk} if pk else {'kind': kind}
    return {
        'form': form,
        'kind': kind,
        'title': editors.form_title(kind, pk),
        'save_url': reverse('web-editor-save' if pk else 'web-editor-save-new', kwargs=kwargs),
        'target_id': pk or '',
    }


def editor_form(request, kind, pk=None):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    form, _target = editors.build_form(kind, request, pk)
    if form is None:
        raise Http404('Not editable.')
    return render(request, 'reading/_editor_form.html',
                  _editor_fragment_context(kind, form, pk))


def editor_save(request, kind, pk=None):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    form, target = editors.build_form(kind, request, pk, data=request.POST)
    if form is None:
        raise Http404('Not editable.')
    if not form.is_valid():
        return render(request, 'reading/_editor_form.html',
                      _editor_fragment_context(kind, form, pk), status=400)
    saved = editors.save_form(kind, form, target)
    return JsonResponse({'ok': True, 'id': saved.pk})


def entry_form(request, kind=None, pk=None):
    """The modal's form fragment: one per kind, or the existing entry's own."""
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if pk is not None:
        entry = get_object_or_404(tatib_models.ServiceEntry, pk=pk)
        kind = entry_forms.kind_name(entry.kind)
        form = entry_forms.build_entry_form(kind, instance=entry)
        tatib = entry.tatib
    else:
        kind = request.GET.get('kind')          # the new form names its kind in the query
        tatib = get_object_or_404(tatib_models.TataIbadah, pk=request.GET.get('tatib'))
        form = entry_forms.build_entry_form(kind, tatib=tatib)
    if form is None:
        raise Http404('Unknown kind.')
    return render(request, 'reading/_entry_form.html', {
        'form': form, 'kind': kind, 'entry': None if pk is None else entry,
        'title': entry_forms.entry_title(kind, None if pk is None else entry),
        'tatib': tatib, 'books': entry_forms.scripture_books(),
        'song': getattr(form, 'song', None),
        'after': request.GET.get('after') if pk is None else None,
        'save_url': reverse('web-entry-save' if pk else 'web-entry-save-new',
                            kwargs={'pk': pk} if pk else {})
                    + ('' if pk else f'?tatib={tatib.pk}'),
    })


def entry_save(request, pk=None):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    entry = get_object_or_404(tatib_models.ServiceEntry, pk=pk) if pk else None
    kind = (entry_forms.kind_name(entry.kind) if entry
            else entry_forms.kind_from_post(request.POST.get('kind')))
    form = entry_forms.build_entry_form(
        kind, data=request.POST, instance=entry,
        tatib=entry.tatib if entry else get_object_or_404(
            tatib_models.TataIbadah, pk=request.GET.get('tatib')))
    if form is None:
        raise Http404('Unknown kind.')
    if not form.is_valid():
        return render(request, 'reading/_entry_form.html', {
            'form': form, 'kind': kind, 'entry': entry,
            'title': entry_forms.entry_title(kind, entry), 'tatib': form.tatib,
            'books': entry_forms.scripture_books(),
            'song': getattr(form, 'song', None),
            'after': request.POST.get('after') if pk is None else None,
            'save_url': reverse('web-entry-save' if pk else 'web-entry-save-new',
                                kwargs={'pk': pk} if pk else {})
                        + ('' if pk else f'?tatib={form.tatib.pk}'),
        }, status=400)
    if entry is None:
        after = request.POST.get('after', '')
        # The stage's anchor is "e<pk>" for a ServiceEntry. Never pass that
        # string to an integer PK lookup (which raises a 500); also avoid
        # treating a legacy item's numeric order as a ServiceEntry PK.
        marker = (tatib_models.ServiceEntry.objects.filter(
            pk=int(after[1:]), tatib=form.tatib).first()
            if after.startswith('e') and after[1:].isdigit() else None)
        if marker is not None:
            # The new entry goes AFTER the clicked entry, never before it.
            (tatib_models.ServiceEntry.objects
             .filter(tatib=form.tatib, order_number__gt=marker.order_number)
             .update(order_number=F('order_number') + 1))
            form.instance.order_number = marker.order_number + 1
        else:
            form.instance.order_number = entry_forms.next_order_number(form.tatib)
    form.instance.kind = entry_forms.KINDS[kind]      # the URL decides the kind, not the post
    saved = form.save()
    return JsonResponse({'ok': True, 'id': saved.pk})


def entry_delete(request, pk):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    entry = get_object_or_404(tatib_models.ServiceEntry, pk=pk)
    entry.delete()
    return JsonResponse({'ok': True})


def entry_reorder(request):
    """The running order, saved in one POST (spec 006, slice 3).

    The same shape the current item API's reorder uses -- one POST of {entry,
    order_number} pairs to a /reorder URL, answering with the order it left behind --
    rather than an endpoint per row.

    What the list NAMES is what moves. Anything it leaves out follows in the order it was
    already in, and the numbers come out contiguous from 1 either way, so a partial list
    can never leave a hole or a duplicate. Every named entry must belong to the Tata
    Ibadah being reordered: a reorder that could move another service's rows is refused
    rather than half-applied. The legacy TataIbadahItem rows live on their own numbering
    and are never touched.
    """
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        payload = json.loads(request.body.decode('utf-8') or '{}')
    except (UnicodeDecodeError, ValueError):
        payload = None
    if not isinstance(payload, dict):
        return JsonResponse({'ok': False, 'error': 'Malformed request.'}, status=400)
    service = tatib_models.TataIbadah.objects.filter(pk=payload.get('tatib')).first()
    if service is None:
        return JsonResponse({'ok': False, 'error': 'Unknown Tata Ibadah.'}, status=400)
    rows = payload.get('entries') or []
    if not isinstance(rows, list):
        return JsonResponse({'ok': False, 'error': 'Malformed request.'}, status=400)

    moved, seen = [], set()
    for row in rows:
        entry = (tatib_models.ServiceEntry.objects
                 .filter(pk=row.get('entry'), tatib=service).first()
                 if isinstance(row, dict) else None)
        if entry is None:
            return JsonResponse(
                {'ok': False, 'error': 'That entry is not in this Tata Ibadah.'}, status=400)
        if entry.pk in seen:
            continue                    # named twice: it goes where it is named first
        seen.add(entry.pk)
        moved.append(entry)

    order = moved + list(service.service_entries.exclude(pk__in=seen).order_by('order_number'))
    for position, entry in enumerate(order, 1):
        if entry.order_number != position:
            entry.order_number = position
            entry.save(update_fields=['order_number'])
    return JsonResponse({
        'ok': True,
        'entries': [{'entry': entry.pk, 'order_number': position}
                    for position, entry in enumerate(order, 1)],
    })


def entry_song_options(request):
    """The song pick's options, grouped by songbook, filtered by q."""
    query = (request.GET.get('q') or '').strip()
    songs = song_models.Song.objects.select_related('book')
    if query:
        songs = songs.filter(Q(title__icontains=query) | Q(number__icontains=query))
    songs = songs.order_by('book__name', 'number', 'title')
    groups, current = [], None
    for song in songs[:200]:
        label = song.book.short_name or song.book.name
        if current is None or current['label'] != label:
            current = {'label': label, 'name': song.book.name, 'songs': []}
            groups.append(current)
        current['songs'].append({'id': song.pk, 'title': song.title,
                                 'number': song.number})
    return render(request, 'reading/_entry_song_options.html', {'groups': groups})


def entry_song_verses(request, pk):
    song = get_object_or_404(song_models.Song, pk=pk)
    numbers = list(song.verse_set.order_by('number').values_list('number', flat=True))
    return JsonResponse({'verses': numbers, 'title': song.title or ''})


def entry_chapter_verses(request, pk, chapter):
    verses = entry_forms.chapter_verse_numbers(pk, chapter)
    if not verses:
        raise Http404('That chapter has no verses here.')
    return JsonResponse({'count': len(verses), 'verses': verses})


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


# A leading "435. " / "435)" / "435 -" inside a title: the alphabetical key drops it.
_TITLE_NUMBER = re.compile(r'^\s*\d+\s*[.\-)\u2013]?\s*')


def _songbooks(selected_id=None):
    # Largest collections first: the accepted mockup's panel order (HAL, KJ,
    # PKJ, NKB, HARIAN, ANTIFON, AJAR) is exactly descending song count.
    books = (song_models.Book.objects.annotate(song_total=Count('song'))
             .order_by('-song_total', 'name', 'lang'))
    return [{'id': book.pk, 'name': book.name, 'short': book.short_name or '',
             'hymn': book.is_hymn_book, 'current': book.pk == selected_id}
            for book in books]


def _song_rows(book, current_id=None):
    # The default is "last modified", newest first, with the file's own order as the
    # tiebreak. Every song in the corpus currently shares one `modified` timestamp, so
    # that tiebreak is what you actually see -- and it has to differ from the A-Z key
    # below, or the toggle would look like it did nothing (spec 005).
    songs = book.song_set.order_by(F('modified').desc(nulls_last=True), 'title')
    rows = []
    for song in songs:
        numbered = book.is_hymn_book and song.number is not None
        rows.append({
            'id': song.pk,
            'number_display': song.book_number if numbered else '',
            'title': song.title or '(untitled)',
            # The A-Z key. Plenty of titles carry their own leading "435. ", which
            # would make alphabetical order identical to the number order.
            'sort_title': _TITLE_NUMBER.sub('', song.title or '').lower(),
            'modified_key': str(int(song.modified.timestamp() * 1000000)) if song.modified else '',
            'current': song.pk == current_id,
        })
    return rows


def _tatib_groups(mode, selected_id=None):
    # Every active service is listed, empty ones included: an empty service has to be
    # reachable to be filled, and its page says it is empty (spec 006 review). The old
    # rule kept only services that already had a legacy text item.
    services = tatib_models.TataIbadah.objects.filter(is_active=True)
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


def _paragraphs(text):
    """A block's lines, with a speaker lifted out of "SPEAKER. text" when present."""
    paras = []
    for line in (text or '').split('\n'):
        match = SPEAKER_RE.match(line)
        if match:
            paras.append({'speaker': match.group(1), 'text': match.group(2)})
        else:
            paras.append({'speaker': '', 'text': line})
    return paras


def _entry_jump(entry):
    """Where a passage or a song entry points, the way a search result does."""
    if entry.kind == tatib_models.ServiceEntryKind.SCRIPTURE and entry.book_translation_id:
        url = reverse('web-bible-chapter',
                      args=[entry.book_translation.book_id, entry.chapter])
        url += f'?v={entry.verse_start}'
        if entry.verse_end:
            url += f'&to={entry.verse_end}'
        return url
    if entry.kind == tatib_models.ServiceEntryKind.SONG and entry.song_id:
        return reverse('web-song', args=[entry.song_id])
    return ''


def _entry_blocks(service, items, toc, text_count):
    """The service's entries, after its legacy items. Additive: a service with none
    renders exactly as it did before (spec 006 keeps the old path working)."""
    for entry in service.service_entries.order_by('order_number'):
        anchor = f'e{entry.pk}'
        title, body = entry.resolve()
        kind_key = entry_forms.kind_name(entry.kind)
        # A passage or a song shows its REFERENCE here, not its text: the pane is the
        # running order, and the words belong on the display.
        shows_text = kind_key not in ('scripture', 'song')
        block = {'entry': True, 'anchor': anchor, 'pk': entry.pk, 'kind': kind_key,
                 'kind_label': entry.get_kind_display(), 'title': title,
                 'paras': _paragraphs(body) if (body and shows_text) else [],
                 'note': entry.title if entry.kind == tatib_models.ServiceEntryKind.SECTION_BREAK
                         else ''}
        if kind_key in ('scripture', 'song'):
            block['jump'] = _entry_jump(entry)
        items.append(block)
        text_count += 1
        label = title or entry.get_kind_display()
        toc.append({'eos': kind_key == 'section_break', 'anchor': anchor, 'n': text_count,
                    'label': label[:60], 'titled': bool(title),
                    'txt': f'{title} {body}'})
    return text_count


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
        items.append({'eos': False, 'anchor': anchor, 'title': item.title,
                      'paras': _paragraphs(item.text)})
        label = item.title or _first_line(item.text)
        if len(label) > 60:
            label = label[:60] + '…'
        toc.append({'eos': False, 'anchor': anchor, 'n': text_count,
                    'label': label or f'Section {text_count}',
                    'titled': bool(item.title),
                    'txt': f'{item.title} {item.text}'})
    text_count = _entry_blocks(service, items, toc, text_count)
    return items, toc


def _line_pairs(text):
    """A body's lines in pairs -- the operator's two-line shape -- with a blank line
    ending a screen, so the text after it starts a fresh one and a single line can
    hold the screen alone."""
    screens, pair = [], []
    for raw in (text or '').split('\n'):
        line = raw.strip()
        if not line:
            if pair:
                screens.append(pair)
                pair = []
            continue
        pair.append(line)
        if len(pair) == 2:
            screens.append(pair)
            pair = []
    if pair:
        screens.append(pair)
    return screens


def _scripture_screens(entry):
    """One verse a screen: the reference names it, and the verse's own title (when the
    translation carries one) says what the passage is called."""
    verses = (bible_models.Verse.objects
              .filter(book_translation_id=entry.book_translation_id, chapter=entry.chapter,
                      verse__gte=entry.verse_start or 1,
                      verse__lte=entry.verse_end or entry.verse_start or 0)
              .order_by('verse'))
    book = entry.book_translation.translation if entry.book_translation_id else ''
    screens = []
    for verse in verses:
        reference = f'{book} {entry.chapter}:{verse.verse}'.strip()
        heading = f'{reference}\n{verse.title}' if verse.title else reference
        screens.append({'blank': False, 'header': heading, 'lines': [verse.text.strip()]})
    return screens


def _projector_screens(service):
    """What the display shows, screen by screen (spec 006, slice 4).

    A passage is one verse at a time, headed by its reference and title; a text is
    two lines at a time under its own header; a song is its lyrics alone, two lines
    at a time; a section break shows nothing -- it is the operator's own note. The
    legacy rows ride along in the same shape before the entries, so the order on the
    screen is the order the reading pane shows.
    """
    screens = []
    for item in service.tataibadahitem_set.order_by('order_number'):
        if item.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
            screens.append({'blank': True, 'header': '', 'lines': []})
            continue
        for lines in _line_pairs(item.text):
            screens.append({'blank': False, 'header': item.title, 'lines': lines})
    for entry in service.service_entries.order_by('order_number'):
        if entry.kind == tatib_models.ServiceEntryKind.SECTION_BREAK:
            screens.append({'blank': True, 'header': '', 'lines': []})
        elif entry.kind == tatib_models.ServiceEntryKind.SCRIPTURE:
            screens.extend(_scripture_screens(entry))
        elif entry.kind == tatib_models.ServiceEntryKind.SONG:
            for lines in _line_pairs(entry.resolve()[1]):
                screens.append({'blank': False, 'header': '', 'lines': lines})
        else:                                            # a text entry
            header, body = entry.resolve()
            for lines in _line_pairs(body):
                screens.append({'blank': False, 'header': header, 'lines': lines})
    return screens


def service_projector(request, service_id):
    """The new service projector: a page of its own, hand-written, showing one screen
    at a time in white on black -- the way the current projector reads on a screen.

    It keeps no server record of what is on screen. Which screen is showing lives in
    the operator's browser and is shared across that browser's tabs over the display
    channel, so several laptops can drive different screens.
    """
    service = get_object_or_404(tatib_models.TataIbadah, pk=service_id)
    return render(request, 'reading/projector.html', {
        'service': service,
        'service_id': service.pk,
        'screens': _projector_screens(service),
        'page_title': f'{service.name} — display',
    })


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
            'result_groups': [],
        })
        if not has_param:
            context['page_title'] = 'GKPS Klender — Search Alkitab, Kidung, and Tata Ibadah'
            return context
        results = search_lib.search(query)
        if not results.valid:
            # An empty query keeps the landing.
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
            'show_song_sort': not book.is_hymn_book,
            'ch_title': f'Song list — {book.name}',
            'book_name': book.name,
            'editor_book_id': book.pk,
            'book_is_hymn': book.is_hymn_book,
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
        context.update({'editor_book_id': book.pk, 'book_is_hymn': book.is_hymn_book})
        context.update({
            'page_title': f'{citation} — GKPS Klender',
            'songbooks': _songbooks(book.pk),
            'songs': _song_rows(book, song.pk),
            'show_song_sort': not book.is_hymn_book,
            'ch_title': f'Song list — {book.name}',
            'verses': verses,
            'read_kind': 'song',
            'read_eyebrow': citation,
            'read_name': song.title or citation,
            'read_no': '',
        })
        return context


@method_decorator(ensure_csrf_cookie, name='dispatch')
class TatibView(TemplateView):
    """Tata Ibadah: services panel (dated / templates) and a service order.

    It carries the CSRF cookie on purpose: saving a rearranged order is a JSON POST from
    the page (static/web/reorder.js), with no form to render a token, so the page itself
    has to have set one.
    """

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
            # Absolute on purpose: the search-first home swaps this button into the live
            # page, where a relative "?mode=..." resolves against /home/ and lands on the
            # search home -- which closes the panel and shows Alkitab (review report).
            'tatib_mode_url': reverse('web-tatib') + f'?mode={other_mode}',
            'tatib_mode_pressed': 'true' if mode == 'template' else 'false',
            'tatib_mode_label': ('Show dated Tata Ibadah' if mode == 'template'
                                 else 'Show Tata Ibadah templates'),
            'service_id': service.pk if service else None,
            'projector_url': (reverse('web-service-projector', args=[service.pk])
                              if service else ''),
            'toc_items': toc,
            'items': items,
            'has_entries': any(block.get('entry') for block in items),
            'read_kind': 'tatib' if service else '',
            'read_name': service.name if service else '',
            'read_no': '',
        })
        if service is not None:
            context['read_eyebrow'] = (search_lib.format_date_short(service.date)
                                       if service.date else 'Tata Ibadah')
        return context
