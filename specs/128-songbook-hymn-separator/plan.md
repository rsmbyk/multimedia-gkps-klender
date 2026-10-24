# Implementation Plan: Hymn songbooks above a single separator, the rest A–Z

**Spec**: `specs/128-songbook-hymn-separator/spec.md`
**Branch**: `feat/128-songbook-hymn-separator`
**Bump**: `patch`
**Preview**: `specs/128-songbook-hymn-separator/preview/` (live route `/songs/`; approved 2026-10-24)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 · Django 4.0 · ES5-style browser JS |
| Primary dependencies | Django templates, WhiteNoise, `static/web/offline-render.js`, `static/web/reading.js` |
| Storage | PostgreSQL (production) · SQLite (tests); no schema change |
| Testing | Django `TestCase` for the panel context · Playwright (Python) `StaticLiveServerTestCase` for the rendered panel, its spacing, the filter, and saved-copy parity |
| Target platform | Desktop browser; the Kidung panel's open and closed layouts |
| Project type | Server-rendered Django application with a browser-side saved renderer |
| Performance goals | no extra query: the panel keeps its single annotated queryset; the filter stays in-page |
| Constraints | no new element, class or heading; ordering independent of database collation and of browser locale data; the saved renderer must agree with the server |
| Scale / scope | 2 groups, 13 songbooks in this installation; one panel, three server routes, two saved-render call sites |

## Constitution Check

`none — the repository has no CONSTITUTION.md; the process treats the constitution as optional and never
auto-creates it.`

Re-checked after Phase 1: `pass` — no principle exists to violate, and no artifact was created to compensate.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the existing `Songbook` row plus the computed panel group; no new field.
- `contracts/` — `none`: no HTTP, API or model interface changes; the panel is server-rendered markup and an
  internal template context key.
- `quickstart.md` — how to run the branch, the three routes, and the filter states.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py` — `_songbook_groups()` | `test` → `multimedia/web/tests.py::ReadingViewTests::test_songbook_panel_puts_hymn_books_before_the_ordinary_ones` | hymn group first |
| FR-002 | `views.py` — `_songbook_name_key()`, the two sorts | `test` → `…::test_songbook_panel_orders_ordinary_songbooks_by_folded_name` and `…::test_songbook_panel_keeps_the_hymn_order_by_song_count` | folded key + original-name tiebreak |
| FR-003 | `multimedia/web/templates/reading/_songbooks_panel.html` + `static/styles/design/components.css` (`.group + .group`) | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_the_songbook_panel_draws_one_divider_between_the_groups` | measured `2px`, `10px`/`10px` |
| FR-004 | `_songbooks_panel.html` | `test` → `multimedia/web/tests.py::ReadingViewTests::test_songbook_panel_has_no_group_heading` | no `group__head` in `#panelBody` |
| FR-005 | `views.py` (empty group skipped) + `components.css` (`.group.is-hidden + .group`) | `test` → `…::test_songbook_panel_omits_the_separator_when_only_one_group_has_rows` · `tests/e2e/test_reading.py::ReadingE2ETests::test_filtering_the_hymn_group_away_takes_the_divider` | both sides |
| FR-006 | `views.py` three views · `_songbooks_panel.html` | `test` → `…::test_songbook_panel_marks_the_current_row_in_either_group` · `…::test_song_detail_and_book_detail_panels_use_the_same_groups` | `aria-current`, row-edit untouched |
| FR-007 | `static/web/offline-render.js` — `songbookGroups()`, `songbooksPanel()` | `test` → `tests/e2e/test_saved_render_parity.py::SavedRenderParityTests::test_saved_songbook_panel_matches_the_server_grouping` | same keys, same order |
| SC-001 | the running panel | `manual` — open `/songs/` and read the column | preview screenshot in `preview/panel-open-1600x1000.png` |
| SC-002 | `_songbooks_panel.html` | `test` → FR-004's assertion | markup inspection |
| SC-003 | `components.css` | `test` → FR-003's E2E measurement | computed style, not declaration |
| SC-004 | `views.py` sort | `test` → FR-002's fixture with mixed-case names | `Buku Ende HKBP` sorts under `b` |
| SC-005 | `offline-render.js` + `tests/e2e/test_saved_render_parity.py` | `test` → FR-007's parity test | saved vs server |
| SC-006 | `tests/e2e/test_reading.py`, `multimedia/web/tests.py` | `inspection` — the existing Kidung assertions re-run unchanged | row height `38px`, gap `1px` |
| US1/AC1–AC4 | panel markup + `components.css` | `test` → FR-001, FR-003, FR-004 rows | one rule, no heading, both modes |
| US2/AC1–AC4 | `views.py` sorts + `components.css` | `test` → FR-002, FR-005 rows | includes the empty-group case |
| US3/AC1–AC2 | three views + `offline-render.js` | `test` → FR-006, FR-007 rows | parity |

**Verification split**: 12 test · 2 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/128-songbook-hymn-separator/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
multimedia/web/reading/views.py                     _songbook_name_key, _songbook_groups, 3 views
multimedia/web/templates/reading/_songbooks_panel.html   group loop
static/web/offline-render.js                        songbookGroups, songbooksPanel, 2 call sites
static/styles/design/components.css                 .group.is-hidden + .group
multimedia/web/tests.py                             ReadingViewTests
tests/e2e/test_reading.py                           ReadingE2ETests
tests/e2e/test_saved_render_parity.py               SavedRenderParityTests
```

### Structure Decision

The server-side grouping lives beside the existing `_songbooks()` helper in `reading/views.py`, because all
three Kidung views already share that module and pass the panel from it. The saved-render grouping lives beside
`bookLink()` in `offline-render.js`, where the panel's other builders (`biblePanel`, `servicePanel`) already
are. The separator needs no new file: it is the panel's own CSS rule plus one empty-group guard. Tests follow
the repo split — domain behaviour in the app's `tests.py`, user-visible acceptance and saved-render parity in
`tests/e2e/`.
