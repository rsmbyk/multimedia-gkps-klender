# Quickstart: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`

## Prerequisites

- The repository's virtualenv (`.venv/bin/python` in the main checkout) with `requirements.txt` and
  `requirements-dev.txt` installed, including Playwright and its Chromium build.
- The local database service running (`docker compose up -d db`).
- `DATABASE_URL` pointing at that service.

## Setup

```sh
# from the slice worktree
PORT=$(docker compose port db 5432 | sed 's/.*://')
export DATABASE_URL="postgres://multimedia:***@127.0.0.1:${PORT}/multimedia"
```

## Run

```sh
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python manage.py runserver 0.0.0.0:8769 --noreload
```

Then open `/home/`, sync the saved library once (the offline status control settles), choose Kidung, open
NKB, and open its first song. The sort control must never appear beside "Filter songs…", online or with the
network unavailable; opening a song of "Lagu" still offers it.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| The saved song page agrees with the server on the control | `manage.py test tests.e2e.test_saved_render_parity.SavedRenderParityTests.test_saved_song_pages_match_the_server_sort_control --keepdb` | 1 test, green |
| Opening a hymn song never paints the control | `manage.py test tests.e2e.test_saved_render_parity.SavedRenderParityTests.test_hymn_song_sidebar_open_never_paints_the_sort_control --keepdb` | 1 test, green |
| The parity class and the neighbouring reading classes are unchanged | `manage.py test tests.e2e.test_saved_render_parity tests.e2e.test_offline_library --keepdb` | green |

## Not yet runnable

- Nothing — the slice runs against the existing local stack; no new service, fixture service, or browser
  binary is needed.
