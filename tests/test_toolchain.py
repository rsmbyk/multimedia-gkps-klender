"""Smoke checks that the Python test toolchain is wired correctly."""

import os

import dj_database_url
import pytest
from django.conf import settings

from multimedia.env import DEFAULT_DB_HOST_PORT, DEFAULT_TEST_DATABASE_URL


@pytest.mark.unit
def test_compose_db_port_avoids_well_known_ports():
    """Published host port sits in the IANA dynamic range, not 8000/5432."""
    assert 49152 <= DEFAULT_DB_HOST_PORT <= 65535
    assert DEFAULT_DB_HOST_PORT not in {8000, 5432}


@pytest.mark.unit
def test_default_test_database_url_matches_compose_db_port():
    """The shared default resolves to loopback on the port compose publishes."""
    parsed = dj_database_url.parse(DEFAULT_TEST_DATABASE_URL)
    assert parsed["HOST"] in {"127.0.0.1", "localhost"}
    assert str(parsed["PORT"]) == str(DEFAULT_DB_HOST_PORT)


@pytest.mark.unit
def test_django_settings_test_uses_postgres():
    """Pytest uses settings_test Postgres; pytest-django prefixes a test_ DB name."""
    assert settings.configured
    engine = settings.DATABASES["default"]["ENGINE"]
    assert "postgresql" in engine
    # pytest-django rewrites NAME to test_<name> for the live connection.
    assert "multimedia" in settings.DATABASES["default"]["NAME"]
    # An explicit TEST_DATABASE_URL (CI, SSH tunnel, in-container run) is
    # allowed to point anywhere, so only the default path is pinned here.
    if not os.environ.get("TEST_DATABASE_URL"):
        assert settings.DATABASES["default"]["HOST"] in {"127.0.0.1", "localhost"}
        # Loopback + the port docker-compose.yml publishes, from one shared
        # default so the stack and the host suite cannot drift apart.
        assert str(settings.DATABASES["default"]["PORT"]) == str(DEFAULT_DB_HOST_PORT)
