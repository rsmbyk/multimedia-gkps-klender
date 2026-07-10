# Spec: Current-state test coverage

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

- As a developer, I want API contracts and domain rules covered by pytest, so
  that CRUD, filters, reorder, and search keep working across refactors.
- As a developer, I want isolatable OBS/web JavaScript covered by Vitest, so
  that BroadcastChannel payloads, storage managers, hotkeys, and projection
  formatting do not regress silently.
- As an operator running local Compose, I want pytest to use Postgres (including
  song search FTS), so that tests match production database capabilities.
- As a maintainer, I want specs and tasks for this coverage effort, so that
  agents and humans can implement in small verified slices.

## Acceptance criteria (EARS)

### Tooling

- THE system SHALL run the Django test suite against Postgres (Compose
  `localhost:5432`, pytest-django `test_*` database), not in-memory SQLite.
- WHEN song search tests run, THE system SHALL exercise Postgres full-text
  search (`SearchVector` / phrase `SearchQuery`) successfully.
- THE project SHALL document how to start Compose Postgres and run `pytest` /
  `npm test` for this suite in [`docs/TDD.md`](../../../docs/TDD.md).
- THE project MAY add `model_bakery` as a small test fixture helper; THE agent
  SHALL NOT add large uncommon test frameworks.

### Auth (intentional)

- THE API SHALL remain unauthenticated (no login required for CRUD).
- WHEN an unauthenticated client calls documented API endpoints, THE system
  SHALL allow access (tests SHALL assert this current policy).

### Tier 1 — API / domain

- THE suite SHALL cover songs books / songs / verses CRUD, list filters, write
  via `book_id`, uniqueness constraints, and short-name validation.
- THE suite SHALL cover bookmark CRUD, date / active / `has_date` filters, name
  uniqueness for nullable dates among active bookmarks, item auto
  `order_number`, comma-separated `verse` validation, `verse_info` /
  `song_info` shapes (including missing verse → empty lyric), and reorder.
- WHEN updating an existing bookmark without changing its unique name+date,
  THE system SHALL accept the update (exclude self from uniqueness check).
- THE suite SHALL cover tatib CRUD, filters, item types (TEXT /
  END_OF_SECTION), append create, `insert_after` create, and reorder.
- WHEN creating a tatib item with `insert_after`, THE system SHALL shift only
  items belonging to the **same** tatib with `order_number` greater than
  `insert_after`, then assign the new item `insert_after + 1`.
- THE suite SHALL cover bible langs / versions / books / translations / verses
  CRUD and the nested query filters OBS uses, including DynamicFields `omit=`.
- THE suite SHALL cover `GET /api/search/songs` (`q` minimum length 3, phrase
  match, page size 50).
- THE suite SHALL cover optional trailing-slash routing for API endpoints.

### Tier 2 — Isolatable JavaScript

- THE suite SHALL cover `static/helpers` behavior that is unit-testable
  (`rx.js` skip-while-undefined BehaviorSubject, hotkeys, local-storage,
  state-value, arrays, date-util, colour, and other pure helpers as
  applicable).
- THE suite SHALL cover OBS BroadcastChannel post/subscribe message shapes for
  songs, bible, and tatib.
- THE suite SHALL cover bookmark / bible-history / tatib / display-options /
  project-settings storage manager round-trips (localStorage + subjects).
- THE suite SHALL cover project source title formatting (bible
  `Book chapter : verse` with optional passage title; songs lyric-focused
  display contract as implemented).

### Tier 3 — Web / OBS UI wiring

- THE suite SHALL cover web content UI modules that can be isolated with mocked
  axios / DOM: songs books/songs/verses and tatib list/items happy paths
  (create/edit/delete/reorder flows that call the API).
- THE suite SHALL cover OBS dock control and hotkey wiring that can be isolated
  without a full OBS browser source (prev/next/toggle mappings and control
  message posting).
- THE suite SHALL NOT rely on brittle full-page Semantic UI snapshots as the
  primary assertion style.

### Process / docs

- THE change SHALL live under `specs/test/current-coverage/` (`spec.md`,
  `plan.md`, `tasks.md`) and stay updated if intent shifts during
  implementation.
- WHEN the coverage work lands, THE changelog SHALL gain an `## Unreleased`
  bullet with area label `[test]` (and `[fix]` if the two bugfixes ship in the
  same PR).

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
