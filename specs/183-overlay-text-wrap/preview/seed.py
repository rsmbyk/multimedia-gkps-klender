"""Seed the slice-183 database: the overflowing text, plus everything that must not move.

    DATABASE_URL=postgres://multimedia:multimedia@127.0.0.1:59075/gkps183 \
    ~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py shell < \
        specs/183-overlay-text-wrap/preview/seed.py

Idempotent: the service's entries are replaced and the fixture rows are updated in
place, so re-running it never changes the ids the probe reads. Entry order is the
probe's key — entry 0 is the report, 1 the pasted link, 2 the lyric, 3 the passage,
4 and 5 the controls, 6 the 64-character kicker.
"""

from datetime import date

from multimedia.bible import models as bible
from multimedia.songs import models as songs
from multimedia.tatib import models as tatib

PROBE_NAME = 'Ibadah Uji Bungkus 183'
LONG_WORD = 'lo' + 'o' * 118                     # 120 characters, no break opportunity
LONGER = 'https://example.org/' + 'x' * 120       # 140 characters, pasted-URL shape

service, _ = tatib.TataIbadah.objects.get_or_create(
    name=PROBE_NAME, defaults={'date': date(2026, 11, 2), 'is_active': True})
service.service_entries.all().delete()

# 1 -- the report: a liturgy body whose long run has no break opportunity.
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=1, kind=tatib.ServiceEntryKind.TEXT,
    title='Title text',
    text='a very ' + LONG_WORD + ' untitled text')

# 2 -- a liturgy turn with a pasted URL, and a speaker mark.
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=2, kind=tatib.ServiceEntryKind.TEXT,
    title='Persembahan',
    text='L. Marhite ' + LONGER + '\nJ. Amen.')

# 3 -- a hymn whose lyric carries one long word: the caption, not the plate.
book = songs.Book.objects.filter(name='Kidung Jemaat').first()
if book is None:
    book = songs.Book.objects.create(name='Kidung Jemaat', short_name='KJ', is_hymn_book=True)
song, _ = songs.Song.objects.update_or_create(
    book=book, number=991, defaults={'title': 'Uji bungkus 183'})
# Verse is soft-deleted, and a soft-deleted row still holds (song, number): purge it.
songs.Verse._base_manager.filter(song=song).delete()
songs.Verse.objects.create(
    song=song, number=1,
    lyric='Kasih setia Tuhan ' + 'mmmm' * 15 + ' sampai selamanya')
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=3, kind=tatib.ServiceEntryKind.SONG,
    song=song, verses=[1])

# 4 -- a passage whose verse title is one long run.
lang = bible.Language.objects.filter(name='Indonesia').first()
if lang is None:
    lang = bible.Language.objects.create(name='Indonesia')
version = bible.Version.objects.filter(lang=lang, abbreviation='TB').first()
if version is None:
    version = bible.Version.objects.create(lang=lang, name='Terjemahan Baru', abbreviation='TB')
mat = bible.Book.objects.filter(name='Mat').first()
if mat is None:
    mat = bible.Book.objects.create(name='Mat', testament='new', number_of_chapters=28)
translation = bible.BookTranslation.objects.filter(version=version, book=mat).first()
if translation is None:
    translation = bible.BookTranslation.objects.create(version=version, book=mat, translation='Matius')
bible.Verse.objects.update_or_create(
    book_translation=translation, chapter=9, verse=3,
    defaults={'title': 'Judul ' + LONG_WORD,
              'text': 'ayat uji bungkus 183, ' + LONG_WORD + ' dan sisanya pendek'})
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=4, kind=tatib.ServiceEntryKind.SCRIPTURE,
    book_translation=translation, chapter=9, verse_start=3)

# 5 -- the controls: short text everywhere, so the fix's own no-change case exists.
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=5, kind=tatib.ServiceEntryKind.TEXT,
    title='Salam', text='Kasih karunia dan damai sejahtera menyertai kita.\nJ. Amen.')
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=6, kind=tatib.ServiceEntryKind.TEXT,
    title='Tanpa judul', text='Duduklah, jemaat Tuhan.')

# 7 -- a heading that is one long run: the entry's title is the plate's kicker.
tatib.ServiceEntry.objects.create(
    tatib=service, order_number=7, kind=tatib.ServiceEntryKind.TEXT,
    title=('Judul' + 'o' * 59)[:64],          # the column's own 64-character limit
    text='Jemaat menyanyikan pujian.')

print('service', service.pk)
for entry in service.service_entries.order_by('order_number'):
    print(entry.order_number, entry.pk, entry.kind, repr(entry.title))
