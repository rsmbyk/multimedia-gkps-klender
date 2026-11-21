#!/bin/sh
# Targeted test runner for slice 210. Credentials stay in the container environment.
set -eu
cd "$(dirname "$0")/../../.."
exec "$HOME/Projects/multimedia-gkps-klender/.venv/bin/python" \
  specs/210-song-verse-picker/preview/db_runner.py "$@"
