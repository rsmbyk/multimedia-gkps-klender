"""Django settings used only by pytest.

Imports the normal project settings, then forces Compose Postgres on the host.
pytest-django creates a separate ``test_*`` database from that connection so
the live Compose ``multimedia`` database is not wiped.

This override ignores any Neon/production ``DATABASE_URL`` in ``.env`` so the
suite never runs against remote data.

Default host port is the one ``docker-compose.yml`` publishes for ``db``
(``multimedia.env.DEFAULT_DB_HOST_PORT``, from the IANA dynamic range), so
pytest and the stack cannot disagree. Reach Compose via either:

- Compose published on that port, or
- ``ssh -f -N -L <that port>:127.0.0.1:5432 docker-vm``

Override with env ``TEST_DATABASE_URL`` when needed.
"""

from __future__ import annotations

import os

import dj_database_url

from multimedia.env import DEFAULT_TEST_DATABASE_URL

# Must run before importing multimedia.settings (fail-fast env rules).
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault("DATABASE_URL", DEFAULT_TEST_DATABASE_URL)

from multimedia.settings import *  # noqa: E402, F403

_TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL", DEFAULT_TEST_DATABASE_URL)

DATABASES = {
    "default": dj_database_url.parse(
        _TEST_DATABASE_URL,
        engine="django.db.backends.postgresql",
    )
}
