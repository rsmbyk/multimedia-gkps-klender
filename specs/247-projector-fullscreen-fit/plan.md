# Implementation Plan: refit the projector words when fullscreen changes the stage

**Spec**: `specs/247-projector-fullscreen-fit/spec.md`
**Branch**: `fix/247-projector-fullscreen-fit`
**Bump**: `patch` (declared here; applied in the pre-merge delivery commit)
**Preview**: `specs/247-projector-fullscreen-fit/preview/` — live at `http://127.0.0.1:8771/projector?service=144`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; vanilla ES5-style JavaScript in `static/web/` |
| Primary dependencies | Django 4.0, DRF, PostgreSQL, WhiteNoise; Playwright (Python) for E2E |
| Storage | No tables, migrations or persisted client state; the fit cache stays in `dataset.fitted` |
| Testing | Targeted Django/Playwright E2E in `tests/e2e/test_projector.py`; full browser suite at the push step |
| Target platform | The standalone `/projector` page, 1440×900 review viewport at 1× |
| Project type | Server-rendered Django app with a client-side fitted display surface |
| Performance goals | One re-fit per transition on the next frame; no polling, no extra requests |
| Constraints | No endpoint/schema/permission/CSS/template change (FR-006); the fit walk and `setSize` are untouched |
| Scale / scope | Two browser-event listeners, one active-screen choice, six E2E cases, one pack |

## Constitution Check

`CONSTITUTION.md` is absent and is never auto-created (SDD-01); there is no principle to check.

| Principle | Status | Note |
| --- | --- | --- |
| n/a — no constitution in this repo | pass | SDD-01: optional, not created on this slice |

Re-checked after Phase 1: pass — no constitution and no violation introduced. The production change
is confined to the projector's existing event-registration block; no new dependency is added.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Key findings: `resize` is currently the only geometry
signal that re-fits; the page's own fullscreen gesture fires `fullscreenchange`, while F11 needs a
`(display-mode: fullscreen)` change listener; the screen on the stage is the detour while one is up,
so the handler must not always fit `screens()[current]`; fitting on the next animation frame reads
the settled stage without polling.

## Phase 1 — Design

- `data-model.md` — the active screen and its fit key; no persisted or new client state.
- `contracts/README.md` — `none` (browser events are consumed inside one file).
- `quickstart.md` — `preview/run_local.py`, dev server on 8771, targeted verification, and the
  headless-fullscreen limitation stated.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/projector.js` — `syncFullscreenFit()` on `fullscreenchange` | `test` → `tests/e2e/test_projector.py::test_fullscreen_signal_refits_the_words_without_a_resize` | stage grows without `resize` |
| FR-002 | same — `change` on `(display-mode: fullscreen)` | `test` → `…::test_display_mode_signal_refits_for_browser_fullscreen` | F11 has no `fullscreenElement` |
| FR-003 | same — `fit(node, true)` and the existing `dataset.fitted` key | `test` → `…::test_a_second_fullscreen_signal_does_not_change_the_fit` | no double fit on repeat signals |
| FR-004 | same — `fitNeighbours()` after the active fit | `test` → `…::test_fullscreen_signal_refits_the_neighbours` | neighbour sizes read from the DOM |
| FR-005 | whole diff | `inspection` — no edits to `fit()`, `setSize()`, CSS, key/click handlers or the cue | the resize path keeps answering through `render(true)` |
| FR-006 | whole diff | `inspection` — only `static/web/projector.js`, `tests/` and the pack change | no model, view, URL, CSS or template in `git diff --name-only` |
| SC-001 | `preview/probe.py` | `inspection` — base `87 → 87 → 87`, slice `87 → 93 → 87` at stage 804 → 1004 → 804 | numbers frozen at gate 1 |
| SC-002 | `preview/probe.py` | `inspection` — heading `53.769 → 57.4772 → 53.769`, base flat | `size ÷ golden ratio` unchanged |
| SC-003 | `tests/e2e/test_projector.py` + CDP viewport override | `test` → `…::test_resize_driven_fullscreen_still_settles_at_87_and_109` | 1440×900 → 1920×1080 → back |
| SC-004 | new E2E cases and `preview/probe.py` | `inspection` — URL, `data-current-screen=0` and body text unchanged in every reading | no navigation or content change |
| US1/AC1 | same as FR-001 | `test` → `…::test_fullscreen_signal_refits_the_words_without_a_resize` | shared row |
| US1/AC2 | same as FR-003 | `test` → `…::test_a_second_fullscreen_signal_does_not_change_the_fit` | shared row |
| US1/AC3 | detour branch in `syncFullscreenFit()` | `manual` — open a passage Go To, press `f`, read the detour's `.screen__lines` font size, press `f` again | no automated Go To fetch in the new cases |
| US1/AC4 | unchanged-stage guard through the same fit key | `test` → `…::test_a_fullscreen_signal_with_an_unchanged_stage_does_not_resize_words` | no visible change |
| US2/AC1 | same as SC-003 | `test` → `…::test_resize_driven_fullscreen_still_settles_at_87_and_109` | shared row |
| US2/AC2 | same as FR-002 | `test` → `…::test_display_mode_signal_refits_for_browser_fullscreen` | shared row |
| US2/AC3 | F key, mouse zones, cue and shortcut handlers | `inspection` — those blocks are byte-identical to the base | full suite at the push step |

**Verification split**: 10 test · 6 inspection · 1 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/247-projector-fullscreen-fit/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md  preview/{probe.py,run_local.py}
```

### Source

```
static/web/projector.js                      fullscreen and display-mode fit triggers
tests/e2e/test_projector.py                  six new cases beside the existing fit cases
docs/spec/projector.md                       R14 modified block at Converge/Fold
backlog/board.md + backlog/items/ITEM-264    card opened at delivery
VERSION + CHANGELOG.md                       patch bumped in the delivery commit
```

### Structure Decision

No new source directories: the change is two event listeners in the projector's existing event
block, and the tests sit with the projector's own E2E module. The pack's `contracts/` is an
explicit `none`, and its preview was built before gate 1. The dev-server helper lives beside the
probe so the targeted test command is reproducible without a credential in the shell history.
