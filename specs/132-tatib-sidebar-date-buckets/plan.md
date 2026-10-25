# Implementation Plan: The Tata Ibadah list groups by age, not by month

**Spec**: `specs/132-tatib-sidebar-date-buckets/spec.md`
**Branch**: `feat/132-tatib-sidebar-date-buckets`
**Bump**: `patch`
**Preview**: `specs/132-tatib-sidebar-date-buckets/preview/` — the running branch, a seeded demo instance,
and the probe that measured both

*Sequencing note*: the owner reviewed the change on a running branch while the design was settled (labels,
order, dock scope, badge treatment), so the working tree already carries the implementation. Gate 1
accepted the spec afterwards; this plan, the tasks and the convergence record are written against it.

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0 templates; ES5-style browser JavaScript (no build step) |
| Primary dependencies | Django template engine; `static/styles/design/tokens.css`, `components.css`, `obs-dock.css`; `zoneinfo` (stdlib); no new library |
| Storage | none — the bucket is derived per render from `TataIbadah.date` and the present day |
| Testing | Django `TestCase` for the rule, the panel markup and the dock; Playwright (Python) E2E for the saved render and the filter |
| Target platform | the reading shell at any width, the dock at dock width, light and dark themes |
| Project type | server-rendered pages + an in-page navigation that swaps shell fragments |
| Performance goals | no new query: the panel's existing query is partitioned in Python; the dock's likewise |
| Constraints | the saved render must keep parity with the server route (spec 122/129); the repo runs on UTC, so the bucket day is taken in `Asia/Jakarta` as the media code already does |
| Scale / scope | 1 new module, 2 views, 3 templates, 2 stylesheets, 2 JS files, 2 unit test modules + 1 new |

## Constitution Check

`n/a — no CONSTITUTION.md in this repository` (SDD-01: optional, never auto-created).

Re-checked after Phase 1: nothing to check against; the repo's `docs/PROCESS.md` rules were applied instead
(one slice, one branch, tests before the claim, no commit before Fold).

## Phase 0 — Research

See `research.md` — seven decisions, **unknowns remaining: 0**.

## Phase 1 — Design

- `data-model.md` — the derived bucket record, its boundary table and the three row shapes
- `contracts/` — `none`: the panel's `tatib_groups` context, the dock's `groups` context and the
  `data-bucket` attribute are internal to this repository's own templates, not an external interface
