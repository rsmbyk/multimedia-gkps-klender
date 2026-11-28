# Implementation Plan: refit the Go To detour on a stage resize

**Spec**: `specs/249-goto-fullscreen-fit/spec.md`
**Branch**: `fix/249-goto-fullscreen-fit`
**Bump**: `patch` (declared here; applied in the pre-merge delivery commit)
**Preview**: `specs/249-goto-fullscreen-fit/preview/` — live at `http://127.0.0.1:8772/projector?service=144`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; vanilla ES5-style JavaScript in `static/web/` |
| Primary dependencies | Django 4.0, DRF, PostgreSQL, WhiteNoise; Playwright (Python) for E2E |
| Storage | No tables, migrations or persisted client state; fit keys remain in `dataset.fitted` |
| Testing | Three named cases in `tests/e2e/test_projector.py`; full browser suite at the push step |
| Target platform | The standalone `/projector` page, 1440×900 review viewport at 1× |
| Project type | Server-rendered Django app with a client-side fitted display surface |
| Performance goals | One detour fit per resize on the next frame; no polling, no extra requests |
| Constraints | No endpoint/schema/permission/CSS/template change; `render()` and `fitNeighbours()` unchanged |
| Scale / scope | One call in the resize listener, three E2E cases, one pack |

## Constitution Check

`CONSTITUTION.md` is absent and is never auto-created (SDD-01); there is no principle to check.

| Principle | Status | Note |
| --- | --- | --- |
| n/a — no constitution in this repo | pass | SDD-01: optional, not created on this slice |

Re-checked after Phase 1: pass — no constitution and no violation. The single production edit sits
in the projector's existing resize listener; no dependency is added.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** `render()` fits only service screens and
`fitNeighbours()` skips the detour, so the detour needs the stage-screen fit on resize; spec 247's
`syncFullscreenFit()` already owns that choice and runs on the next frame.

## Phase 1 — Design

- `data-model.md` — the detour and its fit key; no persisted state.
- `contracts/README.md` — `none`.
- `quickstart.md` — `preview/run_local.py`, dev server on 8772, targeted verification, and the
  headless fullscreen limitation.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js` — `resize` calls `syncFullscreenFit()` | `test` → `tests/e2e/test_projector.py::test_a_goto_detour_refits_on_a_resize` | detour font follows the stage |
| FR-002 | same | `test` → `…::test_a_fullscreen_signal_before_resize_still_fits_the_detour` | signal-first ordering |
| FR-003 | same + existing `dataset.fitted` key | `test` → `…::test_a_goto_detour_refits_on_a_resize` | shared row; key returns to the original |
| FR-004 | whole diff | `test` → `…::test_a_resize_without_a_detour_keeps_service_screens` + `inspection` — `render()` and `fitNeighbours()` byte-identical | guard |
| FR-005 | whole diff | `inspection` — only `static/web/projector.js`, `tests/` and the pack change | no model, view, URL, CSS or template |
| SC-001 | `preview/probe.py` | `inspection` — base `87 → 87 → 87`, slice `87 → 109 → 87` | resize-only ordering |
| SC-002 | `preview/probe.py` | `inspection` — same numbers with `fullscreenchange` first | signal-first ordering |
| SC-003 | new E2E cases + probe | `inspection` — detour stays active, URL and service screens unchanged | no visible state change |
| US1/AC1 | same as FR-001 | `test` → `…::test_a_goto_detour_refits_on_a_resize` | shared row |
| US1/AC2 | same as FR-003 | `test` → `…::test_a_goto_detour_refits_on_a_resize` | shared row |
| US1/AC3 | same as FR-002 | `test` → `…::test_a_fullscreen_signal_before_resize_still_fits_the_detour` | shared row |
| US1/AC4 | same as FR-004 | `test` → `…::test_a_resize_without_a_detour_keeps_service_screens` | shared row |

**Verification split**: 8 test · 4 inspection · 0 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/249-goto-fullscreen-fit/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md  preview/{probe.py,run_local.py}
```

### Source

```
static/web/projector.js                      resize fits the stage screen too
tests/e2e/test_projector.py                  three new cases beside the Go To/fit cases
docs/spec/projector.md                       R14 regression note at Converge/Fold
backlog/board.md + backlog/items/ITEM-266    card opened at delivery
VERSION + CHANGELOG.md                       patch bumped in the delivery commit
```

### Structure Decision

No new source directories: one call in the projector's existing resize listener and three cases in
its own E2E module. The pack's `contracts/` is an explicit `none`; the preview helper lives beside
the probe so the targeted command never puts a credential in shell history.
