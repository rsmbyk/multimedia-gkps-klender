# Implementation Plan: song list keeps its chosen order

**Spec**: `specs/233-song-sort-retained/spec.md`
**Branch**: `fix/233-song-sort-retained`
**Bump**: `patch`
**Preview**: `specs/233-song-sort-retained/preview/` — live at `http://127.0.0.1:8773/songs/book/1/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 + Django 4.0 server; vanilla ES5-style browser JavaScript |
| Primary dependencies | none added — the existing `static/web/reading.js` shell |
| Storage | no schema change; `Song.modified`, `Song.title` and source order are read only |
| Testing | Django test runner; Playwright E2E through `StaticLiveServerTestCase`, throwaway local database |
| Target platform | the reading pages in a desktop browser (review viewport 1440×900) |
| Project type | server-rendered Django templates with an in-place JS shell |
| Performance goals | the re-sort adds one in-memory sort of the visible song rows per refresh |
| Constraints | no document reload; no reordering of non-song lists; hymn books keep number order |
| Scale / scope | one call site, one comparator unchanged, one E2E module |

## Constitution Check

No `CONSTITUTION.md` at the repository root — the constitution is optional and never auto-created
(SDD-01), so there are no principles to check. The table is empty by absence, not by waiver.

Re-checked after Phase 1: n/a — no constitution exists.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no persisted entity added; documents the existing fields the comparator reads.
- `contracts/` — `none` — no new interface; the `#songSort` control and the reconciliation path already exist.
- `quickstart.md` — how to start the preview and run the E2E probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| US1/AC1 | `static/web/reading.js` → `update()`; `tests/e2e/test_song_sort_retained.py` | `test` → `test_create_keeps_alphabetical_order` | rows `Alpha, Beta, Zebra`, button `title` |
| US1/AC2 | `static/web/reading.js` → `applySongOrder()` | `test` → `test_create_in_default_order_leads` | button stays `m`, new song leads |
| US1/AC3 | `static/web/reading.js` → `update()` | `test` → `test_create_keeps_alphabetical_order` | `timeOrigin` unchanged, marker alive |
| US2/AC1 | `static/web/reading.js` → `update()` | `test` → `test_edit_refresh_keeps_alphabetical_order` | |
| US2/AC2 | `static/web/reading.js` → `update()` | `test` → `test_delete_refresh_keeps_alphabetical_order` | |
| US2/AC3 | `static/web/reading.js` → `update()` | `test` → `test_row_click_refresh_keeps_alphabetical_order` | |
| US2/AC4 | `static/web/reading.js` → `applySongOrder()` | `inspection` — hymn book renders no `#songSort` and its `.songrow` order stays by number | spec 011 / 125 |
| US3/AC1 | `static/web/reading.js` → `applySongOrder()` | `inspection` — `songRowEls()` filters on `.songrow`, so chapter and service rows are untouched | |
| US3/AC2 | `static/web/offline-render.js` / server order | `test` → existing `tests/e2e/test_reading.py::test_song_sort_toggles_between_last_modified_and_alphabetical` | default `m` on a fresh load |
| FR-001 | `static/web/reading.js` → `update()` | `test` → `test_create_keeps_alphabetical_order` | the re-sort call after reconciliation |
| FR-002 | `static/web/reading.js` → `syncSortBtn()` | `test` → `test_create_keeps_alphabetical_order` | button and row order agree |
| FR-003 | `static/web/reading.js` → `songSort` initial value | `test` → `test_create_in_default_order_leads` | |
| FR-004 | `static/web/reading.js` → `songRowEls()` | `inspection` — no song rows in `chList` means the sorter is a no-op | |
| SC-001 | `tests/e2e/test_song_sort_retained.py` | `test` → `test_create_keeps_alphabetical_order` | base fails with `['Beta','Zebra','Alpha']` |
| SC-002 | `tests/e2e/test_song_sort_retained.py` | `test` → the three US2 refresh tests | |
| SC-003 | `tests/e2e/test_song_sort_retained.py` | `test` → `test_default_order_and_other_sections_unchanged` | |

**Verification split**: 13 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

No violations.

## Project Structure

### Documentation

```
specs/233-song-sort-retained/
  spec.md plan.md research.md data-model.md quickstart.md tasks.md
  contracts/README.md checklists/requirements.md analysis.md
  preview/README.md
```

### Source

```
static/web/reading.js                       # one call after reconcileChildren
tests/e2e/test_song_sort_retained.py        # new E2E module; the probe is promoted into it
docs/spec/reading.md                        # R57 added at Fold
backlog/board.md, backlog/items/ITEM-247-*  # card opened and closed in this PR
VERSION, CHANGELOG.md                       # patch line at delivery
```

### Structure Decision

The client change is one line in the shell's existing update path; no new module, template or
endpoint is introduced. The E2E module is new because the existing sort test in `test_reading.py`
covers only a button toggle, not a refresh; keeping the refresh cases together makes the red/green
evidence readable in one place.
