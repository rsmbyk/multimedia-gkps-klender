from collections import defaultdict

from django.db import migrations, models


def merge_duplicate_books(apps, schema_editor):
    Book = apps.get_model('songs', 'Book')
    Song = apps.get_model('songs', 'Song')
    database = schema_editor.connection.alias
    books = Book.objects.using(database).order_by('pk')
    groups = defaultdict(list)
    for book in books.iterator():
        groups[book.name].append(book)

    for matching_books in groups.values():
        if len(matching_books) < 2:
            continue

        active_books = [book for book in matching_books if not book.is_deleted]
        keeper = (active_books or matching_books)[0]
        duplicates = [book for book in matching_books if book.pk != keeper.pk]

        occupied = set()
        maximum_number = None
        all_songs = Song.objects.using(database).filter(
            book_id__in=[keeper.pk] + [book.pk for book in duplicates]).order_by('pk')
        for song in all_songs.iterator():
            if song.number is not None:
                maximum_number = (song.number if maximum_number is None
                                  else max(maximum_number, song.number))
                if song.book_id == keeper.pk:
                    occupied.add((song.number, song.sub_number))

        for duplicate in duplicates:
            songs = Song.objects.using(database).filter(book_id=duplicate.pk).order_by('pk')
            for song in songs.iterator():
                number = song.number
                if number is not None and (number, song.sub_number) in occupied:
                    number = (maximum_number or 0) + 1
                    while (number, song.sub_number) in occupied:
                        number += 1
                    maximum_number = number

                Song.objects.using(database).filter(pk=song.pk).update(
                    book_id=keeper.pk, number=number)
                if number is not None:
                    occupied.add((number, song.sub_number))
                    maximum_number = (number if maximum_number is None
                                      else max(maximum_number, number))

            Book.objects.using(database).filter(pk=duplicate.pk).delete()


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('songs', '0014_book_deleted_at_book_deleted_by_song_deleted_at_and_more'),
    ]

    operations = [
        migrations.RunPython(merge_duplicate_books, migrations.RunPython.noop),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set(),
        ),
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-is_hymn_book', 'name']},
        ),
        migrations.RemoveField(
            model_name='book',
            name='lang',
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(max_length=32, unique=True),
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