- `quickstart.md` — serve the worktree, seed the demo instance, read the buckets and measure them

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/date_buckets.py` (`BUCKETS`), `_tatib_panel.html` | `test` → `multimedia/web/tests.py::ReadingViewTests::test_tatib_list_buckets_its_services_by_age` | the four labels, in order |
| FR-002 | `date_buckets.bucket_key` | `test` → `multimedia/web/test_date_buckets.py::DateBucketRuleTests` (6 tests) | day 0 · 1 · 30 · 31 · cross-year · leap day |
| FR-003 | `date_buckets.present_day` | `inspection` — two lines, `timezone.now().astimezone(ZoneInfo('Asia/Jakarta')).date()`, the convention the media views already use | the day itself is a clock read, not a behaviour |
| FR-004 | `date_buckets.groups` (stable partition) | `test` → `…::test_tatib_list_buckets_its_services_by_age` | today, then +60, then +6 |
| FR-005 | `date_buckets.groups` (empty buckets dropped), `_tatib_panel.html` | `test` → `…::test_tatib_list_draws_no_heading_for_a_bucket_without_rows` | one heading when only one bucket has rows |
| FR-006 | `views.obs_dock`, `obs_dock.html`, `obs-dock.css` | `test` → `multimedia/web/test_obs_dock.py::ObsSurfacesTest::test_the_dock_picker_names_the_same_date_buckets_as_the_reading_panel` | four labels, one badge, no tint class |
| FR-007 | `static/web/offline-render.js` (`TATIB_BUCKETS`, `jakartaToday`, `tatibBucket`, `servicePanel`) | `test` → `tests/e2e/test_saved_render_parity.py` (run at the push step); `inspection` — the JS rule reads boundary-for-boundary like `bucket_key` | |
| FR-008 | `_tatib_panel.html`, `offline-render.js`, `static/web/reading.js` (`nodeIdentity`) | `test` → `…::test_tatib_list_buckets_its_services_by_age` asserts `data-bucket` present and `data-month` absent | |
| FR-009 | `static/web/reading.js::applyFilter` (untouched) | `test` → `tests/e2e/test_reading.py` filter suites (existing, run at the push step); `inspection` — the filter counts `.book` rows per `.group` and toggles `is-hidden`, no bucket knowledge | |
| FR-010 | `views._tatib_groups` template branch, `_tatib_panel.html` | `test` → `multimedia/web/tests.py` template-mode tests (existing, unchanged) | verified on the running branch too: one `Templates` heading, no `data-bucket` |
| FR-011 | `static/styles/design/components.css` (`.group__head`, `.group + .group` untouched) | `inspection` — probe prints `2px` / `10px` / `10px` and 11.5px uppercase sticky | |
| FR-012 | `_tatib_panel.html` (badge), `components.css` (`.book__today`), `views._tatib_groups` (`today` flag) | `test` → `…::test_a_today_row_carries_the_today_badge_and_no_other_row_does` | exactly one badge; the aria-label ends `— today` |
| FR-013 | `offline-render.js` (`bookLink` badge branch, `today` flag in `servicePanel`) | `test` → `tests/e2e/test_saved_render_parity.py` (push step); `inspection` — same day, same class | |
| SC-001 | the served `/tatib/` markup | `test` → the bucket test's label assertion; probe output | four headings, once each |
| SC-002 | `date_buckets.bucket_key` | `test` → the six rule tests | |
| SC-003 | `date_buckets.groups` | `test` → the bucket test's order assertion | |
| SC-004 | `/obs/dock` markup | `test` → the dock test | |
| SC-005 | saved render | `test` → `test_saved_render_parity.py` (push step) | accepted gap until then |
| SC-006 | whole app | `test` → `multimedia` suite, 411 tests | green on the branch |

**Verification split**: 11 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| The bucket rule exists twice — Python in `date_buckets.py`, JavaScript in `offline-render.js` | a saved page is rebuilt in the browser from the cached library and has no server to ask | fetching the route's buckets would put a network round-trip on the offline path |
| The badge's twelve CSS lines exist twice — `.book__today`, `.servicerow__today` | the reading shell loads `components.css`, the dock loads `obs-dock.css`; neither loads the other | linking the reading shell's sheet into the dock would pull the whole shell's rules into a panel that has its own accepted design |

## Project Structure

### Documentation

```
specs/132-tatib-sidebar-date-buckets/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/reading/date_buckets.py          BUCKETS, present_day, bucket_key, groups
multimedia/web/reading/views.py                 _tatib_groups (bucket groups + today flag); obs_dock (buckets)
multimedia/web/templates/reading/_tatib_panel.html      data-bucket, Today badge, aria-label
multimedia/web/templates/reading/obs_dock.html          data-bucket, Today badge, tint classes removed
static/styles/design/components.css             .book__today
static/styles/design/obs-dock.css               .servicerow__today; the two tint rules deleted
static/web/reading.js                           nodeIdentity keeps data-bucket instead of data-month
static/web/offline-render.js                    the rule, the today day, the buckets and the badge
multimedia/web/tests.py                         two panel tests, one badge test
multimedia/web/test_date_buckets.py             the rule's six boundary tests
multimedia/web/test_obs_dock.py                 the dock's bucket test
specs/132-…/preview/probe_date_buckets.py       the measurement probe
specs/132-…/preview/seed_demo_data.py           the throwaway demo dataset
```

### Structure Decision

The rule gets its own module rather than another block in `views.py`, because two views and a test module
now consume it, and `views.py` is already 1,940 lines. The templates and stylesheets stay where they are:
no new file is fetched by a page, and the badge is a rule on an existing row component.
