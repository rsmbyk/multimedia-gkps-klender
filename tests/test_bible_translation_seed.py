"""SIM book abbreviation migration and repeatable seed coverage for Spec 100."""

import json
from pathlib import Path

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase

from multimedia.bible import models as bible
from multimedia.bible.seeding import apply_book_abbreviations


RAW = Path(__file__).resolve().parents[1] / 'raw' / 'bible'


class SimBookAbbreviationSeedTests(TestCase):
    def test_abbreviation_and_full_name_seed_files_cover_every_book(self):
        books = json.loads((RAW / 'books.json').read_text())
        full_names = json.loads((RAW / 'book_translations' / 'SIM.json').read_text())
        abbreviations = json.loads((RAW / 'book_abbreviations' / 'SIM.json').read_text())
        book_names = {row['name'] for row in books}
        expected_codes = '''1Mu 2Mu 3Mu 4Mu 5Mu Jos Pah Rut 1Sa 2Sa 1Ra 2Ra 1Kr 2Kr Esr Neh Est Job Psa Pod Par Dod Jes Jer Tan Hes Dan Hos Joe Ams Obj Jon Mik Nah Hab Sef Hag Sak Mal Mat Mrk Luk Joh Lah Rom 1Ko 2Ko Gal Epe Pil Kol 1Te 2Te 1Ti 2Ti Tit Pim Heb Jak 1Pt 2Pt 1Jo 2Jo 3Jo Jud Pak'''.split()

        self.assertEqual(len(abbreviations), 66)
        self.assertEqual(list(abbreviations.values()), expected_codes)
        self.assertEqual(set(full_names), book_names)
        self.assertEqual(set(abbreviations), book_names)

    def test_seeding_updates_the_existing_rows_and_is_repeatable(self):
        full_names = json.loads((RAW / 'book_translations' / 'SIM.json').read_text())
        abbreviations = json.loads((RAW / 'book_abbreviations' / 'SIM.json').read_text())
        language = bible.Language.objects.create(name='Simalungun')
        version = bible.Version.objects.create(
            lang=language, name='Bibel', abbreviation='SIM')
        translations = {}
        for book_name, full_name in full_names.items():
            book = bible.Book.objects.create(
                name=book_name, testament='old', number_of_chapters=1)
            translations[book_name] = bible.BookTranslation.objects.create(
                version=version, book=book, translation=full_name)

        apply_book_abbreviations(version, abbreviations)
        original_ids = {name: row.pk for name, row in translations.items()}
        apply_book_abbreviations(version, abbreviations)

        self.assertEqual(
            bible.BookTranslation.objects.filter(version=version).count(), 66)
        for book_name, row in translations.items():
            row.refresh_from_db()
            self.assertEqual(row.pk, original_ids[book_name])
            self.assertEqual(row.translation, full_names[book_name])
            self.assertEqual(row.abbreviation, abbreviations[book_name])


class SimBookAbbreviationMigrationTests(TransactionTestCase):
    migrate_from = [('bible', '0003_alter_booktranslation_options')]
    migrate_to = [('bible', '0004_add_booktranslation_abbreviation')]

    def setUp(self):
        super().setUp()
        executor = MigrationExecutor(connection)
        executor.migrate(self.migrate_from)
        old_apps = executor.loader.project_state(self.migrate_from).apps
        Language = old_apps.get_model('bible', 'Language')
        Version = old_apps.get_model('bible', 'Version')
        Book = old_apps.get_model('bible', 'Book')
        BookTranslation = old_apps.get_model('bible', 'BookTranslation')
        Verse = old_apps.get_model('bible', 'Verse')

        language = Language.objects.create(name='Simalungun')
        version = Version.objects.create(
            lang=language, name='Bibel', abbreviation='SIM')
        book = Book.objects.create(name='Kej', testament='old', number_of_chapters=50)
        translation = BookTranslation.objects.create(
            version=version, book=book, translation='1 Musa')
        verse = Verse.objects.create(
            book_translation=translation, chapter=1, verse=1, text='Bani mula')
        self.translation_id = translation.pk
        self.verse_id = verse.pk

        MigrationExecutor(connection).migrate(self.migrate_to)
        self.new_apps = MigrationExecutor(connection).loader.project_state(self.migrate_to).apps

    def tearDown(self):
        MigrationExecutor(connection).migrate(
            MigrationExecutor(connection).loader.graph.leaf_nodes())
        super().tearDown()

    def test_migration_fills_the_code_without_replacing_names_or_verse_links(self):
        BookTranslation = self.new_apps.get_model('bible', 'BookTranslation')
        Verse = self.new_apps.get_model('bible', 'Verse')
        translation = BookTranslation.objects.get(pk=self.translation_id)
        verse = Verse.objects.get(pk=self.verse_id)

        self.assertEqual(translation.abbreviation, '1Mu')
        self.assertEqual(translation.translation, '1 Musa')
        self.assertEqual(verse.book_translation_id, self.translation_id)
        self.assertEqual(verse.text, 'Bani mula')
