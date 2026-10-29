# Implementation Plan: the empty notice leaves the stage

**Spec**: `specs/161-projector-empty-notice/spec.md`
**Branch**: `fix/161-projector-empty-notice`
**Bump**: `patch`
**Preview**: `specs/161-projector-empty-notice/preview/preview.html` (static, four boards; live route in its README)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | JavaScript (ES5, browser IIFE) in `static/web/projector.js`; Django template markup; Python 3.12 for the suite |
| Primary dependencies | none new — the page's own scripts, Django 4.0, Playwright (Python) as the E2E driver |
| Storage | none added: the page keeps no state beyond the DOM; the service's screens still arrive in its own response |
| Testing | Django's `StaticLiveServerTestCase` with Playwright, `tests/e2e/test_projector.py`; the static preview's probe for the UI/UX numbers |
| Target platform | the projector page (`/projector`) in Chromium, mirrored to the congregation's display; 1920×1080 and 1440×900 |
| Project type | server-rendered Django app, vanilla JS, no build step |
| Performance goals | one O(1) attribute write per render; no request, no layout read added to the render path |
| Constraints | the notice is server-rendered only when the response has no screens; no route, payload or template copy changes; `renderDetour()`'s fitting and the cue are untouched |
| Scale / scope | one paragraph, one helper, two call sites; one E2E module gains four cases |

## Constitution Check

No `CONSTITUTION.md` at the repository root — the constitution is optional and this project has not
adopted one, so there is no principle to check against. **Status: n/a.**

Re-checked after Phase 1: n/a — no constitution exists to re-check.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — the DOM state the notice is decided from (two facts, five transitions).
- `contracts/` — `none`: the slice adds no route, payload, header or stored field; the page's server
  response and its scripts keep their contract.
- `quickstart.md` — the dev server, the two test modules, the preview probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js` → `syncEmptyNotice()`; `multimedia/web/templates/reading/projector.html:55-57` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests.test_an_empty_service_shows_its_empty_state` | extended to read the notice's visibility, not only its copy |
| FR-002 | `static/web/projector.js` → `renderDetour()` and `syncEmptyNotice()` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests.test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | asserts no box and that the stage gains exactly the notice's height |
| FR-003 | `static/web/projector.js` → `leaveDetour()` → `render()` → `syncEmptyNotice()` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests.test_closing_the_detour_brings_the_empty_notice_back` | |
| FR-004 | `static/web/projector.js` → `reflow()` → `render()` → `syncEmptyNotice()` | `test` → `tests/e2e/test_projector.py::ProjectorE2ETests.test_a_reread_with_screens_hides_the_empty_notice`; `test` → `tests/e2e/test_projector.py::ProjectorE2ETests.test_a_reread_without_screens_keeps_the_empty_notice` | two outcomes, two cases |
| FR-005 | `static/web/projector.js` → `syncEmptyNotice()` | `inspection` — the notice's `hidden` is written in that function only, and the function is called from `render()` and `renderDetour()`; `grep -n "projector__empty" static/web/projector.js` shows no other write | |
| FR-006 | `tests/e2e/test_projector.py` | `test` — the four cases above run green | |
| FR-007 | the whole diff | `inspection` — the diff names `static/web/projector.js`, `tests/e2e/test_projector.py` and this pack only; no route, template copy, stylesheet or fitting change; the module's existing cases stay green | |
| SC-001 | `static/web/projector.js` | `test` → `test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | computed `display: none`, no box |
| SC-002 | `specs/161-projector-empty-notice/preview/preview.html`, `probe.py` | `manual` — the preview probe's readout, checked against the live page: stage 945.6 → 984, fitted lines 103 → 107px, lines' centre 623.9 → 647.7 at 1920×1080 | |
| SC-003 | `static/web/projector.js` | `test` → `test_closing_the_detour_brings_the_empty_notice_back` | |
| SC-004 | `static/web/projector.js` | `test` → `test_a_reread_with_screens_hides_the_empty_notice`; `test` → `test_a_reread_without_screens_keeps_the_empty_notice` | |
| US1/AC1 | `static/web/projector.js`, `projector.html` | `test` — the "before" step of `test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | notice visible on the empty page |
| US1/AC2 | `static/web/projector.js` | `test` → `test_the_empty_notice_leaves_the_stage_for_a_goto_passage` | |
| US1/AC3 | `static/web/projector.js` | `test` → `test_closing_the_detour_brings_the_empty_notice_back` | |
| US1/AC4 | `static/web/projector.js` | `inspection` — stepping inside the detour re-runs `renderDetour()`, whose sync leaves it hidden; the case `test_a_verse_step_inside_a_chapter_makes_no_request` still steps the detour | |
| US2/AC1 | `static/web/projector.js` | `test` → `test_a_reread_with_screens_hides_the_empty_notice` | |
| US2/AC2 | `static/web/projector.js` | `test` → `test_a_reread_without_screens_keeps_the_empty_notice` | pins the other side: passes before and after |

**Verification split**: 13 test · 3 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| — | — | — |

## Project Structure

### Documentation

```
specs/161-projector-empty-notice/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/projector.js                 one helper + calls from render() and renderDetour()
tests/e2e/test_projector.py             four cases in ProjectorE2ETests
```

### Structure Decision

The change lives in the file that already owns the page's state: `.projector__empty` is the one
server-rendered element outside `#projectorScreens`, and every path that could paint over it ends in
`render()` or `renderDetour()`. A helper beside `screens()` keeps the rule in one place; no new
module, no event, and no observer — the page's own render calls already run at every transition the
spec names. The tests join the module that owns the projector's behaviour, in the class whose
fixtures already hold an empty service (`self.other`).
