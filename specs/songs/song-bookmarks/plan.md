# Plan: SONGS-BM — Song bookmarks (setlists)

Spec: [`spec.md`](spec.md) (`SONGS-BM`)

## Approach

Document as-built bookmark domain API plus OBS Bookmarks-tab integration. API
rules are proven by pytest; dock wiring by Vitest storage tests and manual OBS
flows.

## Touch points

| Area | Files / modules |
|------|-----------------|
| Models | `multimedia/bookmarks/models.py` |
| API | `multimedia/api/bookmarks/` |
| OBS UI | `multimedia/obs/static/obs/songs/dock/tabs/bookmarks.js`, modals, `bookmark-manager.js`, `bookmark-storage.js` |
| Admin | `multimedia/bookmarks/admin.py` |
| Tests | `multimedia/bookmarks/tests/test_api.py`, bookmark-storage Vitest |

## Contracts

- Active-only uniqueness for `(name, date)` including null dates.
- Item `verse` CSV integers; enriched `verse_info` / `song_info`.
- Reorder body same shape as tatib items reorder.

## Risks and rollout

- Documentation-only; uniqueness self-exclude is intentional (`TEST-COV`).

## Non-goals

- Standalone bookmarks web UI.
