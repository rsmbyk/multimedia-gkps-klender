#!/bin/sh
set -e

if [ "${RUN_MIGRATIONS}" = "true" ]; then
    python manage.py migrate --noinput
fi

if [ "${COLLECT_STATIC}" = "true" ]; then
    python manage.py collectstatic --noinput
fi

# Fonts the operator mounted at start (Office-only faces) join fontconfig's inventory; the converter's
# cache identity covers that inventory, so a deck converted before them is converted again.
if [ -d /usr/share/fonts/operator ]; then
    fc-cache -f >/dev/null 2>&1 || true
fi

exec "$@"
