"""Django settings used only by pytest.

Imports the normal project settings, then forces an in-memory SQLite database
for test isolation. The app itself always uses Postgres via DATABASE_URL
(Docker Compose locally, Neon/Vercel in production).
"""

from __future__ import annotations

import os

# Must run before importing multimedia.settings (fail-fast env rules).
os.environ.setdefault("DJANGO_DEBUG", "True")
os.environ.setdefault("DJANGO_SECRET_KEY", "test-insecure-pytest-only")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql://multimedia:multimedia@localhost:5432/multimedia",
)

from multimedia.settings import *  # noqa: E402, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
