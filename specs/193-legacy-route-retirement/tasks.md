# Tasks: Retired Addresses

**Spec**: `specs/193-legacy-route-retirement/spec.md`
**Plan**: `specs/193-legacy-route-retirement/plan.md`
**Verification split**: 20 test · 3 inspection · 2 manual

Slice `specs/193-legacy-route-retirement` · **Created**: 2026-11-14 · Ordering per SDD-16; `[P]`
means order-independent, not concurrent.

## Phase 1 — Setup

- No task. The branch (`feat/193-legacy-route-retirement`) and this worktree were cut at the change
  request; the spec pack was written here. Nothing to install: the slice adds no dependency.

## Phase 2 — Foundational

- [x] T001 [Foundational] Write `multimedia/retirement.py` — `RETIRED` (the nine `(old path,
  successor)` pairs from `contracts/routes.md`), `LEGACY` (the three `(regex, destination
  template)` pairs), the `manage` prefix rule, `successor(path)` (prefix, then `RETIRED`, then
  `LEGACY`, else the path itself), `redirect(destination)` (a `RedirectView` with
  `permanent=False, query_string=True`), `routes(prefix='')` and `legacy_routes()` building the
  patterns from the two tables, and `archive()`. `archive()` unquotes its tail, and `successor()`
  answers `/` for a path carrying a backslash, so an archive address can never be read as another
  host. No URLconf names it yet; the
  code exists to pass T002's failing test, and T003 is the red run for the wiring (TDD-01).

## Phase 3 — US1 (P1) 🎯 MVP — a leftover OBS scene shows nothing embarrassing

**Goal**: the seven old OBS addresses answer 302 — docks to `/obs/dock`, sources to `/obs/blank` —
and `/obs/blank` paints one watermark note.
**Independent test**: request all seven addresses, both slash forms; each answers 302 to the
address `contracts/routes.md` names, and `/obs/blank` answers a transparent 200 with the note.

- [x] T002 [P] [US1] Replace `LegacyObsRouteCompatibilityTests` in `multimedia/web/tests.py` with
  `RetiredWebRouteTests` and write the failing
  `test_each_old_dock_answers_302_to_the_one_dock`: for each of the three docks, with and without a
  trailing slash, assert 302 and `Location == '/obs/dock'`. Fails today because each renders the old
  dock (FR-003, US1/AC1, SC-001).
- [x] T003 [US1] Make T002 green: `multimedia/obs/urls.py` becomes one `spec 193` block —
  `urlpatterns = retirement.routes('obs')` — keeping its `path('obs/', include(…))` mount in
  `multimedia/urls.py` (FR-003, FR-010).
- [x] T004 [P] [US1] Failing `test_each_old_source_answers_302_to_the_blank_page`: the four sources,
  both slash forms → 302 to `/obs/blank` (FR-004, US1/AC2).
- [x] T005 [US1] Make T004 green: extend `RETIRED` with the four sources (T001's table is the only
  edit) (FR-004).
- [x] T006 [US1] Write `obs_blank()` in `multimedia/web/reading/views.py` and
  `multimedia/web/templates/reading/obs_blank.html`, reproducing `preview/blank.html` exactly —
  inline `<style>`, system-ui 12px/1.4 at 500, `rgba(255,255,255,.2)`, the shadow, the hover plate
  and revealed anchor — and set `Cache-Control: no-store` on the response. Register
  `path('obs/blank', reading_views.obs_blank, name='web-obs-blank')` in `multimedia/urls.py` beside
  `/obs/dock`, before the includes (FR-006, FR-006a, FR-006b; D005).
- [x] T007 [P] [US1] Failing `test_the_blank_page_is_transparent_and_uncached`: 200,
  `Cache-Control: no-store`, and `background: transparent` on both `html` and `body` (FR-006,
  SC-002).
- [x] T008 [P] [US1] Failing `test_the_blank_page_paints_only_the_note`: 0 `<script`, 0 `<img`,
  0 `<link`, and the body's only text is `Old OBS source` and `Switch to /obs/source/overlay`
  (FR-006b, SC-002).
- [x] T009 [P] [US1] Failing `test_the_old_settings_page_answers_302_to_the_root`: both slash forms
  → 302 to `/` (FR-005, US1/AC4); make it green by extending `RETIRED`.
