# Quickstart: picker popout scrollbar edge

**Spec**: `specs/244-picker-menu-scrollbar-edge/spec.md`

## Prerequisites

- Python 3.12 virtualenv at `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv`.
- The local compose stack's PostgreSQL service, and a dev server started from this worktree.
- Playwright with Chromium for the geometry probe and the E2E test.

## Setup

```sh
cd /home/rsmbyk/Projects/multimedia-gkps-klender-244
# The slice dev server copies DATABASE_URL from the already-running dev server's
# process environment in memory; no credential is written to a file:
/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python \
  /home/rsmbyk/.hermes/cache/scratch/gkps-popout-probe/serve244.py
```

## Run

`http://127.0.0.1:8778/` — from `/`, click the Tata Ibadah tile, the first service, hover the start
bar, choose `+ Passage`, then open Book / Chapter / From verse. The exact click path is in
`preview/README.md`.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Live menu geometry | `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python specs/244-picker-menu-scrollbar-edge/preview/measure.py 8778 after` | scrollport right/bottom 937/891 against menu 938/892 (Book and Chapter), 714/891 against 715/892 (verse) |
| One-option menu | `/home/rsmbyk/Projects/multimedia-gkps-klender/.venv/bin/python specs/244-picker-menu-scrollbar-edge/preview/edges.py` | Chapter menu for Kejadian overflows; after picking Obaja `scrollHeight == clientHeight == 42`, gutter `0` |
| Focused browser module | `DATABASE_URL=<throwaway> .venv/bin/python manage.py test tests.e2e.test_picker_menu_scrollbar_edge --keepdb` | green; written during Implement |
| Accepted sibling modules | `DATABASE_URL=<throwaway> .venv/bin/python manage.py test tests.e2e.test_passage_search_pickers tests.e2e.test_song_entry_pickers --keepdb` | green; deferred to the push step |

## Not yet runnable

- The two browser-module commands above: `tests/e2e/test_picker_menu_scrollbar_edge.py` is written
  during Implement, and the sibling modules are run at the push step. `<throwaway>` is a local
  database name chosen at run time so parallel sessions do not lock the shared test database; no
  credential value is recorded here.
