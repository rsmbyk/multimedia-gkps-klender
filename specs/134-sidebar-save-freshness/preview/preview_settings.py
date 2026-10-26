"""Development settings for the disposable Spec 134 preview."""

import os
from pathlib import Path

from multimedia.settings import *  # noqa: F403

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = Path(os.environ['GKPS_PREVIEW_STATIC_ROOT'])
