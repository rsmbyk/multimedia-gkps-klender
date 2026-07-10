"""Smoke checks that the Python test toolchain is wired correctly."""

import pytest
from django.conf import settings


@pytest.mark.unit
def test_django_settings_load_with_sqlite():
    assert settings.configured
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
