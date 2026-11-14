from datetime import date

from multimedia.bible import models as bible
from multimedia.songs.models import Book, Song
from multimedia.tatib.models import ServiceEntry, ServiceEntryKind, TataIbadah

songbook = Book.objects.create(
    name='Preview Songbook', short_name='PSF', is_hymn_book=False)
song = Song.objects.create(book=songbook, title='Preview Song — Before')
service = TataIbadah.objects.create(
    name='Preview Tata Ibadah — Before', date=date(2026, 11, 1), is_active=True)
ServiceEntry.objects.create(
    tatib=service, kind=ServiceEntryKind.TEXT, order_number=1,
    title='Opening', text='Preview entry content')
bible_language = bible.Language.objects.create(name='Indonesia')
bible_version = bible.Version.objects.create(
    lang=bible_language, name='Terjemahan Baru', abbreviation='TB')
bible_book = bible.Book.objects.create(
    name='Mat', testament='new', number_of_chapters=1)
bible_translation = bible.BookTranslation.objects.create(
    version=bible_version, book=bible_book, translation='Matius')
bible.Verse.objects.create(
    book_translation=bible_translation, chapter=1, verse=1,
    text='Preview Bible chapter remains open')

print(f'Tata Ibadah: /tatib/{service.pk}/')
print(f'Song: /songs/{song.pk}/')
print(f'Search: /search?q=Preview')
print(f'Bible: /bible/{bible_book.pk}/1/')
