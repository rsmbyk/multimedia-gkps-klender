"""Bookmarks API contracts."""

from __future__ import annotations

from datetime import date

import pytest
from model_bakery import baker

from multimedia.bookmarks import models

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_unauthenticated_can_create_bookmark(api_client):
    response = api_client.post(
        "/api/bookmarks/songs/bookmarks",
        {"name": "Evening Set", "date": None, "is_active": True},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Evening Set"


@pytest.mark.django_db
def test_active_bookmark_name_unique_for_null_date(api_client, bookmark):
    response = api_client.post(
        "/api/bookmarks/songs/bookmarks",
        {"name": bookmark.name, "date": None, "is_active": True},
        format="json",
    )
    assert response.status_code == 400
    assert response.json()["name"] == ["This bookmark name already exists"]


@pytest.mark.django_db
def test_active_bookmark_name_unique_for_same_date(api_client):
    baker.make(models.SongBookmark, name="Dated", date=date(2026, 7, 10), is_active=True)
    response = api_client.post(
        "/api/bookmarks/songs/bookmarks",
        {"name": "Dated", "date": "2026-07-10", "is_active": True},
        format="json",
    )
    assert response.status_code == 400
    assert response.json()["name"] == [
        "This bookmark name on this date already exists"
    ]


@pytest.mark.django_db
def test_inactive_bookmark_can_reuse_name(api_client):
    baker.make(models.SongBookmark, name="Reuse", date=None, is_active=False)
    response = api_client.post(
        "/api/bookmarks/songs/bookmarks",
        {"name": "Reuse", "date": None, "is_active": True},
        format="json",
    )
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_bookmark_excludes_self_from_uniqueness(api_client, bookmark):
    response = api_client.patch(
        f"/api/bookmarks/songs/bookmarks/{bookmark.id}",
        {"name": bookmark.name, "date": None, "is_active": True},
        format="json",
    )
    assert response.status_code == 200
    assert response.json()["name"] == bookmark.name


@pytest.mark.django_db
def test_bookmark_filters_has_date_and_month_year(api_client):
    dated = baker.make(
        models.SongBookmark, name="July", date=date(2026, 7, 10), is_active=True
    )
    undated = baker.make(
        models.SongBookmark, name="Undated", date=None, is_active=True
    )

    has_date = api_client.get("/api/bookmarks/songs/bookmarks?has_date=true")
    no_date = api_client.get("/api/bookmarks/songs/bookmarks?has_date=false")
    july = api_client.get(
        "/api/bookmarks/songs/bookmarks?month=7&year=2026&is_active=true"
    )

    assert dated.id in {row["id"] for row in has_date.json()}
    assert undated.id not in {row["id"] for row in has_date.json()}
    assert undated.id in {row["id"] for row in no_date.json()}
    assert dated.id in {row["id"] for row in july.json()}


@pytest.mark.django_db
def test_bookmark_item_auto_order_and_verse_info(
    api_client, bookmark, hymn_song, song_verse
):
    baker.make(
        models.SongBookmarkItem,
        bookmark=bookmark,
        song=hymn_song,
        verse="1",
        order_number=1,
    )
    response = api_client.post(
        "/api/bookmarks/songs/items",
        {
            "bookmark": bookmark.id,
            "song": hymn_song.id,
            "verse": "1,99",
        },
        format="json",
    )
    assert response.status_code == 201
    body = response.json()
    assert body["order_number"] == 2
    verse_info = list(body["verse_info"])
    assert verse_info[0] == {
        "number": 1,
        "lyric": song_verse.lyric,
    }
    assert verse_info[1] == {"number": 99, "lyric": ""}
    assert body["song_info"]["book_number"] == "KJ 12a"
    assert body["song_info"]["title"] == hymn_song.title


@pytest.mark.django_db
def test_bookmark_item_rejects_invalid_verse_list(api_client, bookmark, hymn_song):
    response = api_client.post(
        "/api/bookmarks/songs/items",
        {
            "bookmark": bookmark.id,
            "song": hymn_song.id,
            "verse": "1,abc",
        },
        format="json",
    )
    assert response.status_code == 400
    assert "verse" in response.json()


@pytest.mark.django_db
def test_non_hymn_song_info_book_number_is_null(api_client, bookmark, plain_song):
    from multimedia.songs.models import Verse

    baker.make(Verse, song=plain_song, number=1, lyric="lyric")
    response = api_client.post(
        "/api/bookmarks/songs/items",
        {
            "bookmark": bookmark.id,
            "song": plain_song.id,
            "verse": "1",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["song_info"]["book_number"] is None


@pytest.mark.django_db
def test_reorder_bookmark_items(api_client, bookmark, hymn_song, plain_song, song_verse):
    from multimedia.songs.models import Verse

    baker.make(Verse, song=plain_song, number=1, lyric="a")
    first = baker.make(
        models.SongBookmarkItem,
        bookmark=bookmark,
        song=hymn_song,
        verse="1",
        order_number=1,
    )
    second = baker.make(
        models.SongBookmarkItem,
        bookmark=bookmark,
        song=plain_song,
        verse="1",
        order_number=2,
    )
    response = api_client.post(
        "/api/bookmarks/songs/items/reorder",
        {
            "items": [
                {"item": first.id, "order_number": 2},
                {"item": second.id, "order_number": 1},
            ]
        },
        format="json",
    )
    assert response.status_code == 200
    first.refresh_from_db()
    second.refresh_from_db()
    assert first.order_number == 2
    assert second.order_number == 1
