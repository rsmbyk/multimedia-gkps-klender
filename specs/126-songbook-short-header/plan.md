# Implementation Plan: A song page cites its songbook by its short name

**Spec**: `specs/126-songbook-short-header/spec.md`
**Branch**: `feat/126-songbook-short-header`
**Bump**: `patch`
**Preview**: `specs/126-songbook-short-header/preview/` — the running song page with the change, plus the
measured header boxes and the saved/server comparison

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 / Django 4.0 server-side; vanilla browser JavaScript (ES5 style, no build step) in the saved renderer |
| Primary dependencies | none added — one expression in one view, one in one function |
| Storage | none — no model, migration, saved-payload or IndexedDB schema change |
| Testing | Django test runner (`multimedia/web/tests.py`), Playwright (Python) E2E in `tests/e2e/test_saved_render_parity.py` |
| Target platform | the reading shell's song route `/songs/<id>/`, desktop and narrow viewports |
| Project type | server-rendered Django templates with vanilla JS; the saved renderer builds the same page in the browser from the synced library |
| Performance goals | none — the value is computed from data the view already has; the saved renderer already holds the same fields |
| Constraints | two renderers produce the header (the view, and `offline-render.js`), and spec 122 fixed saved/server parity as the contract for these routes; `.read__eyebrow`'s type must not change (spec 123 compares the Tata Ibadah date against it) |
| Scale / scope | two files, ~10 lines; four new unit pins, two E2E pins (one new case, one new comparison) |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | n/a | no `CONSTITUTION.md` exists in this repo (checked 2026-10-24) — nothing to check against |

Re-checked after Phase 1: n/a — still no constitution file.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the two entities read, unchanged; the header as a pure function of them.
- `contracts/` — `none`; the slice exposes no interface.
- `quickstart.md` — how to serve the branch and what to verify by hand.
- `docs/spec/reading.md` — **created by this slice's Fold**: the repo's first capability file, holding
  `R1` (a song page's header cites its songbook by its short name) and `R2` (a saved reading page shows the
  same header and title as its server route). The requirements from earlier slices are not folded — there was
  no tree when they landed — and the file says so in its header. Both of this slice's capability labels point
  at this one file; the `saved-reading` label used by specs 125 and 126's FRs is `reading/R2`.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `multimedia/web/reading/views.py` (`SongDetailView`) + `static/web/offline-render.js` (`songPage()`) | `test` → `multimedia/web/tests.py::ReadingViewTests::test_song_detail_header_cites_the_short_songbook_reference` | `NKB 12`, not `Nyanyikanlah Kidung Baru 12` |
| FR-002 | same | `test` → `ReadingViewTests::test_song_detail_header_falls_back_to_the_full_songbook_name` | a hymn book whose `short_name` is `''` |
| FR-003 | same | `test` → `ReadingViewTests::test_an_ordinary_songbook_header_keeps_its_full_name` | `Kidung Harian`, blank short name |
| FR-004 | `static/web/offline-render.js` | `test` → `tests/e2e/test_saved_render_parity.py::SavedRenderParityTests::test_saved_documents_use_route_specific_labels_and_markup` (new hymn-eyebrow case) + `::test_header_and_title_agree_between_saved_and_server` | saved text equals server text |
| FR-005 | `multimedia/web/reading/views.py` (`page_title`) + `common()`'s `doc.title` | `test` → `ReadingViewTests::test_song_detail_tab_title_uses_the_short_reference` + the parity test's title leg | `NKB 12 — GKPS Klender` |
| FR-006 | same as FR-001 | `test` → `ReadingViewTests::test_an_ordinary_songbook_with_a_short_name_still_shows_its_full_name` | an ordinary book with `short_name='KH'` keeps `Kidung Harian` |
| FR-007 | untouched files (`reading/base.html`, `_song_rows`, `_songbooks_panel.html`) | `test` → `multimedia.web.tests` + `tests.e2e.test_saved_render_parity` + `tests.e2e.test_offline_library`, re-run unchanged | nothing else moves |
| SC-001 | `views.py` | `test` → `test_song_detail_header_cites_the_short_songbook_reference` | header text is exactly the reference |
| SC-002 | `views.py` | `test` → the fallback, sub-number and unnumbered tests | no header begins with a bare number, none has a trailing space |
| SC-003 | `views.py` | `test` → `test_an_ordinary_songbook_header_keeps_its_full_name` | unchanged from before the slice |
| SC-004 | `offline-render.js` | `test` → `test_header_and_title_agree_between_saved_and_server` | hymn + ordinary routes |
| SC-005 | untouched files | `test` → the re-run suites in FR-007 | label, heading, row and placeholder assertions already in place |
| US1/AC1 | `views.py` | `test` → `test_song_detail_header_cites_the_short_songbook_reference` | `PKJ 4` shape, `NKB 12` in the fixture |
| US1/AC2 | `views.py` | `test` → `ReadingViewTests::test_a_sub_number_follows_the_short_reference` | `NKB 12B` |
| US1/AC3 | `views.py` | `test` → `test_song_detail_header_falls_back_to_the_full_songbook_name` | the full name before the number |
| US1/AC4 | `views.py` | `test` → `ReadingViewTests::test_an_unnumbered_hymn_song_shows_the_reference_alone` | `NKB`, no number, no trailing space |
| US2/AC1 | `views.py` | `test` → `test_an_ordinary_songbook_header_keeps_its_full_name` | |
| US2/AC2 | `reading/base.html`, `views.py::_song_rows`, `_songbooks_panel.html` | `inspection` — on `/songs/1013/`: the second sidebar's heading still reads `Song list — Pelengkap Kidung Jemaat`, its rows still read `PKJ 1`…`PKJ 4`, the panel still lists the songbooks in full, the filter still reads `Filter songs…`, and the stage title is unchanged | no edit to any of them; the re-run suites are the guard |
| US3/AC1 | `offline-render.js` | `test` → `test_header_and_title_agree_between_saved_and_server` | |
| US3/AC2 | `offline-render.js` | `test` → the existing `eyebrow` case on the ordinary route (`Ordinary Test`) in `test_saved_documents_use_route_specific_labels_and_markup` | stays green |

**Verification split**: 19 test · 1 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/126-songbook-short-header/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md  converge.md  fold.md
  contracts/  checklists/  preview/
docs/spec/reading.md                             # created by this slice's Fold (R1, R2)
```

### Source

```
multimedia/web/reading/views.py                  # SongDetailView: the citation and the tab title
static/web/offline-render.js                     # songPage(): the same rule in the saved renderer
multimedia/web/tests.py                          # four new ReadingViewTests pins
tests/e2e/test_saved_render_parity.py            # a hymn eyebrow case and the saved/server comparison
backlog/items/ITEM-127-songbook-short-header.md
backlog/board.md                                 # the card's row
specs/README.md                                  # the spec index row
docs/spec/reading.md                             # the capability tree's first file (Fold)
VERSION  CHANGELOG.md                            # patch bump
```

### Structure Decision

Both code edits land in the files that already own the header — the view and the saved renderer. No new
module, template, CSS file, asset or fixture format: the tests extend the two modules that already create
songbook and song fixtures. The one new directory is `docs/spec/`, created by this slice's Fold as the
capability tree the process reads before every later slice.
