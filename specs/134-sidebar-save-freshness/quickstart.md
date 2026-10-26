# Quickstart: Keep reading views current after sidebar edits

**Spec**: `specs/134-sidebar-save-freshness/spec.md`

## Prerequisites

- The repository's Python 3.12 environment with Django dependencies.
- Chromium installed for the Playwright E2E suite.
- No separate database service for the disposable preview; it creates and removes its own SQLite database and static directory under `/tmp`.

## Setup

No schema or package setup is required for this slice. The preview script applies the existing migrations and seeds disposable Tata Ibadah, songbook, and song records.

## Run

From the repository root:

```sh
specs/134-sidebar-save-freshness/preview/run_preview.sh
```

Open `http://127.0.0.1:8770/tatib/1/` for the Tata Ibadah scenario or `http://localhost:8770/search?q=Preview` for the search-result scenario. The preview writes only to its disposable database. Stop the server with Ctrl+C.

## Verify

| Check | Command | Expected |
| --- | --- | --- |
| Reproduce the active Tata Ibadah stale row | Open `/tatib/1/`, edit the first-sidebar row, and save | Before implementation, stage title changes while the row stays old; after implementation, both show the server-saved name without reloading. |
| Reproduce the stale search result | Open `/search?q=Preview`, select Kidung, edit the matching song, and save | After implementation, the result row and group count reflect whether the saved title still matches; the query remains in place. |
| Verify the implementation E2E suite | `python manage.py test tests.e2e.test_sidebar_save_freshness --noinput -v 2` | All save-freshness scenarios pass against Django's live server and Playwright. |

## Not yet runnable

- The E2E command above is planned but cannot pass yet: `tests/e2e/test_sidebar_save_freshness.py` will be added during Implement, after Gate 2. No application code or test file was written before Gate 2.
