"""Smoke checks that the Python test toolchain is wired correctly."""

import pytest
from django.conf import settings


@pytest.mark.unit
def test_django_settings_test_uses_in_memory_sqlite():
    """Pytest uses settings_test SQLite; the app itself requires Postgres."""
    assert settings.configured
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
    assert settings.DATABASES["default"]["NAME"] == ":memory:"
