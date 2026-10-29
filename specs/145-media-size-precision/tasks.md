# Tasks: a media size reads in the unit that still shows its number

**Spec**: `specs/145-media-size-precision/spec.md`
**Plan**: `specs/145-media-size-precision/plan.md`
**Verification split**: 3 test · 1 inspection · 1 manual

## Phase 1 — Setup

- [X] T001 `backlog/items/ITEM-157-media-size-precision.md` + its `Speccing` board row
- [X] T002 `specs/145-media-size-precision/` pack and `preview/README.md`

## Phase 2 — Foundational

- [X] T003 `static/web/media-size.js` — `window.gkpsFormatSize`, decimal units, one decimal trimmed, unit
      promoted at `1000`
- [X] T004 `multimedia/web/templates/reading/base.html` — load `media-size.js` before `media-entry.js`

## Phase 3 — US1 (P1) 🎯 MVP

**Goal**: no size reads as zero and the unit follows the file.
**Independent test**: a 12,345-byte file reads `Image · 12.3 KB` in the card; a 512-byte file reads
`Image · 512 B`.

- [X] T005 [P] [US1] failing test `test_media_size_reads_in_the_smallest_unit_that_shows_a_number` in
      `tests/e2e/test_media_library.py`, asserting the card's line for 12,345 and 512 bytes
- [X] T006 [US1] `static/web/media-entry.js` — `formatSize` delegates to `window.gkpsFormatSize`
- [X] T007 [US1] `static/web/media-library.js` — `fmtSize` delegates, for the row and the Total

## Phase 4 — US2 (P2)

**Goal**: one label on every surface.
**Independent test**: the card and the library row print the same string for the same file.

- [X] T008 [US2] same test, extended: the library row and the Total read the same string as the card
- [X] T009 [US2] `static/web/media-handoff.js` — remove the unused `fmt`

## Phase N — Polish

- [X] T010 `CHANGELOG.md` line under `## [Unreleased]`, `VERSION` → `1.22.5`
- [X] T011 board row to `Done`, card closed with the merge reference
- [X] T012 `docs/spec/reading.md` folded with `R21`

## Phase N+1 — Convergence

<!-- written by Converge only; absent until it runs -->
