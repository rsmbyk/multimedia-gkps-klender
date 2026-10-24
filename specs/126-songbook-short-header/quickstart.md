# Quickstart: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`

## Prerequisites

- The repository's virtualenv (`.venv/bin/python` in the main checkout) with `requirements.txt` and
  `requirements-dev.txt` installed, including Playwright and its Chromium build.
- The local database service running (`docker compose up -d db`).

## Setup

```sh
# from this worktree
PORT=$(cd ~/Projects/multimedia-gkps-klender && docker compose port db 5432 | sed 's/.*://')
export DATABASE_URL="postgres://multimedia:<password>@127.0.0.1:${PORT}/multimedia"
```

## Run

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8768 --noreload
```

Open `/songs/1013/` (PKJ 4): the header above the title reads `PKJ 4` and the tab reads
`PKJ 4 — GKPS Klender`. `/songs/531/` reads `KJ 24A`, `/songs/101/` reads `HAL 101`, and `/songs/1905/`
(an ordinary songbook) still reads `Lagu`. Narrow the window to 768 px and the header stays on one line.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The server header, the fallback, the ordinary songbook and the tab title | `manage.py test multimedia.web.tests.ReadingViewTests --keepdb` | green, including the four new pins |
| Saved and server agree on the header | `manage.py test tests.e2e.test_saved_render_parity.SavedRenderParityTests --keepdb` | green |
| The rest of the reading shell and the saved library are unchanged | `manage.py test multimedia.web.tests tests.e2e.test_offline_library --keepdb` | green |

## Not yet runnable

- Nothing — the slice runs on the existing local stack; no new service, fixture service or browser binary.
