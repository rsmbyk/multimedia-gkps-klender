# Tasks: The Tata Ibadah list groups by age, not by month

**Spec**: `specs/132-tatib-sidebar-date-buckets/spec.md`
**Plan**: `specs/132-tatib-sidebar-date-buckets/plan.md`
**Verification split**: 11 test · 4 inspection · 0 manual

## Phase 1 — Setup

- [X] T001 `specs/132-tatib-sidebar-date-buckets/preview/probe_date_buckets.py` — the headless probe that
  prints each bucket's key, heading, row count and first/last row, the heading's drawn form and the
  divider's measured box, and saves a screenshot
- [X] T002 `specs/132-tatib-sidebar-date-buckets/preview/seed_demo_data.py` — one service per boundary in a
  throwaway SQLite database, so all four buckets and the today pin are visible on one screen

## Phase 2 — Foundational

- [X] T003 `multimedia/web/reading/date_buckets.py` — `BUCKETS`, `LABELS`, `RECENT_DAYS`, `present_day`
  (`Asia/Jakarta`), `bucket_key`, `groups` (bucket order, empty buckets dropped, today-first stable
  partition)

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: the dated list groups into the four age buckets, each drawn only while it holds rows.
**Independent test**: open `/tatib/` with a service in each bucket; four headings in order, none empty.

- [X] T004 [P] [US1] `multimedia/web/test_date_buckets.py` — the rule's six boundary tests (today, +1,
  −1, −30, −31, previous year, early-January cross-year, leap day)
- [X] T005 [P] [US1] `multimedia/web/tests.py::ReadingViewTests::test_tatib_list_buckets_its_services_by_age`
  — labels, order, membership, `data-bucket` present and `data-month` gone
- [X] T006 [US1] `multimedia/web/reading/views.py::_tatib_groups` — the dated branch builds its groups
  through `date_buckets.groups`
- [X] T007 [US1] `multimedia/web/templates/reading/_tatib_panel.html` — `data-bucket` replaces `data-month`
- [X] T008 [US1] `static/web/reading.js::nodeIdentity` — the reconciler keys on `data-bucket`

## Phase 4 — US2 (P1)

**Goal**: today's rows lead `Upcoming`, then the future farthest-first; every other bucket stays newest
first.

- [X] T009 [P] [US2] `multimedia/web/tests.py::ReadingViewTests::test_tatib_list_buckets_its_services_by_age`
  — the order assertion (today, +60, +6)
- [X] T010 [US2] `date_buckets.groups` — the stable partition (`sort(key=date != today)`)
- [X] T011 [P] [US2] `multimedia/web/tests.py::ReadingViewTests::test_tatib_list_draws_no_heading_for_a_bucket_without_rows`
  — one heading when one bucket has rows

## Phase 5 — US3 (P2)

**Goal**: the dock's picker names dates the same way, and marks today with the same badge instead of tints.

- [X] T012 [P] [US3] `multimedia/web/test_obs_dock.py::ObsSurfacesTest::test_the_dock_picker_names_the_same_date_buckets_as_the_reading_panel`
  — four labels, exactly one badge, no tint class, no `is_upcoming`
- [X] T013 [US3] `multimedia/web/reading/views.py::obs_dock` — groups through `date_buckets.groups`, sets
  `is_today`, drops `is_upcoming`
- [X] T014 [US3] `multimedia/web/templates/reading/obs_dock.html` — `data-bucket`, the badge, the tint
  classes removed
- [X] T015 [US3] `static/styles/design/obs-dock.css` — the two tint rules deleted, `.servicerow__today`
  added in step with `.book__today`

## Phase 6 — US4 (P2)

**Goal**: the saved copy draws the same buckets, the same row order and the same badge.

- [X] T016 [US4] `static/web/offline-render.js` — `TATIB_BUCKETS`, `jakartaToday`, `isoDay`, `utcDays`,
  `tatibBucket`, the today-first partition, and `bookLink`'s badge branch
- [X] T017 [US4] `tests/e2e/test_saved_render_parity.py` — the parity fields extended with the panel's
  headings, bucket keys and today badges (written; run at the push step)

## Phase 7 — Polish

- [X] T018 [P] `multimedia/web/tests.py::ReadingViewTests::test_a_today_row_carries_the_today_badge_and_no_other_row_does`
  — one badge, the `— today` accessible name, no badge elsewhere
- [X] T019 [P] `static/styles/design/components.css` — `.book__today`, the chosen treatment (solid
  `--active-bg` / `--active-ink`)
- [X] T020 `tests/e2e/test_reading.py::ReadingE2ETests::test_the_tata_ibadah_panel_buckets_its_services_by_age`
  — the four headings, the today-first order and the single badge in a browser (written; run at the push
  step)
- [X] T021 Docs: `CHANGELOG.md`, `VERSION`, `docs/spec/reading.md` (`R9`), `backlog/` — at Fold

## Phase 8 — Convergence

See `converge.md`. The fold is `docs/spec/reading.md` `R9`, recorded in `fold.md`.
