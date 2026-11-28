# Implementation Plan: pin the live header at the top as soon as it is clipped

**Spec**: `specs/248-dock-top-pin-early/spec.md`
**Branch**: `feat/248-dock-top-pin-early`
**Bump**: `patch` (declared here; applied in the pre-merge delivery commit)
**Preview**: `specs/248-dock-top-pin-early/preview/` — live at `http://127.0.0.1:8793/obs/dock`

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12; vanilla ES5-style JavaScript in `static/web/` |
| Primary dependencies | Django 4.0, DRF, PostgreSQL, WhiteNoise; Playwright (Python) for E2E |
| Storage | No tables, migrations or persisted client state; the covered row and slot live in the DOM |
| Testing | Targeted Django/Playwright E2E in `tests/e2e/test_dock_top_pin.py`; full browser suite at the push step |
| Target platform | `/obs/dock` runner, 420 × 860 review viewport at 1×, dark mode |
| Project type | Server-rendered Django app with a client-side dock list |
| Performance goals | One paint-only reconciliation per existing `updatePins()` call; no polling, no new listener |
| Constraints | Bottom pin, NEXT band, go-to strip, header wash and entry anatomy unchanged (FR-004) |
| Scale / scope | One boundary expression, one paint-only class, one clone-class guard, one E2E module |

## Constitution Check

`CONSTITUTION.md` is absent and is never auto-created (SDD-01); there is no principle to check.

| Principle | Status | Note |
| --- | --- | --- |
| n/a — no constitution in this repo | pass | SDD-01: optional, not created on this slice |

Re-checked after Phase 1: pass — no constitution and no violation introduced. The production diff
is confined to `updateTopBand()` plus two CSS declarations; no new dependency or endpoint appears.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.** Key findings: the sticky header holds at 0 px from
scrollTop 1056 while the clone waited until 1164; `top: -4px` on the clone produced a measured 4 px
hop, so 0 px is kept; hiding the source with `visibility` (not `display`) prevents a second header
without moving the list; `updatePins()` already owns every reconciliation path.

## Phase 1 — Design

- `data-model.md` — the client-only top pin state; no new entity or persisted field.
- `contracts/README.md` — `none` (no HTTP, message, schema or public JS interface is exposed).
- `quickstart.md` — preview server, boundary probe, targeted E2E runner and deferral statement.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-dock.js` — `updateTopBand()` boundary on `li.top` | `test` → `tests/e2e/test_dock_top_pin.py::test_the_top_pin_takes_over_when_the_header_is_clipped` | takeover 108 px earlier; 0 px hop |
| FR-001 (one header) | same + `.entryrow.is-covered` in `obs-dock.css` | `test` → `…::test_only_one_header_is_painted_while_the_pin_owns_the_edge` | source hidden, clone shown; no geometry change |
| FR-002 | same — `updatePins()` call sites, clone re-use, reduced-motion path | `test` → `…::test_the_top_pin_tracks_the_block_per_frame` | 0 mismatched frames on the new boundary |
| FR-002 (reduced motion) | same | `test` → `…::test_the_top_pin_lands_instantly_under_reduced_motion` | same paint, no stale frame |
| FR-003 | `obs-dock.js` — top-band click path (unchanged) | `test` → `…::test_clicking_the_top_pin_performs_the_centre_act` | display state byte-identical, following returns |
| FR-004 | whole diff | `inspection` — `liveband-slot`, `nextband`, `.offstrip` and `.entryrow[aria-current]` rules untouched; the named regression modules stay green | bottom pin and NEXT band keep their states |
| SC-001 | `preview/probe_boundary.py` | `inspection` — before 1164 / -110 px, after 1056 / -2 px; pin 0/38 px, radius 0/9 px, exact label | numbers frozen at gate 1 |
| SC-002 | `preview/probe_boundary.py` + sampler | `test` → `…::test_the_top_pin_tracks_the_block_per_frame` | 490 stepped frames + per-frame glide sample |
| SC-003 | targeted E2E modules | `test` → `tests.e2e.test_dock_top_pin`, `test_dock_stuck_corner`, `test_dock_open_reset` | run with the throwaway `gkps248` database |
| US1/AC1 | same as FR-001 | `test` → `…::test_the_top_pin_takes_over_when_the_header_is_clipped` | shared row |
| US1/AC2 | same as the one-header row | `test` → `…::test_only_one_header_is_painted_while_the_pin_owns_the_edge` | shared row |
| US1/AC3 | go-to `.offstrip` | `manual` — start a Go To, scroll to the fold, read that the `.offstrip` is unchanged; the service pin is present on both builds (D006) | no automated Go To fixture in the new cases |
| US2/AC1 | whole-block-above state | `inspection` — probe frames past `blockBottom <= 0.5` still show the pin at 0 px with one header-height | spec 242 geometry preserved |
| US2/AC2 | bottom pin and NEXT band | `inspection` — `updateLiveBand()`/`updateBand()` byte-identical in the diff | separate slots, separate states |

**Verification split**: 9 test · 4 inspection · 1 manual

## Plan Exit Gate

- Requirement coverage: FR-001…FR-004 and SC-001…SC-003 each have a row — pass.
- Entity coverage: the three client-only fields in `data-model.md` map to FR-001/FR-002 — pass.
- Interface coverage: `contracts/README.md` declares `none` with a reason — pass.
- Decision provenance: D001–D006 each carry owner, research or manual-check provenance — pass.
- Constitution conformance: no constitution; no new dependency or endpoint — pass.
- Zero unknowns: Phase 0's Open section is empty — pass.
- Verification declared: every row has `test`, `inspection` or `manual`; `quickstart.md` commands run — pass.

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/248-dock-top-pin-early/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/README.md  checklists/requirements.md
  preview/{README.md,serve.sh,probe_boundary.py,before-boundary.json,after-boundary.json}
  run-tests.sh
```

### Source

```
static/web/obs-dock.js                 updateTopBand() boundary + covered-row bookkeeping
static/styles/design/obs-dock.css      .is-covered paint rule and its comment
tests/e2e/test_dock_top_pin.py         new boundary and one-header cases
docs/spec/dock.md                      R19 modified block at Converge/Fold
backlog/board.md + backlog/items/ITEM-265  card opened and closed in the delivery commit
VERSION + CHANGELOG.md                 patch bumped in the delivery commit
```

### Structure Decision

No new source directories: the change is one boundary expression and one paint-only class in the
dock's existing files, with new cases beside spec 242's E2E module. The pack's `contracts/` is an
explicit `none`; the preview was built on the real dev server before gate 1, and the targeted test
helper lives beside the pack so its database derivation is reproducible without a credential in
shell history.
