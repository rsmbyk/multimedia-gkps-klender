"""Entity version guards for the product's write paths (spec 254).

A version is a guard, not a history: a write names the version it opened, and the
server refuses a stale write under a row lock. Helpers here are shared by the
sidebar, entry, legacy-item and verse write paths so the rule has one home.
"""
import json

from django.db import transaction
from django.db.models import F
from django.http import JsonResponse

from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models

CONFLICT_MESSAGE = 'This record changed. Reopen it and try again.'


class VersionConflict(Exception):
    def __init__(self, current_version):
        self.current_version = current_version
        super().__init__(CONFLICT_MESSAGE)


def conflict_response(exc):
    return JsonResponse({'error': 'conflict', 'message': CONFLICT_MESSAGE,
                         'current_version': exc.current_version}, status=409)


def expected(request, key='expected_version'):
    """The version a writer opened, or None when the writer names none."""
    if (request.content_type or '').startswith('application/json'):
        try:
            body = json.loads(request.body.decode('utf-8') or '{}')
        except (UnicodeDecodeError, ValueError):
            body = {}
    else:
        body = request.POST
    value = body.get(key)
    try:
        return int(value) if value not in (None, '') else None
    except (TypeError, ValueError):
        return None


def guard(row, wanted):
    """Raise VersionConflict when the opened version is behind the stored one."""
    if wanted is not None and row.version != wanted:
        raise VersionConflict(row.version)
    return row


def locked(model, pk, wanted):
    """Fetch one row under a lock and check the version the writer opened."""
    row = model.objects.select_for_update().get(pk=pk)
    return guard(row, wanted)


def bump(row):
    """Advance one row's version; call after a stored-value change."""
    type(row).objects.filter(pk=row.pk).update(version=F('version') + 1)
    row.version += 1


def bump_service(service):
    """A service moves when anything it displays changes."""
    if service is not None:
        bump(service)


def form_changed(form, stored=None):
    """Whether any submitted field differs from the row as it is stored."""
    source = stored or type(form.instance).objects.get(pk=form.instance.pk)
    for name, value in form.cleaned_data.items():
        if name in ('expected_version', 'expected_parent_version', 'kind'):
            continue
        if getattr(source, name, None) != value:
            return True
    return False


def referencing_service_ids(target):
    """Distinct active services/templates naming a live verse of the target."""
    if isinstance(target, song_models.Verse):
        entries = tatib_models.ServiceEntry.objects.filter(
            kind=tatib_models.ServiceEntryKind.SONG, song=target.song)
        live_ids = {target.pk}
    elif isinstance(target, song_models.Book):
        entries = tatib_models.ServiceEntry.objects.filter(
            kind=tatib_models.ServiceEntryKind.SONG, song__book=target)
        live_ids = set(song_models.Verse.objects.filter(
            song__book=target, song__is_deleted=False, is_deleted=False
        ).values_list('pk', flat=True))
    else:
        entries = tatib_models.ServiceEntry.objects.filter(
            kind=tatib_models.ServiceEntryKind.SONG, song=target)
        live_ids = set(target.verse_set.filter(is_deleted=False).values_list('pk', flat=True))
    ids = set()
    for service_id, verse_ids in entries.values_list('tatib_id', 'verses'):
        if live_ids.intersection(verse_ids or []):
            ids.add(service_id)
    return ids


def referencing_service_count(target):
    ids = referencing_service_ids(target)
    return tatib_models.TataIbadah.objects.filter(pk__in=ids, is_active=True).count()


def bump_referencing_services(song):
    ids = referencing_service_ids(song)
    if ids:
        tatib_models.TataIbadah.objects.filter(pk__in=ids, is_active=True).update(
            version=F('version') + 1)
