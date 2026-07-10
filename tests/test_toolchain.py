"""Smoke checks that the Python test toolchain is wired correctly."""

import pytest
from django.conf import settings


@pytest.mark.unit
def test_django_settings_test_uses_postgres():
    """Pytest uses settings_test Postgres; pytest-django prefixes a test_ DB name."""
    assert settings.configured
    engine = settings.DATABASES["default"]["ENGINE"]
    assert "postgresql" in engine
    # pytest-django rewrites NAME to test_<name> for the live connection.
    assert "multimedia" in settings.DATABASES["default"]["NAME"]
    assert settings.DATABASES["default"]["HOST"] in {"127.0.0.1", "localhost"}
    assert str(settings.DATABASES["default"]["PORT"]) == "5433"
