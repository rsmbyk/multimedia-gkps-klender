"""Songs API contracts."""

from __future__ import annotations

import pytest
from model_bakery import baker

from multimedia.songs import models

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_unauthenticated_can_list_books(api_client, hymn_book):
    response = api_client.get("/api/songs/books")
    assert response.status_code == 200
    assert any(row["id"] == hymn_book.id for row in response.json())


@pytest.mark.django_db
def test_books_accept_optional_trailing_slash(api_client, hymn_book):
    bare = api_client.get("/api/songs/books")
    slashed = api_client.get("/api/songs/books/")
    assert bare.status_code == 200
    assert slashed.status_code == 200
    assert bare.json() == slashed.json()


@pytest.mark.django_db
def test_create_book(api_client, song_lang):
    response = api_client.post(
        "/api/songs/books",
        {
            "lang": song_lang.id,
            "name": "Nyanyian Pujian",
            "short_name": "NP",
            "is_hymn_book": True,
        },
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Nyanyian Pujian"
    assert body["short_name"] == "NP"
    assert models.Book.objects.filter(id=body["id"]).exists()


@pytest.mark.django_db
def test_book_short_name_must_be_unique(api_client, song_lang, hymn_book):
    response = api_client.post(
        "/api/songs/books",
        {
            "lang": song_lang.id,
            "name": "Another KJ",
            "short_name": hymn_book.short_name,
            "is_hymn_book": True,
        },
        format="json",
    )
    assert response.status_code == 400
    assert "short_name" in response.json()


@pytest.mark.django_db
def test_create_song_with_book_id_returns_nested_book(api_client, hymn_book):
    response = api_client.post(
        "/api/songs/songs",
        {
            "book_id": hymn_book.id,
            "number": 100,
            "sub_number": "",
            "title": "New Hymn",
            "is_untitled": False,
            "key": "c",
        },
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["title"] == "New Hymn"
    assert body["book"]["id"] == hymn_book.id
    assert "book_id" not in body


@pytest.mark.django_db
def test_list_songs_filtered_by_book(api_client, hymn_song, plain_song):
    response = api_client.get(f"/api/songs/songs?book={hymn_song.book_id}")
    assert response.status_code == 200
    ids = {row["id"] for row in response.json()}
    assert hymn_song.id in ids
    assert plain_song.id not in ids


@pytest.mark.django_db
def test_create_and_list_verses_filtered_by_song(api_client, hymn_song, song_verse):
    create = api_client.post(
        "/api/songs/verses",
        {
            "song": hymn_song.id,
            "number": 2,
            "lyric": "All I have needed Thy hand hath provided",
        },
        format="json",
    )
    assert create.status_code == 201

    response = api_client.get(f"/api/songs/verses?song={hymn_song.id}")
    assert response.status_code == 200
    numbers = {row["number"] for row in response.json()}
    assert numbers == {1, 2}


@pytest.mark.django_db
def test_verse_number_must_be_at_least_one(api_client, hymn_song):
    response = api_client.post(
        "/api/songs/verses",
        {"song": hymn_song.id, "number": 0, "lyric": "nope"},
        format="json",
    )
    assert response.status_code == 400
    assert "number" in response.json()


@pytest.mark.django_db
def test_update_and_delete_song(api_client, plain_song):
    patch = api_client.patch(
        f"/api/songs/songs/{plain_song.id}",
        {"title": "Updated Title"},
        format="json",
    )
    assert patch.status_code == 200
    assert patch.json()["title"] == "Updated Title"

    delete = api_client.delete(f"/api/songs/songs/{plain_song.id}")
    assert delete.status_code == 204
    assert not models.Song.objects.filter(id=plain_song.id).exists()


@pytest.mark.django_db
def test_blank_short_names_can_coexist(api_client, song_lang, song_book):
    other = baker.make(
        models.Book,
        lang=song_lang,
        name="Another Non Hymn",
        short_name="",
        is_hymn_book=False,
    )
    assert song_book.short_name == ""
    assert other.short_name == ""
