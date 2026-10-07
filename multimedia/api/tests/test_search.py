"""Song search and cross-cutting API contracts."""

from __future__ import annotations

import pytest
from model_bakery import baker

from multimedia.songs import models as song_models

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_search_requires_q_min_length_3(api_client):
    missing = api_client.get("/api/search/songs")
    short = api_client.get("/api/search/songs?q=ab")
    assert missing.status_code == 400
    assert short.status_code == 400
    assert "q" in short.json()


@pytest.mark.django_db
def test_search_phrase_match_and_page_size(api_client, hymn_song):
    baker.make(
        song_models.Verse,
        song=hymn_song,
        number=1,
        lyric="Morning by morning new mercies I see",
    )
    baker.make(
        song_models.Verse,
        song=hymn_song,
        number=2,
        lyric="Unrelated lyric about something else",
    )

    response = api_client.get('/api/search/songs?q="new mercies"')
    assert response.status_code == 200
    body = response.json()
    assert "results" in body
    assert body["count"] == 1
    assert "new mercies" in body["results"][0]["lyric"].lower()
    # SearchPagination page size is 50
    assert len(body["results"]) <= 50


@pytest.mark.django_db
def test_search_accepts_plain_phrase_without_quotes(api_client, hymn_song):
    baker.make(
        song_models.Verse,
        song=hymn_song,
        number=1,
        lyric="Great is thy faithfulness morning by morning",
    )
    response = api_client.get("/api/search/songs?q=thy faithfulness")
    assert response.status_code == 200
    assert response.json()["count"] >= 1
