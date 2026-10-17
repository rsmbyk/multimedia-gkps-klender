"""Complete, revisioned public-library chunks for Spec 092.

Chunk boundaries keep each response below a large all-library payload. Revisions are
computed from the exact canonical data sent to clients, so an older database row
without a modified timestamp still invalidates its chunk when edited.
"""

import hashlib
import json
import re
from pathlib import Path

from django.conf import settings
from django.db.models import F
from django.db.models.functions import Lower
from django.http import Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib
from multimedia.web.reading.views import _ordered_service_rows, _projector_data, _tatib_stage


def _canonical(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def _revision(data):
    return hashlib.sha256(_canonical(data).encode('utf-8')).hexdigest()


def _bible_chunk(book):
    translations = []
    for translation in (bible.BookTranslation.objects.filter(book=book)
                        .select_related('version', 'version__lang').order_by('pk')):
        verses = list(bible.Verse.objects.filter(book_translation=translation)
                      .order_by('chapter', 'verse')
                      .values('chapter', 'verse', 'title', 'text'))
        translations.append({
            'id': translation.pk,
            'name': translation.translation,
            'abbreviation': translation.abbreviation,
            'version': translation.version.abbreviation or translation.version.name,
            'language': translation.version.lang.name,
            'verses': verses,
        })
    return {'kind': 'bible', 'id': book.pk, 'name': book.name,
            'testament': book.testament, 'chapters': book.number_of_chapters,
            'translations': translations}


def _songs_chunk(book):
    rows = []
    song_rows = songs.Song.objects.active().filter(book=book).prefetch_related('verse_set')
    if book.is_hymn_book:
        song_rows = song_rows.order_by(F('number').asc(nulls_last=True), Lower('sub_number'), 'title', 'pk')
    else:
        song_rows = song_rows.order_by(F('modified').desc(nulls_last=True), 'title')
    for song in song_rows:
        verses = [{'number': verse.number, 'lyric': verse.lyric}
                  for verse in song.verse_set.all() if not verse.is_deleted]
        verses.sort(key=lambda row: row['number'])
        rows.append({'id': song.pk, 'number': song.number, 'sub_number': song.sub_number,
                     'title': song.title or '(untitled)', 'is_untitled': song.is_untitled,
                     'sort_title': re.sub(r'^\s*\d+\s*[.\-)\u2013]?', '', song.title or '').lower(),
                     'modified_key': str(int(song.modified.timestamp() * 1000000))
                     if song.modified else '',
                     'verses': verses})
    return {'kind': 'songs', 'id': book.pk, 'name': book.name,
            'short_name': book.short_name, 'is_hymn_book': book.is_hymn_book,
            'songs': rows}


def _service_chunk(service):
    projector = _projector_data(service)
    items, toc = _tatib_stage(service)
    public_items = [{key: item.get(key) for key in (
        'eos', 'anchor', 'note', 'title', 'subtitle', 'paras', 'clipped', 'kind',
        'media_hash', 'media_family',
        'deleted_target', 'jump', 'entry', 'old_item', 'pk', 'preview', 'after_marker')
        if key in item} for item in items]
    public_toc = [{key: item.get(key) for key in (
        'eos', 'anchor', 'n', 'label', 'label_lines', 'titled',
        'two_line_label', 'song_label', 'song_reference', 'song_title',
        'verse_line', 'txt', 'entry', 'pk') if key in item} for item in toc]
    rows = []
    for kind, row in _ordered_service_rows(service):
        if kind == 'legacy':
            rows.append({'kind': 'legacy', 'id': row.pk, 'order': row.order_number,
                         'item_type': row.item_type, 'title': row.title, 'text': row.text})
        else:
            rows.append({'kind': 'entry', 'id': row.pk, 'order': row.order_number,
                         'entry_kind': row.kind, 'title': row.title, 'text': row.text,
                         'screen_mode': row.default_screen_mode,
                         'screen_breaks': row.screen_breaks,
                         'book_translation_id': row.book_translation_id,
                         'chapter': row.chapter, 'verse_start': row.verse_start,
                         'verse_end': row.verse_end, 'song_id': row.song_id,
                         'verses': row.verses})
    return {'kind': 'service', 'id': service.pk, 'name': service.name,
            'date': service.date.isoformat() if service.date else None,
            'rows': rows, 'items': public_items, 'toc': public_toc,
            'screens': projector['screens'], 'entries': projector['entries']}


def _chunk(kind, pk):
    if kind == 'bible':
        return _bible_chunk(get_object_or_404(bible.Book, pk=pk))
    if kind == 'songs':
        return _songs_chunk(get_object_or_404(songs.Book.objects.active(), pk=pk))
    if kind == 'service':
        return _service_chunk(get_object_or_404(tatib.TataIbadah, pk=pk, is_active=True))
    raise Http404('Unknown offline chunk')


def manifest(request):
    chunks = []
    for kind, queryset in (
        ('bible', bible.Book.objects.order_by('pk')),
        ('songs', songs.Book.objects.active().order_by('pk')),
        ('service', tatib.TataIbadah.objects.filter(is_active=True).order_by('pk')),
    ):
        for row in queryset:
            data = _chunk(kind, row.pk)
            chunks.append({'key': f'{kind}:{row.pk}', 'revision': _revision(data),
                           'url': f'/offline/chunk/{kind}/{row.pk}/'})
    response = JsonResponse({'schema': 1, 'chunks': chunks})
    response['Cache-Control'] = 'no-store'
    return response


def chunk(request, kind, pk):
    data = _chunk(kind, pk)
    revision = _revision(data)
    response = JsonResponse({'schema': 1, 'revision': revision, 'data': data},
                            json_dumps_params={'ensure_ascii': False})
    response['Cache-Control'] = 'no-store'
    response['ETag'] = '"' + revision + '"'
    return response


def projector_shell(request):
    """A reusable offline document; the client fills its screens from IndexedDB."""
    return render(request, 'reading/projector.html', {
        'service_id': 0, 'screens': [], 'page_title': 'Service display',
        'projector_entries': [], 'projector_screens_data': [],
    })


def service_worker(request):
    source = (Path(settings.BASE_DIR) / 'static/web/service-worker.js').read_text()
    version = (Path(settings.BASE_DIR) / 'VERSION').read_text().strip()
    root = Path(settings.BASE_DIR)
    asset_paths = [root / path.lstrip('/') for path in
                   re.findall(r"['\"](/static/[^'\"]+)['\"]", source)]
    template_paths = (root / 'multimedia/web/templates/reading').rglob('*.html')
    fingerprint = hashlib.sha256(source.encode('utf-8'))
    for path in sorted(set(asset_paths).union(template_paths)):
        fingerprint.update(str(path.relative_to(root)).encode('utf-8'))
        fingerprint.update(path.read_bytes())
    cache_version = f'{version}-{fingerprint.hexdigest()[:12]}'
    response = HttpResponse(source.replace('__VERSION__', cache_version),
                            content_type='text/javascript')
    response['Cache-Control'] = 'no-cache'
    response['Service-Worker-Allowed'] = '/'
    return response