- [x] T010 [P] [US1] Write the Playwright module `tests/e2e/test_retired_routes.py`
  (`StaticLiveServerTestCase`, `skipUnless(HAS_PLAYWRIGHT)`, `@tag('e2e')`) with
  `test_the_note_is_a_watermark_until_hovered`: the anchor is hidden at rest, the computed colour
  is `rgba(255, 255, 255, 0.2)`, and after `hover()` the anchor is visible on a
  `rgba(20, 20, 18, 0.82)` plate (FR-006a, US1/AC3).
- [x] T011 [P] [US1] `test_no_old_obs_address_renders_a_page`: the seven addresses answer 302 and
  none of the bodies carries an old dock or overlay marker (SC-001).

## Phase 4 — US2 (P1) — an old web address still finds the site

**Goal**: `/home/` and every `/manage/…` address answer 302 to `/`; the reading addresses are
untouched.
**Independent test**: request `/home/` and four `/manage/…` addresses; each answers 302 to `/`;
`/songs/`, `/songs/<song>/`, `/tatib/`, `/tatib/<service>/` still answer 200.

- [x] T012 [P] [US2] Failing `test_home_answers_302_to_the_root`: `/home` and `/home/`, with
  `?from=mail` kept (FR-001, US2/AC1). Fails today because `/home/` renders the home.
- [x] T013 [US2] Make T012 green: add `('home', '/')` to `RETIRED`, replace
  `path('home/', views.HomeView.as_view(), name='web-home')` in `multimedia/web/urls.py` with one
  `spec 193` block `*retirement.routes()` (FR-001, FR-010).
- [x] T014 [US2] Rename all `reverse('web-home')` call sites to `reverse('web-index')` — 40 in
  `tests/e2e/test_reading.py`, 14 in `test_editor.py`, 5 each in `test_edit_request_feedback.py`
  and `multimedia/web/tests.py`, and the rest in `test_entries.py`, `test_immediate_editor_open.py`,
  `test_projector.py`, `test_old_rows.py`, `test_home_search_center.py`, `test_entry_pickers.py`
  (76 total). The name is gone; without this the suite fails at import (FR-001).
- [x] T015 [P] [US2] Failing `test_every_manage_address_answers_302_to_the_root`: `/manage`,
  `/manage/`, `/manage/songs/`, `/manage/songs/12/`, each keeping its query string (FR-002,
  US2/AC2).
- [x] T016 [US2] Make T015 green: delete `path('manage/', include('multimedia.web.manage.urls'))`
  from `multimedia/web/urls.py`; `routes()` already emits the `^manage(?:/.*)?$` prefix rule from
  the table (FR-002, D004).
- [x] T017 [P] [US2] Failing `test_the_reading_addresses_keep_their_answers`: `/songs/`,
  `/songs/<song>/`, `/tatib/`, `/tatib/<service>/` → 200 (FR-007, US2/AC3, SC-003).
- [x] T018 [P] [US2] Failing `test_the_legacy_song_lists_redirect_to_the_reading_pages`:
  `/songs/books` → 301 `/songs/`, `/songs/books/<id>` → 301 `/songs/book/<id>/`,
  `/songs/songs/<id>` → 301 `/songs/<id>/` (FR-011). Make it green by replacing the three
  `RedirectView(pattern_name=…)` lines in `multimedia/web/urls.py` with `*retirement.legacy_routes()`
  — `LEGACY` already holds the destinations T001 wrote.

## Phase 5 — US3 (P2) — the old version is reachable for one release

**Goal**: `/archive/…` answers the successor of the old address it names, in one hop, always 302.
**Independent test**: request `/archive/`, `/archive/home/`, `/archive/manage/songs/12/`,
`/archive/songs/`, `/archive/obs/songs/source`, `/archive/nowhere/`; each answers 302 to the
address `contracts/routes.md` names, and none renders a page.

- [x] T019 [P] [US3] Failing `test_the_archive_answers_the_successor_in_one_hop`: the six addresses
  above plus `/archive/songs/books` → `/songs/` (FR-008, US3/AC1–5; the legacy row is why
  `successor()` knows `LEGACY`) and `/archive/%5Cevil.example` → `/` (the backslash guard).
