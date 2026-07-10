"""Pytest bootstrap for Django.

Keeps the process in a safe default before settings_test is imported.
multimedia.settings_test forces Compose Postgres (default 127.0.0.1:5433) and
ignores Neon URLs from .env. See docs/TDD.md for the SSH tunnel / port notes.
"""

from __future__ import annotations

import os

# settings.py requires these when imported by settings_test.
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://multimedia:multimedia@127.0.0.1:5433/multimedia",
)
