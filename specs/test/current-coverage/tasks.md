# Tasks: Current-state test coverage

Spec: [`spec.md`](spec.md) · Plan: [`plan.md`](plan.md)

Work top to bottom. Check a box when the task and its verification are done.
Each behavior task follows TDD: failing test → fix/implement → refactor.

## Checklist

- [x] **T1 — Specs agreed (Specify / Plan / Tasks)**
  - Touch: `specs/test/current-coverage/{spec,plan,tasks}.md`
  - Verify: Ronald OK to start Implement; no product code yet in this task

- [x] **T2 — Postgres test settings + docs**
  - Touch: `multimedia/settings_test.py`, `conftest.py`, `docs/TDD.md`,
    `pytest.ini` if needed
  - Verify: with Compose `db` up, `pytest tests/test_toolchain.py -q` passes
    against Postgres (`test_*` DB); docs describe the workflow

- [x] **T3 — Add model_bakery + shared test helpers**
  - Touch: `requirements-dev.txt`, optional `multimedia/conftest.py` or
    `tests/conftest.py` / bakery recipes
  - Verify: `pip install -r requirements-dev.txt`; a tiny smoke test can bake a
    model

- [x] **T4 — Songs API coverage**
  - Touch: `multimedia/songs/tests/` or `multimedia/api/songs/tests/`; remove
    empty stub if replaced
  - Verify: `pytest` for books/songs/verses CRUD, filters, `book_id`,
    uniqueness, short-name validator

- [x] **T5 — Bookmarks API coverage + uniqueness self-exclude fix**
  - Touch: bookmark API tests; `multimedia/api/bookmarks/validators.py`
  - Verify: failing test for update-self uniqueness → fix → green; also create,
    filters, verse CSV, `verse_info`/`song_info`, reorder, unauthenticated access

- [x] **T6 — Tatib API coverage + insert_after same-tatib fix**
  - Touch: tatib API tests; `multimedia/api/tatib/serializers.py`
  - Verify: failing test that other tatib orders must not shift → fix filter →
    green; also CRUD, filters, append, reorder, item types

- [x] **T7 — Bible API coverage**
  - Touch: bible API tests
  - Verify: CRUD + nested filters OBS uses + `omit=` DynamicFields

- [x] **T8 — Song search + trailing slash**
  - Touch: search API tests; router/URL tests as needed
  - Verify: `q` min 3, phrase match, page size 50 on Postgres; optional
    trailing slash works

- [x] **T9 — JS helpers (Tier 2 start)**
  - Touch: colocated `static/helpers/*.test.js` (rx, hotkeys, local-storage,
    state-value, arrays, date-util, colour, others as needed)
  - Verify: `npm test` green for helpers

- [x] **T10 — OBS BC contracts + storage managers**
  - Touch: tests beside `bc.js`, `*-storage.js`, `*-manager.js`, options /
    settings storage
  - Verify: message shapes and localStorage round-trips under Vitest (mocked BC)

- [x] **T11 — Project source formatting**
  - Touch: tests for project source title/lyric formatting logic
  - Verify: bible title format + songs lyric path assertions

- [x] **T12 — Web UI isolatable flows (Tier 3)**
  - Touch: `multimedia/web/static/web/**/*.test.js` with mocked axios/DOM
  - Verify: songs + tatib happy-path create/edit/delete/reorder call expected
    endpoints

- [x] **T13 — OBS dock controls / hotkeys (Tier 3)**
  - Touch: isolatable dock control/hotkey modules under `obs/**/dock/`
  - Verify: prev/next/toggle (and songs modifier variants) map to expected
    actions / BC posts without full OBS

- [x] **T14 — Full suite + changelog**
  - Touch: `CHANGELOG.md` `## Unreleased`
  - Verify: `pytest` and `npm test` both pass; Unreleased bullets for `[test]`
    and `[fix]` as applicable

## Done when

- All acceptance criteria in `spec.md` are met.
- Relevant test suites pass (`pytest` / `npm test`).
- Changelog `## Unreleased` bullet(s) added.
- Spec/plan/tasks remain accurate if any intent changed during implementation.
