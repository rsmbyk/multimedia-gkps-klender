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
import hashlib
import re
from urllib.parse import quote

from django.db import connection, transaction
from django.db.models import Case, CharField, Count, F, IntegerField, Q, Value, When
from django.db.models.functions import Lower
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
from multimedia.tatib.screen_breaks import eligible_boundaries, single_screen_boundaries, valid_breaks
from multimedia.web.reading import editors
from multimedia.web.reading import entries as entry_forms
from multimedia.web.reading.formatting import format_verses
from multimedia.web.reading import legacy_items
from multimedia.web.reading import search as search_lib
from multimedia.web.reading import voices

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


def _editor_fragment_context(kind, form, pk, target=None):
    kwargs = {'kind': kind, 'pk': pk} if pk else {'kind': kind}
    return {
        'form': form,
        'kind': kind,
        'title': editors.form_title(kind, pk),
        'save_url': reverse('web-editor-save' if pk else 'web-editor-save-new', kwargs=kwargs),
        'target_id': pk or '',
        'book_id': target.pk if kind == 'song' and not pk and target else '',
    }


def editor_form(request, kind, pk=None):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    form, target = editors.build_form(kind, request, pk)
    if form is None:
        raise Http404('Not editable.')
    return render(request, 'reading/_editor_form.html',
                  _editor_fragment_context(kind, form, pk, target))


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
                      _editor_fragment_context(kind, form, pk, target), status=400)
    saved = editors.save_form(kind, form, target)
    return JsonResponse({'ok': True, 'id': saved.pk, 'kind': kind})


def old_item_form(request, pk):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    item = get_object_or_404(tatib_models.TataIbadahItem, pk=pk)
    form = legacy_items.LegacyItemForm(instance=item)
    kind = legacy_items.kind_name(item)
    return render(request, 'reading/_old_item_form.html', {
        'form': form,
        'kind': kind,
        'title': 'Edit note' if kind == 'end_of_section' else 'Edit text',
        'save_url': reverse('web-old-item-save', args=[item.pk]),
    })


def old_item_save(request, pk):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    item = get_object_or_404(tatib_models.TataIbadahItem, pk=pk)
    form = legacy_items.LegacyItemForm(data=request.POST, instance=item)
    kind = legacy_items.kind_name(item)
    context = {
        'form': form,
        'kind': kind,
        'title': 'Edit note' if kind == 'end_of_section' else 'Edit text',
        'save_url': reverse('web-old-item-save', args=[item.pk]),
    }
    if not form.is_valid():
        return render(request, 'reading/_old_item_form.html', context, status=400)
    saved = form.save()
    return JsonResponse({'ok': True, 'id': saved.pk, 'kind': 'old-item'})


def old_item_delete(request, pk):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    item = get_object_or_404(tatib_models.TataIbadahItem, pk=pk)
    service = item.tatib
    with transaction.atomic():
        item.delete()
        _compact_service_order(service)
    return JsonResponse({'ok': True})


def _entry_book_options(form, kind):
    books = entry_forms.scripture_books(
        form['book_translation'].value() if kind == 'scripture' else None)
    book_edition = next((book['selected_edition'] for book in books if book['selected']), 'tb')
    return books, book_edition


def _entry_song_option_label(song):
    if song is None:
        return ''
    if not song.book.is_hymn_book:
        return song.title
    book_label = song.book.short_name or song.book.name
    sub_number = (song.sub_number or '').upper()
    number = f' {song.number}{sub_number}' if song.number is not None else ''
    return f'{book_label}{number} {song.title}'


