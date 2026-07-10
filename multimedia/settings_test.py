"""Django settings used only by pytest.

Imports the normal project settings, then forces Compose Postgres on the host.
pytest-django creates a separate ``test_*`` database from that connection so
the live Compose ``multimedia`` database is not wiped.

This override ignores any Neon/production ``DATABASE_URL`` in ``.env`` so the
suite never runs against remote data.

Default host port is **5433** so pytest does not collide with a local Windows
Postgres that often owns ``localhost:5432``. Reach Compose via either:

- Compose published as ``5433:5432``, or
- ``ssh -f -N -L 5433:127.0.0.1:5432 docker-vm``

Override with env ``TEST_DATABASE_URL`` when needed.
"""

from __future__ import annotations

import os

import dj_database_url

# Must run before importing multimedia.settings (fail-fast env rules).
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://multimedia:multimedia@127.0.0.1:5433/multimedia",
)

from multimedia.settings import *  # noqa: E402, F403

_TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://multimedia:multimedia@127.0.0.1:5433/multimedia",
)

DATABASES = {
    "default": dj_database_url.parse(
        _TEST_DATABASE_URL,
        engine="django.db.backends.postgresql",
    )
}
