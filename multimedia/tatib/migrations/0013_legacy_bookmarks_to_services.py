"""Turn the old song bookmarks into services (spec 188).

A bookmark was a dated list of songs with the verse numbers to sing -- the same thing a
service entry list holds now. Each active, dated bookmark that still carries at least one
song becomes one Tata Ibadah of kind SERVICE, and its items become SONG entries in the
bookmark's own order.

The bookmark rows are read, never written: the legacy OBS dock keeps working from them.
An undated bookmark cannot be a service (0012's type constraint requires a date for one),
a deleted bookmark stays deleted, and a bookmark with no songs has nothing to carry.

A service already standing under the same name and date never stops the conversion: the
bookmark still becomes its own service beside it, so the pair carries the same name and
date. The name comparison is case-sensitive -- ``Ibadah Minggu`` and ``ibadah minggu`` are
two different names, and either way the answer is a new service. Do not add a
"same name and date already exists" guard: it would silently drop the bookmark's songs.
"""

from django.db import migrations

# Read from the frozen models below, not imported: a migration keeps its own words.
SERVICE = 0  # TataIbadahKind.SERVICE
SONG = 2  # ServiceEntryKind.SONG


def _verse_numbers(raw):
    """``'1,3,10'`` -> ``[1, 3, 10]``. A part that is not a number is dropped, never guessed."""
    numbers = []
    for part in (raw or '').split(','):
        part = part.strip()
        if part.isdigit():
            numbers.append(int(part))
    return numbers


def convert_bookmarks(apps, schema_editor):
    TataIbadah = apps.get_model('tatib', 'TataIbadah')
    ServiceEntry = apps.get_model('tatib', 'ServiceEntry')
    SongBookmark = apps.get_model('bookmarks', 'SongBookmark')
    SongBookmarkItem = apps.get_model('bookmarks', 'SongBookmarkItem')
    database = schema_editor.connection.alias

    bookmarked = (SongBookmarkItem.objects.using(database)
                  .values_list('bookmark_id', flat=True))
    bookmarks = (SongBookmark.objects.using(database)
                 .filter(is_active=True, date__isnull=False, pk__in=bookmarked)
                 .order_by('date', 'pk'))

    for bookmark in bookmarks:
        # Always a service of its own, even where one already stands under this name and
        # date: the bookmark is the record of what was sung, and a blank service somebody
        # created for the same day is not it.
        service = TataIbadah.objects.using(database).create(
            name=bookmark.name, kind=SERVICE, date=bookmark.date, is_active=True)

        items = (SongBookmarkItem.objects.using(database)
                 .filter(bookmark_id=bookmark.pk).order_by('order_number', 'pk'))
        # The bookmark's order numbers can hold gaps left by deleted rows, so the service
        # is numbered from one in the order the bookmark is read.
        ServiceEntry.objects.using(database).bulk_create([
            ServiceEntry(tatib_id=service.pk, kind=SONG, order_number=position,
                         song_id=item.song_id, verses=_verse_numbers(item.verse))
            for position, item in enumerate(items, start=1)
        ])


class Migration(migrations.Migration):
    dependencies = [
        ('tatib', '0012_tataibadah_kind_and_slots'),
        ('bookmarks', '0015_alter_songbookmarkitem_unique_together'),
    ]

    operations = [
        # Forward only: the bookmarks stay the record the old dock reads, and a reverse
        # would have to decide which of two identical services it created.
        migrations.RunPython(convert_bookmarks, migrations.RunPython.noop),
    ]
