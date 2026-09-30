# Spec: Current test coverage

- **ID:** 017
- **Status:** Accepted
- **Item:** [ITEM-000](../../backlog/items/ITEM-000-adopt-vexbook.md)
- **Plan:** [./plan.md](./plan.md)
- **Tasks:** [./tasks.md](./tasks.md)
- **Bump:** none
- **Legacy:** `TEST-COV` migrated from `specs/test/current-coverage/` (vexbook adopt `v0.4.0`; see `docs/adr/0001-adopt-vexbook-process.md`)

## Intent

Migrated as-built from legacy `TEST-COV` with no behavior change. Original
problem/goal and acceptance criteria are preserved verbatim below for
traceability. New work uses Given / When / Then in this file going forward.

## Scope

### In scope

- Preserve legacy `TEST-COV` intent (spec/plan/tasks) under the vexbook `NNN` layout.
- Keep legacy `CODE`, `CODE-US*`, `CODE-AC*`, `CODE-T*` refs readable for traceability.

### Out of scope

- Behavior changes (none in this migration).
- Retiring legacy `CODE` cross-refs in code/tests (follow-up if wanted).

## Domain rules

- This migration is docs-only (`bump: none`).
- If future behavior changes this area, update this `NNN` spec first per `docs/PROCESS.md`.

## Acceptance scenarios

### Scenario: legacy intent preserved

- **Given** the legacy spec at `specs/test/current-coverage/`
- **When** comparing with this `NNN` pack
- **Then** problem/goal, user stories, and acceptance criteria are preserved verbatim below

### Scenario: suite stays green

- **Given** docs-only migration
- **When** running `pytest` and `npm test`
- **Then** existing suites pass with no behavior change

## Traceability

- Domain/app tests: existing `pytest` suite (`multimedia.settings_test`) and Vitest suite — no new tests for migration.
- E2E: N/A (docs-only migration).
- Implementation: this migration (adopt PR).

---

## Migrated as-built (verbatim from `specs/test/current-coverage/spec.md`)

# Spec: TEST-COV — Current-state test coverage

| Field | Value |
|-------|--------|
| **Spec ID** | `TEST-COV` |
| **Area** | `test` |
| **Status** | `active` |
| **Folder** | `specs/test/current-coverage/` |

## Problem / goal

Almost all product behavior in this worship multimedia app is untested. The
suite today only covers env-safety helpers and toolchain smoke checks. We need
a comprehensive regression suite that locks in the **current** intended
behavior of the API, shared helpers, OBS projection surfaces, and web content
UI — so future changes can follow TDD against a known baseline.

This work does **not** add product features. Two small correctness bugs that
correct tests will expose SHALL be fixed as part of making the suite describe
intended behavior (see acceptance criteria).

## User stories

- **TEST-COV-US1:** As a developer, I want API contracts and domain rules covered
  by pytest, so that CRUD, filters, reorder, and search keep working across
  refactors.
- **TEST-COV-US2:** As a developer, I want isolatable OBS/web JavaScript covered
  by Vitest, so that BroadcastChannel payloads, storage managers, hotkeys, and
  projection formatting do not regress silently.
- **TEST-COV-US3:** As an operator running local Compose, I want pytest to use
  Postgres (including song search FTS), so that tests match production database
  capabilities.
- **TEST-COV-US4:** As a maintainer, I want specs and tasks for this coverage
  effort, so that agents and humans can implement in small verified slices.

## Acceptance criteria (EARS)

### Tooling

- **TEST-COV-AC1:** THE system SHALL run the Django test suite against Postgres
  (Compose host port per `docs/TDD.md`, pytest-django `test_*` database), not
  in-memory SQLite.
- **TEST-COV-AC2:** WHEN song search tests run, THE system SHALL exercise
  Postgres full-text search (`SearchVector` / phrase `SearchQuery`) successfully.
- **TEST-COV-AC3:** THE project SHALL document how to start Compose Postgres and
  run `pytest` / `npm test` for this suite in
  [`docs/TDD.md`](../../../docs/TDD.md).
- **TEST-COV-AC4:** THE project MAY add `model_bakery` as a small test fixture
  helper; THE agent SHALL NOT add large uncommon test frameworks.

### Auth (intentional)

- **TEST-COV-AC5:** THE API SHALL remain unauthenticated (no login required for
  CRUD) — see `API-ACCESS`.
- **TEST-COV-AC6:** WHEN an unauthenticated client calls documented API
  endpoints, THE system SHALL allow access (tests SHALL assert this current
  policy).

### Tier 1 — API / domain

- **TEST-COV-AC7:** THE suite SHALL cover songs books / songs / verses CRUD,
  list filters, write via `book_id`, uniqueness constraints, and short-name
  validation (`API-SONGS`).
