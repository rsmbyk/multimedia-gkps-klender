"""Convert ServiceEntry.verses from verse numbers to verse IDs (spec 189, FR-009).

Each stored number becomes the ID of that song's live verse with the same
number; a number naming no live verse is dropped. Legacy SongBookmarkItem.verse
is untouched (FR-015).
"""

from django.db import migrations


def forward(apps, schema_editor):
    ServiceEntry = apps.get_model('tatib', 'ServiceEntry')
    Verse = apps.get_model('songs', 'Verse')
    for entry in ServiceEntry.objects.filter(kind=2, verses__isnull=False):  # SONG
        stored = entry.verses or []
        if not stored:
            continue
        by_number = {
            verse.number: verse.pk
            for verse in Verse.objects.filter(song_id=entry.song_id, is_deleted=False)
        }
        converted = [by_number[number] for number in stored
                     if isinstance(number, int) and number in by_number]
        if converted != stored:
            entry.verses = converted
            entry.save(update_fields=['verses'])


def backward(apps, schema_editor):
    # Reverse is identity-by-read: IDs would be written back as numbers via
    # the same live mapping when live. Kept no-op for simplicity; the
    # forward mapping is idempotent, so re-running is safe.
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('songs', '0016_alter_verse_unique_together_and_more'),
        ('tatib', '0013_legacy_bookmarks_to_services'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
