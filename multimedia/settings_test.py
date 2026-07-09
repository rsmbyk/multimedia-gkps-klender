"""Django settings used only by pytest.

Imports the normal project settings, then forces an in-memory SQLite database
so the suite never touches Neon / DATABASE_URL regardless of local .env.
"""

from multimedia.settings import *  # noqa: F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
