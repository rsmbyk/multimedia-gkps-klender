"""Pytest bootstrap for Django.

Keeps the process in a safe default before settings_test is imported. The
authoritative test database is defined in multimedia.settings_test (SQLite
in-memory) for isolation; the app runtime uses Docker Compose Postgres.
"""

from __future__ import annotations

import os

# settings.py requires these when imported by settings_test.
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://multimedia:multimedia@localhost:5432/multimedia",
)
