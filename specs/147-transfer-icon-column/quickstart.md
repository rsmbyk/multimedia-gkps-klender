# Quickstart: a transfer row's icon column

**Slice**: `specs/147-transfer-icon-column` · Contracts: [`none.md`](./contracts/none.md) · Data model:
[`data-model.md`](./data-model.md)

## Prerequisites

- The repo venv: `~/Projects/multimedia-gkps-klender/.venv/bin/python` (Django 4.0, Playwright Python
  and its Chromium already installed — the E2E suite uses them).
- The Postgres service from `docker-compose.yml`: `docker compose port db 5432` for the host port
  (`59075` on this machine as of 2026-10-28). The password is the one in `docker-compose.yml`.
- Nothing else. No new dependency, no build step.

## Run it

```sh
cd ~/Projects/multimedia-gkps-klender-147
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8822 --noreload
```

- `/media-library/` — the library; press the Transfers button in the page's own toolbar to open the
  dialog. The rows come from the local media companion on `127.0.0.1:63174`; if it is not running the
  dialog says the library is unavailable and there are no rows to measure.

## Check it by hand

1. Open the Transfers dialog on a list that holds both short and long names. Every upload glyph sits
   on one vertical line; every name and every `Completed` starts on one vertical line.
2. The long names end in `…` and their rows are the same height as the rest.
3. Narrow the window to 420px: the dialog turns 382px, the column still holds, three names truncate.
4. Press the rail button instead of the dialog button: same rows, same geometry.

## Run the checks

```sh
cd ~/Projects/multimedia-gkps-klender-147
DATABASE_URL="postgres://multimedia:***@127.0.0.1:59075/multimedia" \
DJANGO_SECRET_KEY=dev-insecure-local-only-change-me \
~/Projects/multimedia-gkps-klender/.venv/bin/python manage.py test tests.e2e.test_media_library --tag e2e
```

If another run holds the shared test database, name a throwaway one instead of fighting it
(`.../gkps147` — Django creates `test_gkps147` and no other session touches it).

## Regenerate the static comparison

```sh
~/Projects/multimedia-gkps-klender/.venv/bin/python \
  specs/147-transfer-icon-column/preview/build_preview.py \
  http://127.0.0.1:8822/media-library/
```

It copies the rows out of that page after its own script has drawn them, and the stylesheets frozen at
`05379336`, so the **Now** panels keep showing the shipped column after the fix is in the tree. Open
`preview/preview.html`.

## Not yet runnable

- Nothing. Every command above runs today; the E2E's three tests are written by `tasks.md` T004–T006
  and are expected red until T007 lands the declaration.
