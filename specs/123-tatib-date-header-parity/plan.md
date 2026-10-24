# Implementation Plan: Match the Tata Ibadah date header to the songbook header

**Spec**: `specs/123-tatib-date-header-parity/spec.md`
**Branch**: `fix/123-tatib-date-header-parity`
**Bump**: `patch`
**Preview**: `specs/123-tatib-date-header-parity/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | CSS in a Django template app; Python 3.12 / Django 4.0 unchanged |
| Primary dependencies | none added — one rule in `static/styles/design/components.css` |
| Storage | none — no model, migration, or serialized payload |
| Testing | Django test runner (text pins) + Playwright (Python) E2E via `StaticLiveServerTestCase` |
| Target platform | browsers served by the reading shell (`/tatib/<id>/`), desktop and mobile viewports |
| Project type | server-rendered Django templates with vanilla JS; CSS design tokens under `static/styles/design/` |
| Performance goals | none — the paint cost of one rule is unchanged |
| Constraints | `.read__eyebrow` is shared by Bible, Kidung, and media-library pages: the change must stay scoped to `[data-kind="tatib"]`; `margin-bottom: 0` inside a service head and the 34px Project button row must survive (spec 018, spec 102) |
| Scale / scope | one selector, one wrap rule, one E2E module |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| n/a | n/a | no `CONSTITUTION.md` exists in this repo (checked 2026-10-24) — nothing to check against |

Re-checked after Phase 1: n/a — still no constitution file.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entity, field, relationship, migration or payload changes`
- `contracts/` — `none — the slice exposes no interface; it is a stylesheet rule, so there is no request/response, event or function contract to write`
- `quickstart.md` — how to serve the branch and what to verify by hand

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/styles/design/components.css` (`.read[data-kind="tatib"] .read__head-top .read__eyebrow`) | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_tatib_date_header_matches_songbook_header` | compares the date against `/songs/<id>/`'s songbook eyebrow and against the frozen tuple |
| FR-002 | same rule (`margin-bottom: 0`) + `.read__head-top` flex row | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_tatib_date_and_project_button_are_vertically_centered` | existing pin, re-run unchanged |
| FR-003 | `.read[data-kind="tatib"] .read__head-top { flex-wrap: wrap; row-gap: 8px }` | `test` → `tests/e2e/test_reading.py::ReadingE2ETests::test_tatib_date_header_reflows_at_a_narrow_stage` | asserts the date box equals its full text width and the document never scrolls sideways at 1440 / 1280 / 390 |
| FR-004 | `static/web/offline-render.js` (`servicePage()`) writes the same classes | `inspection` — the saved renderer emits `class="read__eyebrow"` inside `[data-kind="tatib"]`, so the rule reaches it; the offline E2E already pins its text | no code change expected; confirmed by reading the renderer |
| FR-005 | `.read__eyebrow` base rule (untouched) | `test` → `test_tatib_date_header_matches_songbook_header` also asserts the song eyebrow's frozen values | keeps the reference from drifting with the target |
| FR-006 | `multimedia/web/templates/reading/base.html`, `multimedia/web/reading/views.py`, `.read__head-top` rules | `test` → `multimedia/web/tests.py::ReadingViewTests::test_tatib_service_header_uses_full_indonesian_month_name`, `::test_undated_tatib_header_keeps_its_label`, and the centring test's `marginBottom == 0px` assertion | no template, view, or control change |
| SC-001 | `static/styles/design/components.css` | `test` → the header test | computed-style equality |
| SC-002 | `static/styles/design/components.css` | `test` → the centring test | row height and centre delta |
| SC-003 | `static/styles/design/components.css` | `test` → the reflow test | no horizontal overflow; date unclipped |
| SC-004 | `.read__eyebrow` base rule | `test` → the header test (frozen song tuple) | Bible/Kidung untouched |
| US1/AC1–AC3 | `static/styles/design/components.css` | `test` → the header test | dated, undated, and reference cases |
| US2/AC1 | `.read[data-kind="tatib"] .read__head-top` | `test` → the reflow test | the wrap itself is observed in the preview at 1280 |
| US3/AC1 | `static/web/offline-render.js` | `inspection` — the saved path carries the same classes; its text is already pinned offline | not exercised live in the preview |

**Verification split**: 11 test · 2 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| none | — | — |

## Project Structure

### Documentation

```
specs/123-tatib-date-header-parity/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
static/styles/design/components.css        # the tatib eyebrow rule and the head-row wrap
tests/e2e/test_reading.py                  # two pins: header parity, narrow-stage reflow
backlog/items/ITEM-124-tatib-date-header-parity.md
backlog/board.md                           # the card's row
VERSION  CHANGELOG.md                      # patch bump
```

### Structure Decision

All work stays inside the existing reading shell: the stylesheet it already loads, the E2E module that
already owns the Tata Ibadah header pins (`tests/e2e/test_reading.py`), and the board's existing card
format. No new module, template, or asset.
