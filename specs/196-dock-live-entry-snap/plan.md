# Implementation Plan: dock live entry snap

**Spec**: `specs/196-dock-live-entry-snap/spec.md`
**Branch**: `feat/196-dock-live-entry-snap` off `develop`
**Bump**: `none`
**Preview**: `specs/196-dock-live-entry-snap/preview/index.html`

## Technical Context
- **Language / version**: JavaScript (vanilla), no framework; Python 3.12 / Django 4.0 for E2E
- **Primary dependencies**: `static/web/obs-dock.js`; `static/styles/design/obs-dock.css`; `multimedia/web/templates/reading/obs_dock.html`; `static/styles/design/tokens.css`
- **Storage**: browser-local only; no server state, no DB writes
- **Testing**: Playwright (Python) E2E via Django `LiveServerTestCase`; `tests/e2e/test_obs_dock.py` pattern
- **Target platform**: every browser the app supports; dock panel 320 / 400 / 520 widths
- **Performance goals**: reuse existing `glideScroll`; no new timers or allocations
- **Constraints**: no new DOM elements; snap reuses `glideScroll`'s path; reduced-motion instant via existing flag; `cancelPendingCenter` unchanged
- **Scale / scope**: one runner entry — the live entry — park logic; every state notice with a live service and no morph
- **Project type**: server-rendered Django + static HTML for preview; no bundler, no build step

## Constitution Check
No `CONSTITUTION.md` exists; SDD-01 makes it optional and never auto-created. The repo's rules apply as the constraints above: markup only, no new token, no new dependency, no interface change. Re-checked after Phase 1: pass — design adds zero bytes of new code; only logic re-target in `sync()`.

## Phase 0 — Research
See `research.md`. Unknowns remaining: 0.

## Phase 1 — Design
- `data-model.md` — n/a (no stored data)
- `contracts/` — `none` (`contracts/none.md`)
- `quickstart.md` — run commands and hand checks

## Traceability
| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 | `static/web/obs-dock.js` — `scheduleCenter` / `centerRow` / `glideScroll` | `inspection` | re-target scrollTop when entry entirely off-screen |
| FR-002 | `static/web/obs-dock.js` — `updateBand` + bottom snap path | `inspection` | foot parked `liBottom − clientHeight − protrude`; no next entry → flush at bottom |
| FR-003 | `static/web/obs-dock.js` — `updateBand` no-next path | `inspection` | band hidden; foot flush at bottom edge |
| FR-004 | `static/web/obs-dock.js` — `centerRow` kept for partly visible | `inspection` | overlap of `.entryli` with `[0, clientHeight)` → centred |
| FR-005 | `static/web/obs-dock.js` — snap fires at sync moments only | `inspection` | only `live && !morphing` in `sync()`; not on scroll settle |
| FR-006 | `static/web/obs-dock.js` — `cancelPendingCenter` on wheel / pointerdown | `inspection` | no snap starts while gesture in progress |
| FR-007 | `static/web/obs-dock.js` — reduced motion instant path | `test` | `glideScroll`'s `reduceMotion.matches` jump reused |
| FR-008 | `static/styles/design/obs-dock.css` — band show/hide unchanged | `inspection` | diff shows no CSS change |
| FR-009 | `static/web/obs-dock.js` — go-to keeps today's behaviour | `inspection` | `sync()` returns before the parking code — the `if (dock.goto)` branch ends in `return;` (~1070–1081) |
| SC-001 | as FR-001 | `test` → `tests/e2e/test_obs_dock_snap.py::SnapE2ETests::test_off_top_snaps_flush_at_top` | `scrollTop` settles at `li.offsetTop`, ±1 px |
| SC-002 | as FR-002 / FR-003 | `test` → `tests/e2e/test_obs_dock_snap.py::SnapE2ETests::test_off_bottom_foot_just_above_next_band`, `…::test_last_entry_snaps_flush_at_bottom` | `scrollTop` ≈ `liBottom − clientHeight − 10`; band bottom flush at scroller's bottom edge, not `hidden`; last entry: ≈ `liBottom − clientHeight`, band hidden |
| SC-003 | as FR-004 | `test` → `tests/e2e/test_obs_dock_snap.py::SnapE2ETests::test_partly_visible_keeps_centring` | `scrollTop` settles at today's centre formula, ±2 px |
| SC-004 | as FR-006 | `test` → `tests/e2e/test_obs_dock_snap.py::SnapE2ETests::test_wheel_cancels_pending_snap` | wheel during snap leaves scrollTop where gesture parked it |
| SC-005 | as FR-007 | `test` → `tests/e2e/test_obs_dock_snap.py::SnapE2ETests::test_reduced_motion_snaps_instant` | emulated reduced motion; position jumps, no glide frames |
| SC-006 | as FR-008 / FR-009 | `inspection` — diff + existing dock suites | `tests/e2e/test_obs_dock.py` untouched cases stay green |
| US1/AC1 | `static/web/obs-dock.js` | `test` → `…::test_off_top_snaps_flush_at_top` | |
| US1/AC2 | `static/web/obs-dock.js` | `test` → `…::test_off_top_snaps_flush_at_top` | hand scrolled away, then state notice |
| US1/AC3 | `static/web/obs-dock.js` | `test` → `…::test_reduced_motion_snaps_instant` | |
| US2/AC1 | `static/web/obs-dock.js` | `test` → `…::test_off_bottom_foot_just_above_next_band` | |
| US2/AC2 | `static/web/obs-dock.js` | `test` → `…::test_last_entry_snaps_flush_at_bottom` | |
| US2/AC3 | `static/web/obs-dock.js` | `test` → `…::test_reduced_motion_snaps_instant` | |
| US3/AC1 | `static/web/obs-dock.js` | `test` → `…::test_partly_visible_keeps_centring` | |
| US3/AC2 | `static/web/obs-dock.js` | `test` → `…::test_already_centred_stays_put` | |
| US4/AC1 | `static/web/obs-dock.js` | `test` → `…::test_wheel_cancels_pending_snap` | |
| US4/AC2 | `static/web/obs-dock.js` | `test` → `…::test_no_snap_starts_during_gesture` | |

**Verification split**: 9 test · 9 inspection · 2 manual

## Complexity Tracking
| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure
### Documentation
```
specs/196-dock-live-entry-snap/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md
  contracts/  checklists/  preview/
```

### Source
No source files are added or changed beyond the logic re-target in `sync()` at `static/web/obs-dock.js`.
The snap is pure logic: measure the `.entryli` box against `clientHeight`, and if entirely above top →
`glideScroll(liTop)` (row flush at the scroller's top edge); if entirely below bottom →
`glideScroll(liBottom - runBody.clientHeight - protrude)` where `protrude` is the band's
`bottom: -10px` magnitude (`0` when the band is hidden → foot flush at the bottom edge). All existing
paths (`glideScroll`, `cancelPendingCenter`, `updateBand`) remain untouched; only the target passed
to `glideScroll` changes.

### Structure Decision
No new files or directories are required; the feature lives entirely inside `sync()` of `static/web/obs-dock.js`. The preview HTML mirrors the real DOM; the spec's `## UI/UX` numbers supply the rest.