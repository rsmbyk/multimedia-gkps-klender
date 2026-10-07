# Plan 017: Current test coverage

- **Status:** Accepted
- **Spec:** [./spec.md](./spec.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Bump:** none
- **Legacy:** `TEST-COV` from `specs/test/current-coverage/`

## Why

Adopt vexbook `v0.4.0` with full migration (`CODE` → `NNN`). Preserve as-built
intent with no behavior change.

## Scope / edges

**In:** copy intent from `specs/test/current-coverage/{spec,plan,tasks}.md` into `specs/017-test-coverage/`.

**Out:** behavior, API, OBS, or schema changes.

## Approach

Header conversion to vexbook `_template` shape; original bodies embedded
verbatim in `spec.md`. Legacy IDs kept readable.

<details>
<summary>Legacy plan (verbatim from `specs/test/current-coverage/plan.md`)</summary>

# Plan: TEST-COV — Current-state test coverage

Spec: [`spec.md`](spec.md) (`TEST-COV`)

## Approach

Lock current product behavior with a layered suite — no feature work except two
small correctness fixes that correct tests will require.

1. **Specify / plan / tasks** (this folder) — done before implementation.
2. **Test tooling** — switch pytest from in-memory SQLite to Compose Postgres;
   add `model_bakery`; refresh `docs/TDD.md` and bootstrap comments.
3. **Tier 1** — DRF `APIClient` integration tests per API area (songs →
   bookmarks → tatib → bible → search → trailing slash), plus the two bugfixes
   driven by failing tests first.
4. **Tier 2** — Vitest unit tests for helpers, BC contracts, storage managers,
   project title formatting (mock BroadcastChannel / localStorage / Rx where
   needed).
5. **Tier 3** — Isolatable web + OBS dock wiring with mocked axios/DOM; avoid
   brittle full Semantic snapshots.
6. **Changelog** — `## Unreleased` `[test]` / `[fix]` bullets.

Work on branch `chore/test-current-coverage` from `develop`. Commit in logical
slices as tasks complete. First publish of the branch waits for Ronald; after
upstream exists, keep a draft PR updated.

## Touch points

| Area | Files / modules (expected) |
|------|----------------------------|
| Specs | `specs/test/current-coverage/{spec,plan,tasks}.md` |
| Pytest / settings | `multimedia/settings_test.py`, `conftest.py`, `pytest.ini`, `docs/TDD.md`, `requirements-dev.txt` |
| Fixtures | New helpers under `multimedia/api/tests/` or per-app `tests/` (model_bakery recipes) |
| Songs API | `multimedia/api/songs/`, `multimedia/songs/` |
| Bookmarks API | `multimedia/api/bookmarks/` (incl. `validators.py`), `multimedia/bookmarks/` |
| Tatib API | `multimedia/api/tatib/serializers.py` (`insert_after` scope fix), `multimedia/tatib/` |
| Bible API | `multimedia/api/bible/` |
| Search API | `multimedia/api/search/` (Postgres FTS) |
| Router | `multimedia/api/routers.py`, URL conf |
| JS helpers | `static/helpers/*.js` + colocated `*.test.js` |
| OBS BC / storage | `multimedia/obs/static/obs/**/bc.js`, `*-storage.js`, `*-manager.js`, options/settings |
| Project source | `multimedia/obs/static/obs/project/source/` |
| Web UI | `multimedia/web/static/web/songs/`, `multimedia/web/static/web/tatib/` |
| OBS docks | hotkeys/controls under `multimedia/obs/static/obs/{songs,bible,tatib}/dock/` |
| Changelog | `CHANGELOG.md` |

## Contracts

### API (assert via HTTP)

- Unauthenticated CRUD allowed on all ModelViewSets under `/api/`.
- Songs: nested `book` on read; `book_id` on write; filters `?book=`; short-name
  and uniqueness rules as models/validators define.
- Bookmarks: `verse` = comma-separated integers; `verse_info` maps missing
  verses to empty lyric; uniqueness of active `name`+`date` (nullable date
  included); updates exclude self.
- Tatib items: `insert_after` optional order_number; shift scoped to same
  `tatib`; reorder POST updates `order_number` list.
- Bible: nested filters used by OBS (version abbreviation, book name,
  translation, chapter, verse); `omit=` DynamicFields.
- Search: `q` length ≥ 3; phrase FTS on `Verse.lyric`; page size 50.
- Optional trailing slash accepted.

### JS / OBS

- `rx.js`: BehaviorSubject wrapper skips `undefined` until first real value;
  still exposes `next` / `getValue`.
- BC helpers: stable payload field names for songInfo / passage / tatibItem /
  status / control.
- Storage managers: load/save/clear round-trip through localStorage.
- Project source: bible title `"{bookName} {chapterNumber} : {verseNumber}"`
  (+ passage title when present); songs path remains lyric-focused as coded.

### Bugfixes (TDD)

1. `UniqueForNullableDateValidator` — exclude current instance on update.
2. `TataIbadahItemSerializer.create` — filter shift queryset by `tatib=tatib`.

## Risks and rollout

- **Risks:**
  - Postgres must be up (`docker compose up -d db` via docker-vm) or pytest
    fails to connect; document clearly.
  - pytest-django creates/destroys `test_multimedia` — must not point
    `NAME` at the live `multimedia` DB without the test_ prefix behavior.
  - Tier 3 DOM tests can become brittle if they over-assert Semantic UI markup;
    prefer behavior (API calls fired, subjects updated, BC posts).
  - Search / FTS edge cases may differ slightly by Postgres version; assert
    phrase presence, not exact rank floats.
- **Migrations / backfill:** none (test + two logic fixes only).
- **Feature flags / gradual rollout:** N/A; suite is local until CI exists.

## Non-goals

- Auth, admin, seeders, CI Actions, E2E OBS browser automation, new product
  features beyond the two fixes, replacing the test stack.


</details>

## TDD

- Domain/app tests: existing suite must stay green (no new tests).
- E2E (tool named after stack exists): N/A for docs-only migration.

## Risks

- Cross-refs in code/docs still mention legacy `TEST-COV` — intended; follow-up may update them.
