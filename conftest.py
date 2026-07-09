"""Pytest bootstrap for Django.

Keeps the process in a safe default before settings_test is imported. The
authoritative test database is defined in multimedia.settings_test (SQLite
in-memory), so a local .env cannot point the suite at Neon.
"""

from __future__ import annotations

import os

os.environ.setdefault("DJANGO_DEBUG", "True")
