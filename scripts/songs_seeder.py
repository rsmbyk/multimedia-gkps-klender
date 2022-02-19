import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multimedia.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import json
import re

from django.db import transaction

from multimedia.songs.models import Language, Book, Verse, Song


# Language

with open('raw/songs/langs.json') as f:
    langs_json = json.load(f)

for lang in langs_json:
    print(Language.objects.get_or_create(name=lang['name']))


# Books

with open('raw/songs/books.json') as f:
    books_json = json.load(f)

with transaction.atomic():
    for book in filter(lambda x: x['is_active'], books_json):
        book_object, _ = Book.objects.get_or_create(
            lang=Language.objects.get(name=book['lang']),
            name=book['name'],
            short_name=book['short_name'],
            is_hymn_book=True,
        )

        print(book_object)

        # Songs

        with open(f'raw/songs/books/{book["short_name"]}.json') as f:
            hal_json = json.load(f)

        for song in hal_json:
            if 'no' in song:
                number = song['no']
                title = song['title']
            else:
                b, number, title = song['title'].split(maxsplit=2)

            song_object, _ = Song.objects.get_or_create(
                book=book_object,
                number=int(number) if number[-1].isdigit() else int(number[:-1]),
                sub_number='' if number[-1].isdigit() else number[-1].lower(),
                title=title.strip(),
                key=''
                    if len(re.split('[ =]', song['key'])) < 2
                    else re.split('[ =]', song['key'])[1].strip().lower()
            )

            print(song_object)

            # Verses

            for i, verse in enumerate(song['lyrics']):
                verse_object = Verse.objects.get_or_create(
                    song=song_object,
                    number=i+1,
                    lyric=verse,
                )

                print(verse_object)
