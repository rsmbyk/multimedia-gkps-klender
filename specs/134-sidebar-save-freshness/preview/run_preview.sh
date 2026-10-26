#!/usr/bin/env bash
set -euo pipefail

preview_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$preview_dir/../../.." && pwd)"
default_python="$repo_root/../multimedia-gkps-klender/.venv/bin/python"
python_bin="${GKPS_PYTHON:-$default_python}"
if [[ ! -x "$python_bin" ]]; then
  python_bin="$(command -v python3)"
fi

scratch_dir="$(mktemp -d "${TMPDIR:-/tmp}/gkps-sidebar-save-preview.XXXXXX")"
cleanup() {
  rm -rf "$scratch_dir"
}
trap cleanup EXIT INT TERM

export DATABASE_URL="sqlite:///$scratch_dir/db.sqlite3"
export DJANGO_DEBUG=True
export DJANGO_DEVELOPMENT_MODE=False
export DJANGO_SETTINGS_MODULE=preview_settings
export GKPS_PREVIEW_STATIC_ROOT="$scratch_dir/static"
export PYTHONPATH="$preview_dir${PYTHONPATH:+:$PYTHONPATH}"

mkdir -p "$GKPS_PREVIEW_STATIC_ROOT"
"$python_bin" "$repo_root/manage.py" migrate --noinput
"$python_bin" "$repo_root/manage.py" shell < "$preview_dir/seed_preview.py"
"$python_bin" "$repo_root/manage.py" runserver 127.0.0.1:8770 --noreload
