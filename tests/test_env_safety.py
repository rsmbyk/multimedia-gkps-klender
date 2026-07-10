"""Env safety helpers used by multimedia.settings."""

import pytest
from django.core.exceptions import ImproperlyConfigured

from multimedia.env import (
    build_databases,
    resolve_secret_key,
    validate_debug_on_vercel,
)


@pytest.mark.unit
def test_resolve_secret_key_requires_value_when_debug_false():
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        resolve_secret_key(debug=False, secret_key="")


@pytest.mark.unit
def test_resolve_secret_key_requires_value_when_debug_true():
    with pytest.raises(ImproperlyConfigured, match="DJANGO_SECRET_KEY"):
        resolve_secret_key(debug=True, secret_key=None)


@pytest.mark.unit
def test_resolve_secret_key_returns_provided_value():
    assert resolve_secret_key(debug=False, secret_key="prod-secret") == "prod-secret"
    assert resolve_secret_key(debug=True, secret_key="dev-secret") == "dev-secret"


@pytest.mark.unit
def test_validate_debug_on_vercel_rejects_debug_true():
    with pytest.raises(ImproperlyConfigured, match="DJANGO_DEBUG"):
        validate_debug_on_vercel(debug=True, vercel=True)


@pytest.mark.unit
def test_validate_debug_on_vercel_allows_debug_false_on_vercel():
    validate_debug_on_vercel(debug=False, vercel=True)


@pytest.mark.unit
def test_validate_debug_on_vercel_allows_debug_true_off_vercel():
    validate_debug_on_vercel(debug=True, vercel=False)


@pytest.mark.unit
def test_build_databases_requires_database_url():
    with pytest.raises(ImproperlyConfigured, match="DATABASE_URL"):
        build_databases(database_url="", skip_database=False)


@pytest.mark.unit
def test_build_databases_skips_when_collectstatic():
    assert build_databases(database_url="", skip_database=True) == {}


@pytest.mark.unit
def test_build_databases_parses_postgres_url():
    databases = build_databases(
        database_url="postgresql://multimedia:multimedia@db:5432/multimedia",
        skip_database=False,
    )
    assert databases["default"]["ENGINE"] in {
        "django.db.backends.postgresql",
        "django.db.backends.postgresql_psycopg2",
    }
    assert databases["default"]["NAME"] == "multimedia"
    assert databases["default"]["HOST"] == "db"
