# Implementation Plan: Back clears the Go To from the cue over an empty stage

**Spec**: `specs/228-goto-cue-back-reset/spec.md`
**Branch**: `fix/228-goto-cue-back-reset`
**Bump**: `patch` — 1.36.13 → 1.36.14
**Preview**: `specs/228-goto-cue-back-reset/preview/`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12, Django 4.0, vanilla JS |
| Primary dependencies | Django, Django REST Framework, Playwright (Python) for E2E |
| Storage | PostgreSQL; no data changes in this slice |
| Testing | Django test runner; Playwright E2E via `StaticLiveServerTestCase` |
| Target platform | Browser projector page, all viewports |
| Project type | Server-rendered templates with a browser-local display state |
| Performance goals | None; no new work at runtime |
| Constraints | One branch of one JS function, one `revealCursor()` guard and two CSS switches; no template, endpoint or model change |
| Scale / scope | Empty-stage cue reset and idle HUD only; detour and populated-service paths untouched |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| none | pass | No `CONSTITUTION.md` exists at the base commit; there is no project principle to check. |

Re-checked after Phase 1: pass — the change clears existing DOM nodes only.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entities; the change clears existing DOM.`
- `contracts/` — `none` — no HTTP, model, script or event interface changes.
- `quickstart.md` — the targeted E2E lane and the live probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js:915` `renderCue()` empty branch | `test` → `...::test_back_clears_a_passage_cue_when_no_service_is_open` and `...::test_back_clears_a_song_cue_when_the_service_has_no_entries` | prefix, flip, baits, progress cleared |
| FR-002 | same | `test` → `_assert_cue_clear` in both cases | `#cue-next` hidden and computed `display: none`; no arrow box |
| FR-003 | same | `test` → `...::test_a_dock_back_clears_the_projector_cue_with_no_service` + `paintIdle()` inspection | three exit paths reach `renderCue()` |
| FR-004 | `static/web/projector.js:909–914` | `test` → the 227 cases in the same module | detour still paints label and controls |
| FR-005 | `static/web/projector.js`, `static/styles/design/projector.css` | `inspection` — `git diff` touches `projector.js`, `projector.css`, the tests and the records | no state, message or template change |
| FR-006 | `static/styles/design/projector.css:458` | `test` → `...::test_an_idle_empty_cue_has_no_separator_and_no_next` | computed `display: none`, `innerText === ''` |
| FR-007 | `static/styles/design/projector.css:457` | `test` → `...::test_an_idle_empty_projector_ignores_mouse_zones_but_keeps_fullscreen` | zones `pointerEvents: none`; fullscreen still entered |
| FR-008 | `static/web/projector.js:465,1123` | `test` → `...::test_an_idle_empty_projector_keeps_the_cursor_and_its_buttons` | no `cursor-hidden`, body cursor `auto` |
| FR-009 | `static/styles/design/projector.css:457–458` | `test` → same cursor/buttons case | keys, find and service list still open |
| SC-004 | E2E separator/zones case | `test` | both empty situations |
| SC-005 | E2E cursor/buttons case | `test` | fullscreen, keys, find, service list |
| SC-001 | no-service Back case | `test` | prefix, flip, Back |
| SC-002 | empty-service Back case | `test` | bait count |
| SC-003 | `tests.e2e.test_goto_shared_state`, `tests.e2e.test_dock_goto` | `test` | 31 tests, all green |
| US1/AC1 | no-service passage Back | `test` | same as SC-001 |
| US1/AC2 | empty-service song Back | `test` | same as SC-002 |
| US1/AC3 | dock Back | `test` | shared-state path |
| US1/AC4 | never-opened cue | `inspection` — the clear is the same branch used at first render | separator-only cue |
| US1/AC5 | populated service | `test` → pre-existing cases | unchanged path |
| US2/AC1 | idle cue | `test` → separator case | no visible text |
| US2/AC2 | idle zones | `test` → zones/fullscreen case | inert, fullscreen kept |
| US2/AC3 | idle cursor | `test` → cursor/buttons case | visible after 2.4s |
| US2/AC4 | idle buttons | `test` → cursor/buttons case | fullscreen + cue controls |
| US2/AC5 | detour over empty stage | `test` → the 227 cases in the goto lane | cue unchanged while up |

**Verification split**: 16 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/228-goto-cue-back-reset/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/projector.js                 empty branch of renderCue(), empty-stage sync, cursor guard
static/styles/design/projector.css      idle separator and mouse-zone switches
tests/e2e/test_goto_shared_state.py     six E2E cases for the stale cue, the reset and the idle HUD
docs/spec/projector.md                  R2 folded with the clear-on-exit and idle HUD rules
```

### Structure Decision

The tests extend the module that owns the shared Go To state and already carries the no-service and
empty-service fixtures from spec 227; a third case covers the dock's own Back. The code change stays
in the one function that owns the cue.
