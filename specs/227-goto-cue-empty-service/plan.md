# Implementation Plan: A Go To still names itself with no service under it

**Spec**: `specs/227-goto-cue-empty-service/spec.md`
**Branch**: `fix/227-goto-cue-empty-service`
**Bump**: `patch` — 1.36.12 → 1.36.13
**Preview**: `specs/227-goto-cue-empty-service/preview/`

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
| Constraints | One JS function; no template, endpoint or model change |
| Scale / scope | The `renderCue()` guard order only; all other cue paths unchanged |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| none | pass | No `CONSTITUTION.md` exists at the base commit; there is no project principle to check. |

Re-checked after Phase 1: pass — no new component, dependency or runtime behaviour is introduced.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — `n/a — no entities; the change is the order of two guards.`
- `contracts/` — `none` — no HTTP, model, script or event interface changes.
- `quickstart.md` — the targeted E2E lane and the live probe.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js:909` `renderCue()` | `test` → `tests.e2e.test_goto_shared_state.GotoSharedStateE2ETests::test_cue_carries_a_passage_and_its_controls_with_no_service` | no service, detour paints, prefix names passage |
| FR-002 | `static/web/projector.js:1687` `renderDetourCue()` (unchanged) | `test` → `...::test_cue_carries_a_passage_and_its_controls_with_no_service` and `...::test_cue_carries_a_song_and_its_baits_when_the_service_has_no_entries` | flip, baits and Back |
| FR-003 | `static/web/projector.js:909` | `test` → the two new cases plus 23 pre-existing goto tests | detour checked before the empty return |
| FR-004 | `static/web/projector.js:1532` `applyGoto()` (unchanged) | `inspection` — Back writes `goto: null`, `applyGoto` paints idle and `syncEmptyNotice` restores the notice | covered by `test_a_picker_go_to_stands_alone_and_paints_on_both_surfaces` |
| FR-005 | `static/web/display.js` (unchanged) | `inspection` — `git diff` touches only `projector.js`, the tests, the pack and the records | no new message or state field |
| SC-001 | E2E no-service case | `test` | prefix, flip, Back |
| SC-002 | E2E empty-service case | `test` | prefix, bait count |
| SC-003 | `tests.e2e.test_goto_shared_state`, `tests.e2e.test_dock_goto` | `test` | 25 tests, all green |
| US1/AC1 | no-service passage | `test` | same as SC-001 |
| US1/AC2 | empty-service song | `test` | same as SC-002 |
| US1/AC3 | stepping the detour | `test` → `tests.e2e.test_dock_goto` (existing offrow/back tests) | detour controls keep working |
| US1/AC4 | Back over empty service | `inspection` — existing picker test covers the idle return | notice restored |
| US1/AC5 | populated service | `test` → 23 pre-existing goto tests | unchanged cue path |
| US1/AC6 | dock- and reading-started Go To | `test` → `tests.e2e.test_goto_shared_state` (existing tests) | one shared state |

**Verification split**: 10 test · 3 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/227-goto-cue-empty-service/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source

```
static/web/projector.js                 guard order in renderCue()
tests/e2e/test_goto_shared_state.py     two E2E cases for the empty-cue defect
docs/spec/projector.md                  R2 folded with the new scenario
```

### Structure Decision

The tests extend the module that already owns the shared Go To state and its no-service fixture;
they do not open a new file for a two-case regression. The code change stays in the function that
already draws the cue.
