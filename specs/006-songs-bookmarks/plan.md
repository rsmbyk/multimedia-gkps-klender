# Plan 006: Song bookmarks and setlists

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `SONGS-BM` from `specs/songs/song-bookmarks/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/songs/song-bookmarks/{spec,plan,tasks}.md` into `specs/006-songs-bookmarks/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/songs/song-bookmarks/plan.md`)</summary>

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


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `SONGS-BM` — intended; follow-up may update them.