def _entry_song_reference_filter(query):
    """The picker's ``<book substring> <number prefix>[sub] [title]`` reference."""
    query_parts = query.split()
    number_pattern = re.compile(r'(?P<number>[0-9]+)(?P<sub_number>[A-Za-z]?)')
    number_index = None
    match = None
    for index, part in enumerate(query_parts[1:], start=1):
        candidate = number_pattern.fullmatch(part)
        if candidate is not None:
            number_index = index
            match = candidate
            break
    if number_index is None or match is None:
        return None

    book_query = search_lib.normalize(' '.join(query_parts[:number_index]))
    if not book_query:
        return None
    books = list(song_models.Book.objects.active().filter(is_hymn_book=True)
                 .only('pk', 'name', 'short_name'))
    matching_book_ids = [
        book.pk for book in books
        if any(book_query in search_lib.normalize(alias)
               for alias in (book.name, book.short_name) if alias)
    ]
    if not matching_book_ids:
        return None

    number_digits = match.group('number').lstrip('0') or '0'
    number_field = song_models.Song._meta.get_field('number')
    _, maximum = connection.ops.integer_field_range(number_field.get_internal_type())
    if maximum is None:
        # PositiveIntegerField's portable maximum when a backend doesn't
        # report its integer range (for example, SQLite).
        maximum = 2 ** 31 - 1
    maximum_digits = str(maximum)
    if (len(number_digits) > len(maximum_digits)
            or (len(number_digits) == len(maximum_digits)
                and number_digits > maximum_digits)):
        return None

    number = int(number_digits)
    sub_number = match.group('sub_number')
    if sub_number:
        number_filter = Q(number=number, sub_number__iexact=sub_number)
    elif number_digits == '0':
        number_filter = Q(number=0)
    else:
        number_filter = Q()
        for scale in range(len(maximum_digits) - len(number_digits) + 1):
            low = number * 10 ** scale
            if low > maximum:
                break
            high = min((number + 1) * 10 ** scale - 1, maximum)
            number_filter |= Q(number__range=(low, high))

    reference_filter = Q(book_id__in=matching_book_ids) & number_filter
    title_query = ' '.join(query_parts[number_index + 1:])
    if title_query:
        reference_filter &= Q(title__icontains=title_query)
    return reference_filter


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
    books, book_edition = _entry_book_options(form, kind)
    return render(request, 'reading/_entry_form.html', {
        'form': form, 'kind': kind, 'entry': None if pk is None else entry,
        'title': entry_forms.entry_title(kind, None if pk is None else entry),
        'tatib': tatib, 'books': books, 'book_edition': book_edition,
        'song': getattr(form, 'song', None),
        'song_label': _entry_song_option_label(getattr(form, 'song', None)),
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
        books, book_edition = _entry_book_options(form, kind)
        return render(request, 'reading/_entry_form.html', {
            'form': form, 'kind': kind, 'entry': entry,
            'title': entry_forms.entry_title(kind, entry), 'tatib': form.tatib,
            'books': books, 'book_edition': book_edition,
            'song': getattr(form, 'song', None),
            'song_label': _entry_song_option_label(getattr(form, 'song', None)),
            'after': request.POST.get('after') if pk is None else None,
            'save_url': reverse('web-entry-save' if pk else 'web-entry-save-new',
                                kwargs={'pk': pk} if pk else {})
                        + ('' if pk else f'?tatib={form.tatib.pk}'),
        }, status=400)
    if entry is None:
        after = request.POST.get('after', '')
        with transaction.atomic():
            # Normalize legacy API reorderings before honoring a saved insertion point.
            _compact_service_order(form.tatib)
            marker = None
            if after.startswith('e') and after[1:].isdigit():
                marker = tatib_models.ServiceEntry.objects.filter(
                    pk=int(after[1:]), tatib=form.tatib).first()
            elif after.startswith('l') and after[1:].isdigit():
                marker = tatib_models.TataIbadahItem.objects.filter(
                    pk=int(after[1:]), tatib=form.tatib).first()
            if after == 'start':
                # Insert at the beginning: shift every row up one and take order 1.
                for model in (tatib_models.TataIbadahItem, tatib_models.ServiceEntry):
                    model.objects.filter(tatib=form.tatib).update(
                        order_number=F('order_number') + 1)
                form.instance.order_number = 1
            elif marker is not None:
                # Insert AFTER the clicked element, never before it, shifting both tables.
                for model in (tatib_models.TataIbadahItem, tatib_models.ServiceEntry):
                    model.objects.filter(tatib=form.tatib,
                                         order_number__gt=marker.order_number).update(
                                             order_number=F('order_number') + 1)
                form.instance.order_number = marker.order_number + 1
            else:
                form.instance.order_number = entry_forms.next_order_number(form.tatib)
            form.instance.kind = entry_forms.KINDS[kind]  # the URL decides, not the post
            saved = form.save()
    else:
        form.instance.kind = entry_forms.KINDS[kind]
        saved = form.save()
    return JsonResponse({'ok': True, 'id': saved.pk, 'kind': 'entry'})


def entry_screen_breaks(request, pk):
    """Save the arrangement from a Text entry's preview modal."""
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    try:
        payload = json.loads(request.body)
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({'error': 'Invalid screen breaks.'}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({'error': 'Invalid screen breaks.'}, status=400)
    with transaction.atomic():
        entry = get_object_or_404(tatib_models.ServiceEntry.objects.select_for_update(), pk=pk,
                                  kind=tatib_models.ServiceEntryKind.TEXT)
        if (payload.get('text_signature') != _text_signature(entry.text)
                or payload.get('screen_state_signature') != _screen_state_signature(entry)):
            return JsonResponse({'error': 'The text or screen mode changed. Reopen Preview.'},
                                status=409)
        mode = payload.get('default_screen_mode', entry.default_screen_mode)
        if mode not in tatib_models.TextScreenMode.values or 'breaks' not in payload:
            return JsonResponse({'error': 'Invalid screen mode or breaks.'}, status=400)
        breaks = payload['breaks']
        if breaks is not None and not valid_breaks(
                entry.text, breaks,
                single_screen=mode == tatib_models.TextScreenMode.SINGLE_SCREEN):
            return JsonResponse({'error': 'Breaks must fall between written lines.'}, status=400)
        if mode != entry.default_screen_mode and breaks is not None:
            return JsonResponse({'error': 'Changing default mode clears custom breaks.'}, status=400)
        entry.default_screen_mode = mode
        entry.screen_breaks = breaks
        entry.screen_breaks_reset = False
        entry.full_clean()
        entry.save(update_fields=['default_screen_mode', 'screen_breaks', 'screen_breaks_reset'])
        return JsonResponse({'ok': True, 'breaks': breaks, 'default_screen_mode': mode,
                             'screen_state_signature': _screen_state_signature(entry)})


def entry_delete(request, pk):
    if not editors.editors_allowed(request):
        return HttpResponseForbidden('Editing is restricted.')
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    entry = get_object_or_404(tatib_models.ServiceEntry, pk=pk)
    service = entry.tatib
    with transaction.atomic():
        entry.delete()
        _compact_service_order(service)
    return JsonResponse({'ok': True})


def entry_reorder(request):
    """The running order, saved in one POST (spec 006, slice 3).

    The same shape the current item API's reorder uses -- one POST of {entry,
    order_number} pairs to a /reorder URL, answering with the order it left behind --
    rather than an endpoint per row.

    What the list NAMES is what moves. Anything it leaves out follows in its existing
    order. Entries exchange their slots in the shared sequence; old rows keep their slots.
    An old API reorder may have numbered its rows alone, so normalize first. Every named
    entry must belong to this Tata Ibadah; invalid requests change nothing.
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

    with transaction.atomic():
        _compact_service_order(service)
        current_entries = list(service.service_entries.order_by('order_number', 'pk'))
        by_pk = {entry.pk: entry for entry in current_entries}
        positions = [entry.order_number for entry in current_entries]
        order = [by_pk[entry.pk] for entry in moved]
        order.extend(entry for entry in current_entries if entry.pk not in seen)
        for entry, position in zip(order, positions):
            entry.order_number = position
        if order:
            tatib_models.ServiceEntry.objects.bulk_update(order, ['order_number'])
    return JsonResponse({
        'ok': True,
        'entries': [{'entry': entry.pk, 'order_number': entry.order_number}
                    for entry in order],
    })


def entry_song_options(request):
    """The song pick's options, grouped by songbook, filtered by q."""
    query = (request.GET.get('q') or '').strip()
    songs = song_models.Song.objects.active().filter(book__is_deleted=False).select_related('book')
    if query:
        reference_filter = _entry_song_reference_filter(query)
        if reference_filter is not None:
            songs = songs.filter(reference_filter)
        else:
            book_filter = Q(book__is_hymn_book=True) & (
                Q(book__short_name__icontains=query)
                | Q(book__name__icontains=query))
            songs = songs.filter(
                Q(title__icontains=query) | Q(number__icontains=query) | book_filter)
    songs = songs.annotate(
        picker_hymn_first=Case(
            When(book__is_hymn_book=True, then=Value(0)),
            default=Value(1), output_field=IntegerField()),
        picker_hymn_book_id=Case(
            When(book__is_hymn_book=True, then=F('book_id')),
            default=Value(0), output_field=IntegerField()),
        picker_other_book_name=Case(
            When(book__is_hymn_book=False, then=F('book__name')),
            default=Value(''), output_field=CharField()),
        picker_number_missing=Case(
            When(book__is_hymn_book=True, number__isnull=True, then=Value(1)),
            default=Value(0), output_field=IntegerField()),
        picker_hymn_number=Case(
            When(book__is_hymn_book=True, then=F('number')),
            default=Value(0), output_field=IntegerField()),
        picker_hymn_sub_number=Case(
            When(book__is_hymn_book=True, number__isnull=False, then=Lower('sub_number')),
            default=Value(''), output_field=CharField()),
        picker_other_title=Case(
            When(book__is_hymn_book=False, then=F('title')),
            default=Value(''), output_field=CharField()),
        picker_hymn_title=Case(
            When(book__is_hymn_book=True, then=F('title')),
            default=Value(''), output_field=CharField()),
    ).order_by(
        'picker_hymn_first', 'picker_hymn_book_id',
        'picker_other_book_name', 'book_id', 'picker_number_missing',
        'picker_hymn_number', 'picker_hymn_sub_number',
        'picker_other_title', 'picker_hymn_title', 'pk')
    groups, current = [], None
    current_book_id = None
    for song in songs[:200]:
        book_label = song.book.short_name or song.book.name
        if current is None or current_book_id != song.book_id:
            current_book_id = song.book_id
            current = {'label': book_label, 'name': song.book.name, 'songs': []}
            groups.append(current)
        option_label = _entry_song_option_label(song)
        current['songs'].append({
            'id': song.pk,
            'title': song.title,
            'number': song.number,
            'option_label': option_label,
        })
    return render(request, 'reading/_entry_song_options.html', {'groups': groups})


def entry_song_verses(request, pk):
    song = get_object_or_404(
        song_models.Song.objects.active().filter(book__is_deleted=False), pk=pk)
    numbers = list(song.verse_set.filter(is_deleted=False)
                   .order_by('number').values_list('number', flat=True))
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
    books = (song_models.Book.objects.active()
             .annotate(song_total=Count('song', filter=Q(song__is_deleted=False)))
             .order_by('-song_total', 'name'))
    return [{'id': book.pk, 'name': book.name, 'short': book.short_name or '',
             'hymn': book.is_hymn_book, 'current': book.pk == selected_id}
            for book in books]


def _song_rows(book, current_id=None):
    active_songs = book.song_set.filter(is_deleted=False)
    if book.is_hymn_book:
        songs = active_songs.order_by(
            F('number').asc(nulls_last=True), Lower('sub_number'), 'title')
    else:
        # The default is "last modified", newest first, with the file's own order as the
        # tiebreak. Every song in the corpus currently shares one `modified` timestamp, so
        # that tiebreak is what you actually see -- and it has to differ from the A-Z key
        # below, or the toggle would look like it did nothing (spec 005).
        songs = active_songs.order_by(F('modified').desc(nulls_last=True), 'title')
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


def _tatib_groups(mode, selected_service=None):
    # Every active service is listed, empty ones included: an empty service has to be
    # reachable to be filled, and its page says it is empty (spec 006 review). The old
    # rule kept only services that already had a legacy text item.
    services = tatib_models.TataIbadah.objects.filter(is_active=True)
    selected_id = selected_service.pk if selected_service else None
    if mode == 'template':
        # Mirrors the mockup's Indonesian locale collation for these names:
        # case- and diacritic-folded, with the '|' separator ignored.
        templates = sorted(services.filter(date__isnull=True),
                           key=lambda service: search_lib.normalize(service.name).replace('|', ''))
        rows = [{'id': service.pk, 'name': service.name, 'date_display': '',
                 'current': service.pk == selected_id}
                for service in templates]
        groups = [{'label': 'Templates', 'key': '', 'services': rows}]
    else:
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
    # A service the shown mode does not hold is not listed at all -- no synthetic row and no
    # "currently open" card under the last one (spec 082). The open service is highlighted
    # only where its own row is.
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
    """A liturgy text's lines, each with its voice and its speaker mark lifted out as
    written ("P.", "Paragenda:", "P+J:") when it has one (spec 059)."""
    return [{'mark': line.mark, 'voice': line.voice, 'text': line.text}
            for line in voices.voice_lines((text or '').split('\n'))]


def _plain_paragraphs(text):
    """Lines that are not liturgy (a passage): no speaker, no voice."""
    return [{'mark': '', 'voice': '', 'text': line} for line in (text or '').split('\n')]


def _text_signature(text):
    return hashlib.sha256((text or '').encode('utf-8')).hexdigest()


def _screen_state_signature(entry):
    state = json.dumps([entry.default_screen_mode, entry.screen_breaks], separators=(',', ':'))
    return hashlib.sha256(state.encode('utf-8')).hexdigest()


def _text_preview(entry):
    raw = (entry.text or '').split('\n')
    multi_boundaries = eligible_boundaries(entry.text)
    single_boundaries = single_screen_boundaries(entry.text)
    paragraphs = _paragraphs(entry.text)
    return {'kind': 'editable_text', 'title': entry.title,
            'lines': [dict(para, index=index, present=bool(raw[index - 1].strip()),
                           can_break_after=index in single_boundaries,
                           multi_boundary=index in multi_boundaries)
                      for index, para in enumerate(paragraphs, 1)],
            'breaks_json': json.dumps(entry.screen_breaks),
            'default_screen_mode': entry.default_screen_mode,
            'screen_state_signature': _screen_state_signature(entry),
            'signature': _text_signature(entry.text),
            'save_url': reverse('web-entry-screen-breaks', args=[entry.pk]),
            'reset_notice': entry.screen_breaks_reset}


PANE_TEXT_LINES = 3


def _clamped_paragraphs(text):
    """A text's pane lines: at most PANE_TEXT_LINES, hard-truncated with a trailing "…"
    when the rest is hidden (blank lines count). Returns the lines and whether it was
    clipped; ordinary Text entries offer Preview even when they fit."""
    paras = _paragraphs(text)
    if len(paras) <= PANE_TEXT_LINES:
        return paras, False
    kept = paras[:PANE_TEXT_LINES]
    last = dict(kept[-1])
    last['text'] = last['text'].rstrip() + '…'
    kept[-1] = last
    return kept, True


def _entry_preview(entry, kind_key):
    """The whole content of a passage or song for the read-only preview."""
    title, body = entry.resolve()
    if kind_key == 'scripture':
        return {'kind': 'passage', 'reference': title, 'paras': _plain_paragraphs(body)}
    song = entry.song
    if song.book.is_hymn_book and song.number is not None:
        heading = entry.citation()      # the short form, shared with the stage (spec 054)
    else:
        heading = f'{song.book.name} — {song.title}' if song.title else song.book.name
    verses = song.verse_set.filter(number__in=entry.verses or [], is_deleted=False).order_by('number')
    return {'kind': 'song', 'heading': heading,
            'verses': [{'number': verse.number, 'lines': (verse.lyric or '').split('\n')}
                       for verse in verses]}


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


def _ordered_service_rows(service):
    """Return old rows and entries in their shared Tata Ibadah order."""
    rows = [(row.order_number, 0, row.pk, 'legacy', row)
            for row in service.tataibadahitem_set.order_by('order_number', 'pk')]
    rows.extend((entry.order_number, 1, entry.pk, 'entry', entry)
                for entry in service.service_entries.order_by('order_number', 'pk'))
    return [(kind, row) for _number, _kind_order, _pk, kind, row in sorted(rows)]


def _compact_service_order(service):
    """Close gaps across both tables, preserving the order the service currently shows."""
    legacy_rows, entries = [], []
    for number, (kind, row) in enumerate(_ordered_service_rows(service), 1):
        row.order_number = number
        (legacy_rows if kind == 'legacy' else entries).append(row)
    if legacy_rows:
        tatib_models.TataIbadahItem.objects.bulk_update(legacy_rows, ['order_number'])
    if entries:
        tatib_models.ServiceEntry.objects.bulk_update(entries, ['order_number'])


def _tatib_stage(service):
    items, toc = [], []
    text_count = 0
    for kind, row in _ordered_service_rows(service):
        if kind == 'legacy':
            anchor = row.order_number
            after_marker = f'l{row.pk}'
            if row.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
                items.append({'eos': True, 'anchor': anchor, 'note': row.text,
                              'old_item': True, 'pk': row.pk, 'after_marker': after_marker})
                toc.append({'eos': True, 'anchor': anchor})
                continue
            text_count += 1
            paras, clipped = _clamped_paragraphs(row.text)
            preview = ({'kind': 'text', 'title': row.title, 'paras': _paragraphs(row.text)}
                       if clipped else None)
            items.append({'eos': False, 'anchor': anchor, 'title': row.title,
                          'old_item': True, 'pk': row.pk, 'after_marker': after_marker,
                          'paras': paras, 'clipped': clipped, 'preview': preview})
            label = row.title or _first_line(row.text)
            if len(label) > 60:
                label = label[:60] + '…'
            toc.append({'eos': False, 'anchor': anchor, 'n': text_count,
                        'label': label or f'Section {text_count}',
                        'titled': bool(row.title), 'txt': f'{row.title} {row.text}'})
            continue

        anchor = f'e{row.pk}'
        title, body = row.resolve()
        kind_key = entry_forms.kind_name(row.kind)
        if kind_key == 'section_break':
            # One divider for both shapes: a section_break entry draws the same rule as
            # a legacy END_OF_SECTION row, carrying its own controls. A break has no
            # label (spec 038), so the divider shows no note.
            items.append({'eos': True, 'anchor': anchor, 'note': '',
                          'entry': True, 'pk': row.pk, 'after_marker': anchor})
            text_count += 1
            toc.append({'eos': True, 'anchor': anchor, 'n': text_count,
                        'label': row.get_kind_display(), 'titled': False,
                        'pk': row.pk, 'entry': True, 'txt': row.get_kind_display()})
            continue
        deleted_target = row.target_deleted
        # A passage or a song shows its reference here, not its text: the words belong on the display.
        shows_text = kind_key not in ('scripture', 'song')
        paras, clipped = _clamped_paragraphs(body) if (body and shows_text) else ([], False)
        verse_line = ''
        if kind_key == 'song' and row.song_id and not deleted_target and row.verses:
            # Spec 066: the stage and the sidebar state the entry's own verses, full or partial.
            verse_line = 'Bait ' + format_verses(row.verses)
        block = {'entry': True, 'anchor': anchor, 'pk': row.pk, 'kind': kind_key,
                 'kind_label': row.get_kind_display(), 'title': title,
                 'deleted_target': deleted_target, 'subtitle': verse_line,
                 'paras': paras, 'clipped': clipped,
                 'note': row.title if row.kind == tatib_models.ServiceEntryKind.SECTION_BREAK else ''}
        if kind_key in ('scripture', 'song') and not deleted_target:
            block['jump'] = _entry_jump(row)
        preview = None
        if not deleted_target:
            if kind_key in ('scripture', 'song'):
                preview = _entry_preview(row, kind_key)
            elif kind_key == 'text':
                preview = _text_preview(row)
            elif clipped:
                preview = {'kind': 'text', 'title': title, 'paras': _paragraphs(body)}
        block['preview'] = preview
        items.append(block)
        text_count += 1
        text_kind = kind_key == 'text'
        two_line_label = text_kind and not title
        label = title or row.get_kind_display()
        if two_line_label:
            label = '\n'.join((body or '').split('\n')[:2]) or row.get_kind_display()
        if kind_key == 'song' and row.song_id and row.song.book.is_hymn_book:
            # A hymn song reads by its short reference and title (spec 039).
            song = row.song
            label = f'{song.book_number} {song.title}'.strip() if song.title else song.book_number
        # Keep song parts structured so the sidebar can style them independently.
        song_label = kind_key == 'song' and bool(row.song_id) and not deleted_target
        song_reference, song_title = '', ''
        if song_label:
            song_reference = row.song.book_number if row.song.book.is_hymn_book else ''
            song_title = row.song.title or ('' if song_reference else label)
        filter_text = f'{label} {title} {body} {verse_line}'
        label = label[:60]
        label_lines = label.split('\n') if two_line_label else None
        if verse_line:
            two_line_label = True
            label_lines = [label, verse_line]
        toc.append({'eos': kind_key == 'section_break', 'anchor': anchor, 'n': text_count,
                    'label': label, 'label_lines': label_lines, 'titled': bool(title),
                    'two_line_label': two_line_label, 'pk': row.pk, 'entry': True,
                    'song_label': song_label, 'song_reference': song_reference,
                    'song_title': song_title, 'verse_line': verse_line,
                    'txt': filter_text})
    return items, toc


def _screen_lines(text, voiced=False):
    """A body's lines as the display shows them: the line as written, and its speaker
    voice when the body is a liturgy text (spec 059). Songs and passages pass no voice."""
    raw_lines = (text or '').split('\n')
    if not voiced:
        return [{'text': raw, 'voice': ''} for raw in raw_lines]
    return [{'text': line.line, 'voice': line.voice} for line in voices.voice_lines(raw_lines)]


def _line_pairs(text, voiced=False, breaks=None):
    """Group lines in pairs, or at saved boundaries for a Text entry.

    Blank lines end a screen in either mode. Voices are read over the whole body
    first so a speaker carries onto the next screen of the same item.
    """
    screens, pair = [], []
    for index, raw in enumerate(_screen_lines(text, voiced), 1):
        line = {'text': raw['text'].strip(), 'voice': raw['voice']}
        if not line['text']:
            if pair:
                screens.append(pair)
                pair = []
            continue
        pair.append(line)
        if (index in breaks if breaks is not None else len(pair) == 2):
            screens.append(pair)
            pair = []
    if pair:
        screens.append(pair)
    return screens


def _single_screen_groups(text, breaks):
    """Group voiced lines at saved content boundaries without edge paragraph blanks."""
    groups, group = [], []
    skip_boundary_blanks = False
    for index, line in enumerate(_screen_lines(text, voiced=True), 1):
        if not line['text'].strip() and skip_boundary_blanks:
            continue
        if line['text'].strip():
            skip_boundary_blanks = False
        group.append(line)
        if index in breaks:
            groups.append(group)
            group = []
            skip_boundary_blanks = True
    if group:
        groups.append(group)
    return groups


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
        screens.append({'blank': False, 'header': heading,
                        'lines': [{'text': verse.text.strip(), 'voice': ''}]})
    return screens


def _blank_screen():
    """A built-in rest. It is not a section break and is never stored."""
    return {'blank': True, 'header': '', 'lines': []}


def _song_screens(entry):
    """Each selected verse in stored order, two lines at a time, then one blank.

    The blank after the last verse is the entry's only trailing rest.
    """
    if not entry.song_id:
        return []
    verses = (entry.song.verse_set.filter(number__in=entry.verses or [], is_deleted=False)
              .order_by('number'))
    screens = []
    for verse in verses:
        for lines in _line_pairs(verse.lyric):
            screens.append({'blank': False, 'header': '', 'lines': lines})
        screens.append(_blank_screen())
    return screens


def _projector_data(service):
    """Projection screens and their service-entry/bait boundaries (spec 091)."""
    screens, entries = [], []
    for kind, row in _ordered_service_rows(service):
        start = len(screens)
        baits = []
        if kind == 'legacy':
            if row.item_type == tatib_models.TataIbadahItemType.END_OF_SECTION:
                group = [_blank_screen()]
                entry_type, label, untitled = 'break', row.text or '', False
            else:
                group = [{'blank': False, 'header': row.title, 'lines': lines}
                         for lines in _line_pairs(row.text, voiced=True)]
                group.append(_blank_screen())
                entry_type = 'text'
                untitled = not bool(row.title)
                label = row.title or _first_line(row.text)
        elif row.kind == tatib_models.ServiceEntryKind.SECTION_BREAK:
            group = [_blank_screen()]
            entry_type, label, untitled = 'break', row.title or '', False
        elif row.kind == tatib_models.ServiceEntryKind.SCRIPTURE:
            group = _scripture_screens(row) + [_blank_screen()]
            entry_type, label, untitled = 'passage', row.citation(), False
            if row.book_translation_id:
                for translation in bible_models.BookTranslation.objects.filter(
                        book_id=row.book_translation.book_id,
                        version__abbreviation__in=['TB', 'SIM']).select_related('version'):
                    verses = bible_models.Verse.objects.filter(
                        book_translation=translation, chapter=row.chapter,
                        verse__gte=row.verse_start or 1,
                        verse__lte=row.verse_end or row.verse_start or 0).order_by('verse')
                    for verse in verses:
                        position = verse.verse - (row.verse_start or 1)
                        if 0 <= position < len(group) - 1:
                            reference = f'{translation.translation} {row.chapter}:{verse.verse}'
                            group[position].setdefault('translations', {})[
                                translation.version.abbreviation.upper()] = {
                                    'header': f'{reference}\n{verse.title}' if verse.title else reference,
                                    'line': verse.text.strip(),
                                }
        elif row.kind == tatib_models.ServiceEntryKind.SONG:
            group = []
            if row.song_id:
                for verse in row.song.verse_set.filter(
                        number__in=row.verses or [], is_deleted=False).order_by('number'):
                    bait_start = start + len(group)
                    pairs = _line_pairs(verse.lyric)
                    for split, lines in enumerate(pairs, 1):
                        group.append({'blank': False, 'header': '', 'lines': lines,
                                      'bait': verse.number, 'split': split,
                                      'split_total': len(pairs)})
                    group.append({**_blank_screen(), 'bait': verse.number, 'bait_rest': True})
                    baits.append({'number': verse.number, 'start': bait_start,
                                  'end': start + len(group) - 1})
            entry_type, untitled = 'song', False
            label = (row.song.book_number if row.song.book.is_hymn_book
                     else row.song.title or row.song.book.name) if row.song_id else ''
        else:
            header, body = row.resolve()
            single = row.default_screen_mode == tatib_models.TextScreenMode.SINGLE_SCREEN
            groups = ([_screen_lines(body, voiced=True)] if row.screen_breaks is None
                      else _single_screen_groups(body, row.screen_breaks)) if single else _line_pairs(
                          body, voiced=True, breaks=row.screen_breaks)
            group = [{'blank': False, 'header': header, 'lines': lines, 'single': single}
                     for lines in groups]
            group.append(_blank_screen())
            entry_type, untitled = 'text', not bool(header)
            label = header or _first_line(body)

        for position, screen in enumerate(group):
            screen['entry_index'] = len(entries)
            if entry_type == 'text' and not screen['blank']:
                screen['split'] = position + 1
                screen['split_total'] = len(group) - 1
            screens.append(screen)
        entries.append({'type': entry_type, 'label': label, 'untitled': untitled,
                        'start': start, 'end': len(screens) - 1, 'baits': baits,
                        'translation': (row.book_translation.version.abbreviation.upper()
                                        if entry_type == 'passage' and row.book_translation_id
                                        else '')})
    return {'screens': screens, 'entries': entries}


def _projector_screens(service):
    """Keep the established screen-list interface for callers and tests."""
    return _projector_data(service)['screens']


def service_projector(request, service_id):
    """The new service projector: a page of its own, hand-written, showing one screen
    at a time in white on black -- the way the current projector reads on a screen.

    It keeps no server record of what is on screen. Which screen is showing lives in
    the operator's browser and is shared across that browser's tabs over the display
    channel, so several laptops can drive different screens.
    """
    service = get_object_or_404(tatib_models.TataIbadah, pk=service_id)
    projector = _projector_data(service)
    return render(request, 'reading/projector.html', {
        'service': service,
        'service_id': service.pk,
        'screens': projector['screens'],
        'projector_screens_data': projector['screens'],
        'projector_entries': projector['entries'],
        'page_title': f'{service.name} — display',
    })


def projector_lookup(request, service_id):
    """The closest passage and song matches for the projector's quick Go To picker."""
    get_object_or_404(tatib_models.TataIbadah, pk=service_id)
    query = (request.GET.get('q') or '').strip()[:120]
    if not query:
        return JsonResponse({'results': []})
    results = search_lib.search(query)
    rows = []
    for row in results['bible']:
        target = row['target']
        if row['kind'] in ('reference', 'chapter') and target.get('chapter'):
            rows.append({'kind': 'passage', 'label': row['title'], 'target': target})

    song_hits = [row for row in results['songs'] if row['kind'] == 'song']
    exact_number_ids = set()
    if query.isdecimal():
        exact_number_ids = set(song_models.Song.objects.active().filter(
            pk__in=[row['target']['song_id'] for row in song_hits],
            number=int(query),
        ).values_list('pk', flat=True))
    # The shared search also scores songbook and lyric matches. Go To keeps
    # title/reference matches, then shows only the strongest available tier.
    strong_hits = [
        (200 if row['target']['song_id'] in exact_number_ids else row['score'], row)
        for row in song_hits
        if row['score'] >= 95 or row['target']['song_id'] in exact_number_ids
    ]
    if strong_hits:
        best_score = max(score for score, _ in strong_hits)
        selected = [row for score, row in strong_hits if score == best_score][:12 - len(rows)]
        songs_by_id = song_models.Song.objects.select_related('book').in_bulk(
            row['target']['song_id'] for row in selected)
        for row in selected:
            song = songs_by_id[row['target']['song_id']]
            label = (_entry_song_option_label(song).strip()
                     if song.book.is_hymn_book else row['title'])
            rows.append({'kind': 'song', 'label': label, 'target': row['target']})
    return JsonResponse({'results': rows[:12]})


def projector_detour(request, service_id):
    """Render an unplanned song or one freely navigable Bible verse on demand."""
    get_object_or_404(tatib_models.TataIbadah, pk=service_id)
    kind = request.GET.get('kind')
    if kind == 'song':
        song = get_object_or_404(song_models.Song.objects.filter(is_deleted=False),
                                 pk=request.GET.get('song_id'))
        screens, baits = [], []
        for verse in song.verse_set.filter(is_deleted=False).order_by('number'):
            start = len(screens)
            groups = _line_pairs(verse.lyric)
            for split, lines in enumerate(groups, 1):
                screens.append({'blank': False, 'header': '', 'lines': lines,
                                'bait': verse.number, 'split': split,
                                'split_total': len(groups)})
            screens.append({**_blank_screen(), 'bait': verse.number, 'bait_rest': True})
            baits.append({'number': verse.number, 'start': start, 'end': len(screens) - 1})
        label = (song.book_number if song.book.is_hymn_book
                 else song.title or song.book.name)
        return JsonResponse({'kind': kind, 'label': label, 'screens': screens, 'baits': baits})

    if kind != 'passage':
        return JsonResponse({'error': 'Unknown detour'}, status=400)
    try:
        book_id = int(request.GET.get('book_id', ''))
        chapter = int(request.GET.get('chapter', '1'))
        verse = int(request.GET.get('verse', '1'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid reference'}, status=400)
    action = request.GET.get('action', '')
    level = request.GET.get('level', 'plain')
    books = list(bible_models.Book.objects.filter(booktranslation__verse__isnull=False)
                 .distinct().order_by('pk').values_list('pk', flat=True))
    if book_id not in books:
        return JsonResponse({'error': 'Book has no verses'}, status=404)
    if level == 'ctrl' and action:
        position = books.index(book_id)
        if action == 'first': position = 0
        elif action == 'last': position = len(books) - 1
        elif action == 'next': position = min(position + 1, len(books) - 1)
        elif action == 'previous': position = max(position - 1, 0)
        book_id = books[position]
        chapter, verse = 1, 1

    translations = list(bible_models.BookTranslation.objects.filter(
        book_id=book_id).select_related('version').order_by('pk'))
    preferred = next((t for t in translations if t.version.abbreviation.upper() == 'TB'),
                     translations[0] if translations else None)
    if not preferred:
        return JsonResponse({'error': 'Book has no translation'}, status=404)
    positions = list(bible_models.Verse.objects.filter(book_translation=preferred)
                     .order_by('chapter', 'verse').values_list('chapter', 'verse'))
    if not positions:
        return JsonResponse({'error': 'Book has no verses'}, status=404)
    if level == 'shift' and action:
        chapters = sorted(set(item[0] for item in positions))
        nearest = min(range(len(chapters)), key=lambda i: abs(chapters[i] - chapter))
        if action == 'first': nearest = 0
        elif action == 'last': nearest = len(chapters) - 1
        elif action == 'next': nearest = min(nearest + 1, len(chapters) - 1)
        elif action == 'previous': nearest = max(nearest - 1, 0)
        chapter = chapters[nearest]
        verse = next(number for ch, number in positions if ch == chapter)
    else:
        current_position = next((i for i, item in enumerate(positions)
                                 if item >= (chapter, verse)), len(positions) - 1)
        if action == 'next': current_position = min(current_position + 1, len(positions) - 1)
        elif action == 'previous': current_position = max(current_position - 1, 0)
        elif action in ('first', 'last') and level == 'plain':
            chapter_positions = [i for i, item in enumerate(positions) if item[0] == chapter]
            if chapter_positions:
                current_position = chapter_positions[-1 if action == 'last' else 0]
        chapter, verse = positions[current_position]
    variants = {}
    for translation in translations:
        abbreviation = translation.version.abbreviation.upper()
        if abbreviation not in ('TB', 'SIM'):
            continue
        row = bible_models.Verse.objects.filter(
            book_translation=translation, chapter=chapter, verse=verse).first()
        if row:
            reference = f'{translation.translation} {chapter}:{verse}'
            variants[abbreviation] = {
                'header': f'{reference}\n{row.title}' if row.title else reference,
                'line': row.text.strip(),
            }
    selected = 'TB' if 'TB' in variants else next(iter(variants), '')
    if not selected:
        return JsonResponse({'error': 'Verse unavailable'}, status=404)
    return JsonResponse({'kind': kind, 'book_id': book_id, 'chapter': chapter,
                         'verse': verse, 'translation': selected,
                         'label': f'{preferred.translation} {chapter}:{verse}',
                         'translations': variants})


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
            song_models.Book.objects.active(), pk=self.kwargs['book_id'])
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
            song_models.Song.objects.active().filter(book__is_deleted=False)
            .select_related('book'), pk=self.kwargs['song_id'])
        book = song.book
        if book.is_hymn_book and song.number is not None:
            citation = f'{book.name} {song.number}{song.sub_number.upper()}'
        else:
            citation = book.name
        verses = [verse.lyric for verse in song.verse_set.filter(is_deleted=False)
                  .order_by('number')]
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
            'tatib_groups': _tatib_groups(mode, service),
            'show_tatib_mode': True,
            # Absolute on purpose: the search-first home swaps this button into the live
            # page, where a relative "?mode=..." resolves against /home/ and lands on the
            # search home -- which closes the panel and shows Alkitab (review report).
            'tatib_mode_url': (reverse('web-tatib-service', args=[service.pk])
                               if service else reverse('web-tatib')) + f'?mode={other_mode}',
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
            context['read_eyebrow'] = (search_lib.format_date_long(service.date)
                                       if service.date else 'Tata Ibadah')
        return context