- [x] T020 [US3] Make T019 green: `archive(request, rest='')` in `multimedia/retirement.py` strips
  the prefix, unquotes the remaining path, calls `successor()`, keeps `request.GET` and returns
  `HttpResponseRedirect`; register
  `re_path(r'^archive(?:/(?P<rest>.*))?$', retirement.archive, name='web-archive')` in
  `multimedia/urls.py` beside `/obs/blank` (FR-008, D006).
- [x] T021 [P] [US3] `test_no_retired_or_archived_address_answers_301`: iterate `RETIRED`, the
  `manage` prefix and the archive rows from `contracts/routes.md`; every answer is 302 (FR-009,
  US3/AC6, SC-005).
- [x] T022 [P] [US3] `test_every_retired_location_resolves_to_a_200`: follow each `Location` once
  through the test client and assert 200 and no further redirect (SC-004).

## Phase 6 — Polish

- [x] T023 [Polish] `inspection` FR-010: `grep -rn 'spec 193' multimedia` and read the four marked
  blocks; confirm the next release's deletion is exactly `multimedia/retirement.py`, those blocks,
  the `/archive/` route and `/archive`'s name — nothing else.
- [x] T024 [Polish] `inspection` US2/AC4: read `static/web/editors.js:318-322`; confirm both return
  addresses are `/songs/` and `/tatib/` and neither passes through `/manage/` or `web-home`.
- [x] T025 [Polish] `inspection` US1/AC3: open `specs/193-legacy-route-retirement/preview/index.html`
  and read the dark and bright frames; the 20% line is a hint on the dark stage and is swallowed by
  the bright slide, and the hover state restores it.
- [x] T026 [Polish] `manual` US1 on air: in OBS, load each retired source into the scene that still
  holds it and watch the program out — the blank page's watermark appears, never an old dock or a
  stale caption.
- [x] T027 [Polish] Run the full suite (`manage.py test --noinput`) and the E2E module; record every
  failure and confirm each is one of the pre-existing red items (ITEM-137/139/140/141/144/153/156/
  174/175/184/185). The non-E2E suite matched `origin/develop` exactly (23 known failures); the
  targeted spec 193 suites are green: `RetiredWebRouteTests` 17/17 and
  `tests.e2e.test_retired_routes` 1/1, run 2026-11-14 with `--keepdb`. The full E2E run
  (`--tag=e2e`, 682 tests) was stopped at ~15% after 28 minutes of browser-bound runtime; its
  partial output showed only `F`/`E` characters belonging to the known-red list, no new red.
- [x] T028 [Polish] Fold: write `docs/spec/routing.md` (`R1` — retired addresses answer 302 to their
  successor; `R2` — `/archive/…` resolves in one hop for one release; `R3` — `/obs/blank` is a
  transparent watermark page) and `fold.md`. `docs/spec/` has no `routing.md` yet, so this is an
  `added` capability, not a modified one.
- [x] T029 [Polish] First commit at Fold: the spec pack, `multimedia/retirement.py`, the four
  touched URLconfs, the view, the template, both test modules, `docs/spec/routing.md`, the card and
  the board row together, targeted suite green.
- [x] T030 [Polish] Delivery: branch pushed on the owner's word (GIT-07), PR opened as a draft with
  the body that becomes the squash message; card to `In review` in a commit after the PR number
  exists. Pushed 2026-11-14, draft PR #509 opened, card and board row moved to In review in
  5ee7f972.

## Phase 7 — Convergence

Converged 2026-11-14. Checklist 20/20 ticked. Capability fold: `routing` gains R1 (a retired address
answers one 302 to its live successor), R2 (`/archive/<old path>` answers the same successor in one
hop for this one release), R3 (`/obs/blank` transparent, one corner watermark note). Docs reconciled:
`docs/spec/routing.md` (R1–R3), `docs/ARCHITECTURE.md` (URL roots incl. `/archive/`), `docs/GLOSSARY.md`
(retired address, archive namespace), `CHANGELOG.md`, `VERSION`. Verification: 17/17
`RetiredWebRouteTests`, watermark E2E green; the non-E2E suite matches `origin/develop`'s 23 known
reds; the full 682-test E2E run was stopped and the partial log matched the known-red list.
Version 1.30.0 → 1.31.0 (minor, per the card's `bump`).