- **TEST-COV-AC8:** THE suite SHALL cover bookmark CRUD, date / active /
  `has_date` filters, name uniqueness for nullable dates among active
  bookmarks, item auto `order_number`, comma-separated `verse` validation,
  `verse_info` / `song_info` shapes (including missing verse → empty lyric),
  and reorder (`SONGS-BM`).
- **TEST-COV-AC9:** WHEN updating an existing bookmark without changing its
  unique name+date, THE system SHALL accept the update (exclude self from
  uniqueness check).
- **TEST-COV-AC10:** THE suite SHALL cover tatib CRUD, filters, item types
  (TEXT / END_OF_SECTION), append create, `insert_after` create, and reorder
  (`API-TATIB`).
- **TEST-COV-AC11:** WHEN creating a tatib item with `insert_after`, THE system
  SHALL shift only items belonging to the **same** tatib with `order_number`
  greater than `insert_after`, then assign the new item `insert_after + 1`.
- **TEST-COV-AC12:** THE suite SHALL cover bible langs / versions / books /
  translations / verses CRUD and the nested query filters OBS uses, including
  DynamicFields `omit=` (`API-BIBLE`).
- **TEST-COV-AC13:** THE suite SHALL cover `GET /api/search/songs` (`q`
  minimum length 3, phrase match, page size 50) (`API-SEARCH`).
- **TEST-COV-AC14:** THE suite SHALL cover optional trailing-slash routing for
  API endpoints (`API-ACCESS`).

### Tier 2 — Isolatable JavaScript

- **TEST-COV-AC15:** THE suite SHALL cover `static/helpers` behavior that is
  unit-testable (`rx.js` skip-while-undefined BehaviorSubject, hotkeys,
  local-storage, state-value, arrays, date-util, colour, and other pure helpers
  as applicable).
- **TEST-COV-AC16:** THE suite SHALL cover OBS BroadcastChannel post/subscribe
  message shapes for songs, bible, and tatib.
- **TEST-COV-AC17:** THE suite SHALL cover bookmark / bible-history / tatib /
  display-options / project-settings storage manager round-trips (localStorage
  + subjects).
- **TEST-COV-AC18:** THE suite SHALL cover project source title formatting
  (bible `Book chapter : verse` with optional passage title; songs
  lyric-focused display contract as implemented) (`OBS-PROJECT`).

### Tier 3 — Web / OBS UI wiring

- **TEST-COV-AC19:** THE suite SHALL cover web content UI modules that can be
  isolated with mocked axios / DOM: songs books/songs/verses and tatib
  list/items happy paths (create/edit/delete/reorder flows that call the API).
- **TEST-COV-AC20:** THE suite SHALL cover OBS dock control and hotkey wiring
  that can be isolated without a full OBS browser source (prev/next/toggle
  mappings and control message posting).
- **TEST-COV-AC21:** THE suite SHALL NOT rely on brittle full-page Semantic UI
  snapshots as the primary assertion style.

### Process / docs

- **TEST-COV-AC22:** THE change SHALL live under
  `specs/test/current-coverage/` (`spec.md`, `plan.md`, `tasks.md`) and stay
  updated if intent shifts during implementation.
- **TEST-COV-AC23:** WHEN the coverage work lands, THE changelog SHALL gain an
  `## Unreleased` bullet with area label `[test]` (and `[fix]` if the two
  bugfixes ship in the same PR).

## Out of scope

- Adding authentication or changing the open-API policy.
- New product features beyond the two correctness fixes above.
- Django admin coverage.
- Seeder / ops script coverage.
- CI / GitHub Actions wiring (local suite only for now).
- Replacing Vitest or pytest with another framework.
- Full end-to-end browser automation against a live OBS instance.

## Constraints

- Follow [`specs/constitution.md`](../../constitution.md) and linked docs
  (TDD, Git Flow, deploy, versioning).
- Branch from `develop` as `chore/test-current-coverage` (tooling + tests; bug
  fixes are incidental to correct coverage).
- Prefer existing patterns in `docs/TDD.md`; update that doc when Postgres test
  settings replace SQLite.
- Docker for local Postgres remains VirtualBox `docker-vm` / Compose — do not
  assume Docker Desktop.
- Related product specs: `API-*`, `SONGS-BM`, `OBS-*`, `WEB-*`, `APP`.

## Notes

- Bookmark `verse` is a comma-separated integer list string
  (`validate_comma_separated_integer_list`); OBS builds it via
  `JSON.stringify(selectedVerses).slice(1, -1)`.
- Tatib `insert_after` is an **order_number**, not an item primary key.
- Prior empty stubs: `multimedia/songs/tests.py`,
  `multimedia/bookmarks/tests.py`.
- Agreed clarifications (session): auth stays open long-term; Postgres test
  settings required; Tiers 1–3 all in scope; SDD specs required; uniqueness
  self-exclude and tatib-scoped `insert_after` are intended fixes.

