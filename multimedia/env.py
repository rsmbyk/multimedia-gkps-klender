"""Environment resolution helpers for Django settings.

Kept importable without loading full Django settings so unit tests can cover
fail-fast rules without reloading the settings module.
"""

from __future__ import annotations

from typing import Any

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


# Host port where ``docker-compose.yml`` publishes its ``db`` service. Picked
# from the IANA dynamic range (49152-65535) so the stack is unlikely to collide
# with other local apps; override per clone with ``DB_PORT`` in ``.env``.
#
# This lives here — a module with no Django settings side effects, importable
# before settings load — so ``conftest.py`` and ``multimedia.settings_test``
# read the same value the compose file publishes instead of repeating a
# literal that can drift. See ``specs/018-local-compose-ports/``.
DEFAULT_DB_HOST_PORT = 59075

DEFAULT_TEST_DATABASE_URL = (
    f"postgresql://multimedia:multimedia@127.0.0.1:{DEFAULT_DB_HOST_PORT}/multimedia"
)


def resolve_secret_key(*, debug: bool, secret_key: str | None) -> str:
    """Return DJANGO_SECRET_KEY or raise if missing.

    A random fallback is intentionally not used: with DEBUG=False it would
    rotate on every process start and invalidate sessions/cookies.
    """
    del debug  # required in both modes; kept for a clear call site
    if secret_key:
        return secret_key
    raise ImproperlyConfigured(
        "DJANGO_SECRET_KEY must be set. For local Docker, copy .env.example to "
        ".env. For production, set it in the host environment (e.g. Vercel)."
    )


def validate_debug_on_vercel(*, debug: bool, vercel: bool) -> None:
    """Refuse DEBUG on Vercel so production cannot ship with debug enabled."""
    if vercel and debug:
        raise ImproperlyConfigured(
            "DJANGO_DEBUG must be False when VERCEL is set."
        )


def build_databases(
    *,
    database_url: str | None,
    skip_database: bool,
) -> dict[str, Any]:
    """Build DATABASES from DATABASE_URL, or {} when skipping (collectstatic)."""
    if skip_database:
        return {}
    if not database_url:
        raise ImproperlyConfigured(
            "DATABASE_URL must be set. Local development uses Docker Compose, "
            "which injects a local Postgres URL. Do not point local .env at "
            "production Neon."
        )
    return {
        "default": dj_database_url.parse(database_url),
    }
