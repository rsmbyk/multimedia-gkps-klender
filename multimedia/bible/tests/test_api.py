"""Bible API contracts."""

from __future__ import annotations

import pytest
from model_bakery import baker

from multimedia.bible import models

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_unauthenticated_can_list_versions(api_client, bible_version):
    response = api_client.get("/api/bible/versions")
    assert response.status_code == 200
    assert any(row["id"] == bible_version.id for row in response.json())


@pytest.mark.django_db
def test_create_language_and_book(api_client):
    lang = api_client.post("/api/bible/langs", {"name": "English"}, format="json")
    assert lang.status_code == 201

    book = api_client.post(
        "/api/bible/books",
        {"name": "Gen", "testament": "old", "number_of_chapters": 50},
        format="json",
    )
    assert book.status_code == 201
    assert book.json()["testament"] == "old"


@pytest.mark.django_db
def test_filter_translations_by_version_and_book_name(
    api_client, bible_translation, bible_version, bible_book
):
    other_book = baker.make(
        models.Book, name="Mat", testament=models.Testament.NEW, number_of_chapters=28
    )
    baker.make(
        models.BookTranslation,
        version=bible_version,
        book=other_book,
        translation="Matius",
    )

    by_version = api_client.get(
        f"/api/bible/translations?version={bible_version.id}"
    )
    by_abbr_and_name = api_client.get(
        f"/api/bible/translations?version__abbreviation=TB&book__name={bible_book.name}"
    )

    assert by_version.status_code == 200
    assert len(by_version.json()) == 2
    assert by_abbr_and_name.status_code == 200
    assert len(by_abbr_and_name.json()) == 1
    assert by_abbr_and_name.json()[0]["id"] == bible_translation.id


@pytest.mark.django_db
def test_filter_verses_with_omit(
    api_client, bible_verse, bible_translation, bible_version, bible_book
):
    response = api_client.get(
        "/api/bible/verses"
        f"?book_translation__version__abbreviation={bible_version.abbreviation}"
        f"&book_translation__book__name={bible_book.name}"
        f"&chapter={bible_verse.chapter}"
        "&omit=id,book_translation,chapter"
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 1
    row = body[0]
    assert "id" not in row
    assert "book_translation" not in row
    assert "chapter" not in row
    assert row["verse"] == bible_verse.verse
    assert row["text"] == bible_verse.text


@pytest.mark.django_db
def test_filter_verses_by_book_translation_id(api_client, bible_verse, bible_translation):
    response = api_client.get(
        f"/api/bible/verses?book_translation={bible_translation.id}"
        f"&chapter={bible_verse.chapter}"
    )
    assert response.status_code == 200
    assert any(row["id"] == bible_verse.id for row in response.json())
