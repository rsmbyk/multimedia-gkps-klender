"""Pytest bootstrap for Django.

Keeps the process in a safe default before settings_test is imported.
multimedia.settings_test forces Compose Postgres (on the host port
docker-compose.yml publishes, via multimedia.env) and ignores Neon URLs from
.env. See docs/TDD.md for the SSH tunnel / port notes.
"""

from __future__ import annotations

import os

from multimedia.env import DEFAULT_TEST_DATABASE_URL

# settings.py requires these when imported by settings_test.
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault("DATABASE_URL", DEFAULT_TEST_DATABASE_URL)
