# Quickstart: the first refresh authenticates its references write

**Spec**: `specs/150-references-token-order/spec.md`

## Prerequisites

- The repo's virtualenv at `../multimedia-gkps-klender/.venv` (Playwright 1.47 and its Chromium builds
  already installed).
- A database URL no other worktree is using:
  `DATABASE_URL=postgres://multimedia:<pw>@127.0.0.1:<db-port>/gkps150`.
- For the live readout only: the compose stack (`web` on `http://localhost:63404`, `media` on
  `127.0.0.1:63174`) with this branch merged, and `collectstatic` re-run inside the `web` container so
  Whitenoise serves the new script.

## Setup

```sh
cd ~/Projects/multimedia-gkps-klender-150
export PY=../multimedia-gkps-klender/.venv/bin/python
PW=$(grep -m1 'POSTGRES_PASSWORD' docker-compose.yml | sed 's/.*POSTGRES_PASSWORD: *//; s/"//g; s/ *$//')
DBPORT=$(cd ../multimedia-gkps-klender && docker compose port db 5432 | cut -d: -f2)
export DATABASE_URL="postgres://multimedia:${PW}@127.0.0.1:${DBPORT}/gkps150"
```

## Run

```sh
$PY manage.py test tests.e2e.test_media_library.MediaLibraryE2ETests.test_the_first_refresh_writes_its_references_with_the_token --keepdb --noinput
```

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| the new case | the `Run` command above | green after the fix; red before it (the page's first write carries `''`) |
| the six spec-148 cases under the stricter stub | `$PY manage.py test tests.e2e.test_media_library --keepdb --noinput` | the six green; the module's one pre-existing red (ITEM-156) unchanged |
| the live page, after the merge | `docker compose exec -T web python manage.py collectstatic --noinput && docker compose restart web`, then `$PY specs/148-media-library-refresh-flicker/preview/frame_sampler.py` | `worst jolt: 0px`, exit 0, and `POST /v1/references` answered 200 on the first refresh |

## Not yet runnable

- The live readout, before the merge: the compose `web` service serves the `develop` checkout and a
  worktree server is refused by the companion's origin allow-list (`local_media.py:447`). Recorded as the
  `manual` row for SC-001.
