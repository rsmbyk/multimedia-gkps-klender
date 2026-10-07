"""Tatib API contracts."""

from __future__ import annotations

from datetime import date

import pytest
from model_bakery import baker

from multimedia.tatib import models

pytestmark = pytest.mark.integration


@pytest.mark.django_db
def test_unauthenticated_can_create_tatib(api_client):
    response = api_client.post(
        "/api/tatib/tatibs",
        {"name": "Ibadah Pagi", "date": None, "is_active": True},
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Ibadah Pagi"


@pytest.mark.django_db
def test_tatib_filters(api_client):
    dated = baker.make(
        models.TataIbadah, name="July", date=date(2026, 7, 10), is_active=True
    )
    undated = baker.make(
        models.TataIbadah, name="Undated", date=None, is_active=True
    )

    has_date = api_client.get("/api/tatib/tatibs?has_date=true")
    no_date = api_client.get("/api/tatib/tatibs?has_date=false")
    july = api_client.get("/api/tatib/tatibs?month=7&year=2026&is_active=true")

    assert dated.id in {row["id"] for row in has_date.json()}
    assert undated.id in {row["id"] for row in no_date.json()}
    assert dated.id in {row["id"] for row in july.json()}


@pytest.mark.django_db
def test_item_append_assigns_next_order(api_client, tatib):
    baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="Intro",
        text="Welcome",
        order_number=1,
    )
    response = api_client.post(
        "/api/tatib/items",
        {
            "tatib": tatib.id,
            "item_type": models.TataIbadahItemType.TEXT,
            "title": "Prayer",
            "text": "Let us pray",
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["order_number"] == 2


@pytest.mark.django_db
def test_insert_after_shifts_only_same_tatib(api_client, tatib):
    other = baker.make(models.TataIbadah, name="Other", date=None, is_active=True)
    a1 = baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="A1",
        text="a1",
        order_number=1,
    )
    a2 = baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="A2",
        text="a2",
        order_number=2,
    )
    a3 = baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.END_OF_SECTION,
        title="",
        text="",
        order_number=3,
    )
    b2 = baker.make(
        models.TataIbadahItem,
        tatib=other,
        item_type=models.TataIbadahItemType.TEXT,
        title="B2",
        text="b2",
        order_number=2,
    )

    response = api_client.post(
        "/api/tatib/items",
        {
            "tatib": tatib.id,
            "item_type": models.TataIbadahItemType.TEXT,
            "title": "Inserted",
            "text": "between 1 and 2",
            "insert_after": 1,
        },
        format="json",
    )
    assert response.status_code == 201
    assert response.json()["order_number"] == 2

    a1.refresh_from_db()
    a2.refresh_from_db()
    a3.refresh_from_db()
    b2.refresh_from_db()
    assert a1.order_number == 1
    assert a2.order_number == 3
    assert a3.order_number == 4
    assert b2.order_number == 2  # other tatib must not shift


@pytest.mark.django_db
def test_reorder_tatib_items(api_client, tatib):
    first = baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="First",
        text="1",
        order_number=1,
    )
    second = baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="Second",
        text="2",
        order_number=2,
    )
    response = api_client.post(
        "/api/tatib/items/reorder",
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


@pytest.mark.django_db
def test_list_items_filtered_and_ordered(api_client, tatib):
    baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="Second",
        text="2",
        order_number=2,
    )
    baker.make(
        models.TataIbadahItem,
        tatib=tatib,
        item_type=models.TataIbadahItemType.TEXT,
        title="First",
        text="1",
        order_number=1,
    )
    response = api_client.get(
        f"/api/tatib/items?tatib={tatib.id}&ordering=order_number"
    )
    assert response.status_code == 200
    assert [row["order_number"] for row in response.json()] == [1, 2]
