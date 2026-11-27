# Implementation Plan: pending state for Search and Media Library rail tiles

**Spec**: `specs/245-rail-fetch-feedback/spec.md`
**Branch**: `fix/245-rail-fetch-feedback`
**Bump**: `patch`
**Preview**: `specs/245-rail-fetch-feedback/preview/combined.html`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; vanilla ES5-style JavaScript in `static/web/` |
| Primary dependencies | Django 4.0, DRF, PostgreSQL, jQuery/RxJS/Fomantic where already loaded; Playwright (Python) for E2E |
| Storage | No new tables; client-only state in `activeFetches` and DOM attributes |
| Testing | Targeted Django/Playwright E2E in `tests/e2e/test_navigation_pending.py`; full browser suite at the push step |
| Target platform | Desktop-first reading shell, 1440×900 review viewport, narrow ≤720px |
| Project type | Server-rendered Django app with in-place stage swaps via `navigate()` |
| Performance goals | Lock, bar and placeholder paint with the request; no separate delay; no extra requests |
| Constraints | No endpoint/schema/permission change (FR-010); `navigate()` stays the single choke point; WhiteNoise manifest needs `collectstatic` after static edits |
| Scale / scope | Two rail tiles, three placeholder shapes, one CSS override, one E2E module |

## Constitution Check

`CONSTITUTION.md` is absent and is never auto-created (SDD-01); there is no principle to check.

| Principle | Status | Note |
| --- | --- | --- |
| n/a — no constitution in this repo | pass | SDD-01: optional, not created on this slice |

Re-checked after Phase 1: pass — no constitution and no violation introduced.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Key findings: a new `media-library` kind must be
added to `STAGE_KINDS`, `swapsStage` and the history `pushes` list; `shell:page` already
re-initialises the library after the swap; the shell's home-state CSS gates hide Search shapes
inside the stage and need a scoped override; Search's destination and snapshot are untouched.

## Phase 1 — Design

- `data-model.md` — three client-only entities: RailTile, PendingFetch, Placeholder; no persistence.
- `contracts/README.md` — `none` (no new interface; existing fetch header and `shell:page` reused).
- `quickstart.md` — local DB through `preview/run_local.py`, dev server on 8787, targeted verification.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/reading.js` — `#railMediaLibrary` click → `navigate(..., kind:'media-library')`; kind registered | `test` → `tests/e2e/test_navigation_pending.py::test_media_library_rail_fetches_in_place` | Search keeps `openSearch()` |
| FR-002 | `static/web/reading.js` — `lockItem()` on rail source | `test` → `…::test_search_rail_locks_the_tile` | opacity + `aria-disabled` |
| FR-003 | `static/web/reading.js` — `sectionsFor()` / `barFor('stage')` | `test` → `…::test_search_rail_shows_the_stage_bar` | 3px at stage y=0 |
| FR-004 | `static/web/reading.js` — `placeholderFor()` three shapes; `static/styles/design/components.css` — scoped visibility override | `test` → `…::test_search_results_placeholder_matches_real_groups` | result-group anatomy |
| FR-004 | same | `test` → `…::test_search_home_placeholder_matches_the_landing` | logo + input/submit |
| FR-004 | same | `test` → `…::test_media_library_placeholder_matches_real_rows` | chips, groups, file rows |
| FR-005 | `static/web/reading.js` — `sectionsFor()` and lock target | `inspection` — no rail/sidebar container disable in the diff | R61 parity |
| FR-006 | `static/web/reading.js` — `finish()` / `fail()` / `clearStageFor()` | `test` → `…::test_settlement_clears_the_busy_state` | both destinations |
| FR-006 | same | `inspection` — `noLocationFallback` branch keeps state until unload | fallback path |
| FR-007 | `static/web/reading.js` — `activeFetches` cancel rule | `test` → `…::test_search_then_media_library_cancels_the_first` | existing case extended |
| FR-008 | `static/web/reading.js` — `openSearch()`, `lastSearchSnapshot()`, rail hrefs | `inspection` — destinations unchanged from base | no snapshot edits |
| FR-009 | `static/web/reading.js` — `announce()`; `components.css` reduced-motion rule | `inspection` — one status message per start/settle, sweep stops | no focus move |
| FR-010 | whole diff | `inspection` — no `multimedia/web/*`, URL, model or migration file | client/CSS/tests only |
| FR-011 | `static/web/media-library.js` — loading text before `refresh()` | `test` → `…::test_media_library_direct_load_shows_a_loading_state` | direct loads only |
| FR-012 | `static/styles/design/components.css` — hide direct-child search sections while busy | `test` → `…::test_destination_placeholder_hides_the_previous_search_home` | descendant copy stays visible |
| SC-001 | `preview/probe.py` + `preview/combined.html` | `inspection` — three probed states with computed values | 0 ms/1.2 s/2.5 s |
| SC-002 | `static/web/reading.js` — placeholder padding | `test` → `…::test_destination_placeholder_origin_matches_the_reading_page` | stage +64/+40 at 1440px |
| SC-003 | `static/web/reading.js` — settlement cleanup | `test` → `…::test_media_library_settlement_clears_state` | no residue |
| SC-004 | `static/web/reading.js` — supersede | `test` → `…::test_search_then_media_library_cancels_the_first` | shared with FR-007 |
| US1/AC1 | rail tile lock | `test` → `…::test_search_rail_locks_the_tile` | shared with FR-002 |
| US1/AC2 | stage bar | `test` → `…::test_search_rail_shows_the_stage_bar` | shared with FR-003 |
| US1/AC3 | placeholder anatomy | `test` → `…::test_media_library_placeholder_matches_real_rows` | shared with FR-004 |
| US1/AC4 | rail and sidebar interactivity | `inspection` — only tile and stage locked | no container disable |
| US2/AC1 | settlement | `test` → `…::test_media_library_settlement_clears_state` | shared with SC-003 |
| US2/AC2 | full-page fallback | `inspection` — `fail()` branch | R61 behaviour reused |
| US2/AC3 | supersede | `test` → `…::test_search_then_media_library_cancels_the_first` | shared with FR-007 |
| US3/AC1 | Search destination | `inspection` — `openSearch()` unchanged | saved last results |
| US3/AC2 | reduced motion | `inspection` — CSS `@media` rule | lock and text survive |
| US3/AC3 | status announcement | `inspection` — `announce()` call sites | one per transition |

**Verification split**: 18 test · 11 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/245-rail-fetch-feedback/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md  preview/
```

### Source

```
static/web/reading.js                          new kind, rail click, three placeholder shapes
static/styles/design/components.css            scoped placeholder visibility + reduced-motion
tests/e2e/test_navigation_pending.py           new cases for both rail tiles
docs/spec/reading.md                           R62 folded at Converge
```

### Structure Decision

No new source directories: the behaviour lives in the shell's existing navigation module and the
app's existing stylesheet and E2E module. The only new pack folders are the spec's `contracts/`
(explicit `none`) and its preview, which was built before gate 1. Backend templates are read as
the source of placeholder anatomy but are not changed.
