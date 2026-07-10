"""Shared pytest fixtures for Django app tests."""

from __future__ import annotations

import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from multimedia.bible import models as bible_models
from multimedia.bookmarks import models as bookmark_models
from multimedia.songs import models as song_models
from multimedia.tatib import models as tatib_models


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def song_lang():
    return baker.make(song_models.Language, name="Indonesian")


@pytest.fixture
def hymn_book(song_lang):
    return baker.make(
        song_models.Book,
        lang=song_lang,
        name="Kidung Jemaat",
        short_name="KJ",
        is_hymn_book=True,
    )


@pytest.fixture
def song_book(song_lang):
    return baker.make(
        song_models.Book,
        lang=song_lang,
        name="Lagu Rohani",
        short_name="",
        is_hymn_book=False,
    )


@pytest.fixture
def hymn_song(hymn_book):
    return baker.make(
        song_models.Song,
        book=hymn_book,
        number=12,
        sub_number="a",
        title="Great Is Thy Faithfulness",
        is_untitled=False,
    )


@pytest.fixture
def plain_song(song_book):
    return baker.make(
        song_models.Song,
        book=song_book,
        number=None,
        sub_number="",
        title="Amazing Grace",
        is_untitled=False,
    )


@pytest.fixture
def song_verse(hymn_song):
    return baker.make(
        song_models.Verse,
        song=hymn_song,
        number=1,
        lyric="Morning by morning new mercies I see",
    )


@pytest.fixture
def bible_lang():
    return baker.make(bible_models.Language, name="Indonesian")


@pytest.fixture
def bible_version(bible_lang):
    return baker.make(
        bible_models.Version,
        lang=bible_lang,
        name="Terjemahan Baru",
        abbreviation="TB",
    )


@pytest.fixture
def bible_book():
    return baker.make(
        bible_models.Book,
        name="Yoh",
        testament=bible_models.Testament.NEW,
        number_of_chapters=21,
    )


@pytest.fixture
def bible_translation(bible_version, bible_book):
    return baker.make(
        bible_models.BookTranslation,
        version=bible_version,
        book=bible_book,
        translation="Yohanes",
    )


@pytest.fixture
def bible_verse(bible_translation):
    return baker.make(
        bible_models.Verse,
        book_translation=bible_translation,
        chapter=3,
        verse=16,
        title="",
        text="Karena begitu besar kasih Allah akan dunia ini",
    )


@pytest.fixture
def bookmark():
    return baker.make(
        bookmark_models.SongBookmark,
        name="Sunday Set",
        date=None,
        is_active=True,
    )


@pytest.fixture
def tatib():
    return baker.make(
        tatib_models.TataIbadah,
        name="Ibadah Minggu",
        date=None,
        is_active=True,
    )
