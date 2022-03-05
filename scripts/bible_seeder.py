import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'multimedia.settings')
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

import json

from django.db import transaction

from multimedia.bible import models


# Languages

with open('raw/bible/langs.json') as f:
    langs_json = json.load(f)

with transaction.atomic():
    for lang in langs_json:
        lang_object, _ = models.Language.objects.get_or_create(name=lang['name'])
        print(lang_object)


# Versions

with open('raw/bible/versions.json') as f:
    versions_json = list(filter(lambda x: x.pop('include'), json.load(f)))

with transaction.atomic():
    for version in versions_json:
        version['lang'] = models.Language.objects.get(name=version['lang'])
        version_object, _ = models.Version.objects.get_or_create(**version)
        print(version_object)


# Books

with open('raw/bible/books.json') as f:
    books_json = json.load(f)

with transaction.atomic():
    for book in books_json:
        book_object, _ = models.Book.objects.get_or_create(**book)
        print(book_object)


# Book Translations

with transaction.atomic():
    for version in versions_json:
        with open(f'raw/bible/book_translations/{version["abbreviation"]}.json') as f:
            book_translation_json = json.load(f)

        for book, translation in book_translation_json.items():
            book_translation_object, _ = models.BookTranslation.objects.get_or_create(
                version=models.Version.objects.get(abbreviation=version['abbreviation']),
                book=models.Book.objects.get(name=book),
                translation=translation,
            )
            print(book_translation_object)


# Versions

with transaction.atomic():
    for version in versions_json:
        with open(f'raw/bible/verses/{version["abbreviation"]}.json') as f:
            verses_json = json.load(f)

        for book_name, book in verses_json.items():
            for chapter_number, chapter in book.items():
                for verse_number, verse in chapter.items():
                    verse_object, _ = models.Verse.objects.get_or_create(
                        book_translation=models.BookTranslation.objects.get(
                            version__abbreviation=version['abbreviation'],
                            book__name=book_name,
                        ),
                        chapter=int(chapter_number),
                        verse=int(verse_number),
                        title=verse['title'],
                        text=verse['text'],
                    )
                    print(verse_object)
