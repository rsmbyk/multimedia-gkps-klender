# Implementation Plan — spec 246

**Slice**: `specs/246-media-library-bible-rail`
**Status**: Plan complete — gate 2 pending
**Spec**: Accepted at gate 1 on 2026-11-27
**Capability**: new `reading/R63`
**Bump**: `patch` (declared at Plan, applied at Fold per VER-04)

## Technical Context

- **Language/runtime**: Python 3.12, Django 4.0, DRF; PostgreSQL on the compose stack, SQLite in
  the slice preview.
- **Front end**: server-rendered templates, vanilla JS shell in `static/web/reading.js`;
  no new dependency, package or build step.
- **Change surface**: one context key in `multimedia/web/reading/views.py::media_library`.
  The rail handler, templates, CSS, endpoints and schema are untouched.
- **Preview**: live server from the slice worktree (`http://127.0.0.1:8769/`), approved at gate 1.
- **Testing**: Playwright E2E in a Django `StaticLiveServerTestCase`, against a throwaway
  database; no new seam beyond the page the operator opens by clicking through the rail.
- **Cards/versioning**: `ITEM-263`; `VERSION` 1.37.3 → 1.37.4 at Fold; changelog line under
  `## [Unreleased]`; board closes in the delivery commit.

## Constitution Check

No `CONSTITUTION.md` exists at the repo root, so the check is skipped silently (SDD-01).
No standing principle is claimed or violated.

## Complexity Tracking

No violation to justify. The change is one server-rendered context value; no new abstraction,
dependency or migration is introduced.

## Phase 0 — Research

See `research.md`. All decisions are grounded in the accepted preview and the code already in the
repo; zero open unknowns. No owner question was needed.

## Phase 1 — Design

- `data-model.md` — no model, migration or schema change.
- `contracts/none.md` — no external interface change.
- `quickstart.md` — how to reproduce, run the targeted lane and drive the live preview.

The approved preview components are the design surface: the Media Library view context feeds the
same document root the rail handler reads, so the design adds no new UI component.

## Traceability

Verified by: **9 test · 5 inspection · 4 manual**.

| ID | Component | Verified by | Evidence |
| --- | --- | --- | --- |
| FR-001 | Media Library view context → document root `data-section` | test | tests/e2e/test_media_library_bible_rail.py::test_media_library_declares_its_own_section |
| FR-002 | rail handler section comparison in static/web/reading.js (unchanged) | test | tests/e2e/test_media_library_bible_rail.py::test_first_bible_rail_click_from_media_library_opens_books |
| FR-003 | `#panelBody .book` rows and `#panelEmpty.hidden` | test | tests/e2e/test_media_library_bible_rail.py::test_first_bible_rail_click_from_media_library_opens_books |
| FR-004 | railBtnClick own-tile toggle branch (unchanged) | manual | preview/README.md step 4 — click the section tile already on stage |
| FR-005 | media_library.html `aria-current` and R62 pending state (unchanged) | inspection | diff against origin/develop: no template, CSS or JS file changes |
| FR-006 | change surface | inspection | git diff origin/develop..HEAD — only the view context line and the new spec/test files |
| SC-001 | one `GET /bible/` on the first Alkitab click | test | request count assertion in the new E2E module |
| SC-002 | sidebar row count after that click | test | `#panelBody .book` count assertion in the new E2E module |
| SC-003 | empty-list visibility after that click | test | `#panelEmpty[hidden]` assertion in the new E2E module |
| SC-004 | other rail navigation lanes | inspection | existing navigation E2E modules left untouched; targeted run recorded in Converge |
| US1 AC1 | document root section on Media Library | test | test_media_library_declares_its_own_section |
| US1 AC2 | first Alkitab click from Media Library | test | test_first_bible_rail_click_from_media_library_opens_books |
| US1 AC3 | another section first, then Alkitab | inspection | preview/probe.py afterOtherSection on both surfaces |
| US2 AC1 | own-tile toggle | manual | preview/README.md step 4 |
| US2 AC2 | cross-section switch | manual | preview/README.md step 3 |
| US2 AC3 | direct `/media-library/` load | inspection | media_library.html rail tile marker plus probe direct comparison |
| Edge 1 | in-place rail arrival adopts the same section | test | E2E setup clicks the rail tile, not a deep link |
| Edge 2 | narrow viewport | manual | preview/README.md — drawer state unchanged; no new CSS |

The seven Plan exit checks are recorded in `analysis.md` alongside the gate-2 review.

## Delivery bound at Fold

- Fold writes `reading/R63` into `docs/spec/reading.md` as an added block and bumps `last folded`.
- The delivery commit carries the code, spec pack, `VERSION`, changelog line and the board close.
- Push happens only on the owner's word (GIT-07); no push or PR update is implied by gate 2.
