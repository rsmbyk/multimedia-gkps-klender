# Implementation Plan: A saved hymn song page never shows the song sort control

**Spec**: `specs/125-saved-song-sort-parity/spec.md`
**Branch**: `fix/125-saved-song-sort-parity`
**Bump**: `patch`
**Preview**: `specs/125-saved-song-sort-parity/preview/` — the running server page for the same route is
the reference; the note records the measured frames

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | vanilla browser JavaScript (ES5 style, no build step) in `static/web/offline-render.js`; Python 3.12 / Django 4.0 unchanged |
| Primary dependencies | none added — one argument at one call site |
| Storage | none — no model, migration, saved payload or IndexedDB schema change |
| Testing | Playwright (Python) E2E via `StaticLiveServerTestCase` in `tests/e2e/test_saved_render_parity.py` |
| Target platform | browsers served by the reading shell (`/songs/<id>/`), desktop viewport |
| Project type | server-rendered Django templates with vanilla JS; the saved renderer builds the same page in the browser from the synced library |
| Performance goals | none — the value is computed from data the renderer already holds; no extra request |
| Constraints | two renderers emit the second sidebar (`multimedia/web/templates/reading/base.html` server-side, `static/web/offline-render.js` in the browser); the control's visibility must agree between them for every song route |
| Scale / scope | one argument in one function, two browser tests, no markup, CSS or template change |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | n/a | no `CONSTITUTION.md` exists in this repo (checked 2026-10-24) — nothing to check against |

Re-checked after Phase 1: n/a — still no constitution file.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity, field, relationship, migration or payload changes`
- `contracts/` — `none — the change is inside a browser renderer; it exposes no request, response, event or function contract`
- `quickstart.md` — how to serve the branch and what to verify by hand

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/offline-render.js` (`songPage()` → `common()`'s `songListOpen`) | `test` → `tests/e2e/test_saved_render_parity.py::SavedRenderParityTests::test_saved_song_pages_match_the_server_sort_control` | saved hymn song: `#songSort.hidden` true, as the server page |
| FR-002 | same | `test` → `SavedRenderParityTests::test_hymn_song_sidebar_open_never_paints_the_sort_control` | no sampled frame with the control visible, online or offline |
| FR-003 | same | `test` → the parity test's ordinary-songbook leg | control visible on both saved and server documents |
| FR-004 | `tests/e2e/test_saved_render_parity.py` | `test` → both new tests, plus the class's existing three | the hidden state joins the fields the class compares |
| FR-005 | untouched files (`reading/base.html`, `offline-render.js` `listPage()`, `chTitle`, rows) | `test` → `tests.e2e.test_saved_render_parity`, `tests.e2e.test_offline_library`, the navigation classes of `tests.e2e.test_reading`, re-run unchanged | nothing else moves |
| SC-001 | `static/web/offline-render.js` | `test` → the frame-sampling test | zero frames visible; one filter width |
| SC-002 | `static/web/offline-render.js` | `test` → the parity test | equal `hidden` state for every song route it covers |
| SC-003 | untouched files | `test` → the parity test's ordinary leg and the existing classes | unchanged |
| US1/AC1 | `static/web/offline-render.js` | `test` → the frame-sampling test's online leg | hidden from the first frame through the settled page |
| US1/AC2 | `static/web/offline-render.js` | `test` → the frame-sampling test's offline leg | hidden while the saved frame is final |
| US1/AC3 | `static/web/offline-render.js` | `test` → the parity test's ordinary leg | visible before and after, as today |
| US2/AC1 | `static/web/offline-render.js` | `test` → the parity test over hymn and ordinary song and book routes | the same rule the server applies |
| US2/AC2 | `static/web/offline-render.js` `listPage()` | `inspection` — the book routes already decide from `selected.is_hymn_book`; the parity test's book routes are the guard | no edit expected |
| US2/AC3 | `tests/e2e/test_saved_render_parity.py` | `test` → the class's field comparison over every route in its list | the regression cannot return unnoticed |

**Verification split**: 13 test · 1 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/125-saved-song-sort-parity/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/offline-render.js                     # songPage(): the control follows the book's hymn flag
tests/e2e/test_saved_render_parity.py            # the red-first parity pin and the frame sampler
backlog/items/ITEM-126-saved-song-sort-parity.md
backlog/board.md                                 # the card's row
specs/README.md                                  # the spec index row
VERSION  CHANGELOG.md                            # patch bump
```

### Structure Decision

Everything stays inside the saved renderer and the E2E module that already owns saved/server parity. No
new module, template, CSS, asset, or fixture format: the tests use the module's existing library-sync
helper and the songbook fixtures it already creates.
