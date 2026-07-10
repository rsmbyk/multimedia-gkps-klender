#!/usr/bin/env bash
# One-shot: dump Neon (DATABASE_URL from .env) into local Compose Postgres.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if [[ ! -f .env ]]; then
  echo "Missing .env (need Neon DATABASE_URL for the dump source)." >&2
  exit 1
fi

NEON_URL="$(grep -E '^DATABASE_URL=' .env | head -1 | cut -d= -f2- | tr -d '\r')"
NEON_URL="${NEON_URL%\"}"
NEON_URL="${NEON_URL#\"}"
NEON_URL="${NEON_URL%\'}"
NEON_URL="${NEON_URL#\'}"
# Windows .env CRLF can leave a trailing CR inside query params.

if [[ -z "${NEON_URL}" ]]; then
  echo "DATABASE_URL is empty in .env" >&2
  exit 1
fi

DUMP_DIR="${DUMP_DIR:-/tmp/neon-migrate}"
DUMP_FILE="${DUMP_DIR}/neon.dump"
NETWORK="${COMPOSE_NETWORK:-multimedia-gkps-klender_default}"
mkdir -p "${DUMP_DIR}"

echo "Dumping Neon to ${DUMP_FILE} ..."
# Host networking avoids flaky Docker DNS / IPv6-only resolution to Neon.
docker run --rm \
  --network host \
  -e DATABASE_URL="${NEON_URL}" \
  -v "${DUMP_DIR}:/out" \
  postgres:16-alpine \
  sh -c 'pg_dump "$DATABASE_URL" --no-owner --no-acl --format=custom --file=/out/neon.dump'

ls -lh "${DUMP_FILE}"

echo "Ensuring local Compose db is up ..."
docker compose up -d db
docker compose exec -T db pg_isready -U multimedia -d multimedia

echo "Dropping and recreating local public schema ..."
docker compose exec -T db psql -U multimedia -d multimedia -v ON_ERROR_STOP=1 -c \
  "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO multimedia; GRANT ALL ON SCHEMA public TO public;"

echo "Restoring dump into local db ..."
set +e
docker run --rm \
  --network "${NETWORK}" \
  -e PGPASSWORD=multimedia \
  -v "${DUMP_DIR}:/in:ro" \
  postgres:16-alpine \
  pg_restore --verbose --no-owner --no-acl \
    -h db -U multimedia -d multimedia \
    /in/neon.dump
restore_rc=$?
set -e

if [[ "${restore_rc}" -gt 1 ]]; then
  echo "pg_restore failed with exit code ${restore_rc}" >&2
  exit "${restore_rc}"
fi

echo "Verifying restore ..."
docker compose exec -T db psql -U multimedia -d multimedia -c \
  "SELECT count(*) AS django_migrations FROM django_migrations;"
docker compose exec -T db psql -U multimedia -d multimedia -c \
  "SELECT relname AS table, n_live_tup AS approx_rows FROM pg_stat_user_tables ORDER BY n_live_tup DESC LIMIT 15;"

echo "Restarting web so it reconnects cleanly ..."
docker compose up -d web

echo "Done."
