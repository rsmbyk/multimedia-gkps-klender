# Implementation Plan: the dock's re-centring keeps pace with fast advancing

**Spec**: `specs/205-dock-centre-pace/spec.md`
**Branch**: `fix/205-dock-centre-pace`
**Bump**: `patch`
**Preview**: `live preview at http://127.0.0.1:8765/obs/dock` (probe: `preview/probe.py`)

## Technical Context

| Field | Value |
| --- | --- |
| Language / version | Python 3.12 (tests); vanilla JS (the change) |
| Primary dependencies | Django 4.0; Playwright (Python) for E2E |
| Storage | unchanged (no model or migration) |
| Testing | Django runner; `StaticLiveServerTestCase` E2E in `tests/e2e/` |
| Target platform | the OBS browser dock (Chromium), desktop |
| Project type | server-rendered Django + vanilla JS |
| Performance goals | the centring glide completes within the advance cadence; no new per-frame work |
| Constraints | one shared pace/curve across the three re-centre paths; hand toggle untouched; reduced motion instant |
| Scale / scope | one JS file (`obs-dock.js`): one constant, one curve, three call sites; one new E2E test |

## Constitution Check

| Principle | Status | Note |
| --- | --- | --- |
| No `CONSTITUTION.md` in this repo (SDD-01) | pass | nothing to check against |

Re-checked after Phase 1: pass.

## Phase 0 — Research

See `research.md`. **Unknowns remaining: 0.**

## Phase 1 — Design

- `data-model.md` — no entities; invariants recorded.
- `contracts/` — none (no external interface).
- `quickstart.md` — commands that run in this worktree.

## Traceability

| Requirement | Component / file | Verified by | Notes |
| --- | --- | --- | --- |
| FR-001 (pace) | `static/web/obs-dock.js` (`CENTRE_MS`, `glideScroll`, `glideRow`, `startMorph`) | `test` → `tests/e2e/test_obs_dock_follow.py::test_the_centring_glide_runs_at_the_shared_pace` (new) | single-move duration ≤ 280 ms; red on develop's 400 ms |
| FR-001 (curve) | `static/web/obs-dock.js` (`ease`) | `test` → `tests/e2e/test_obs_dock_follow.py::test_the_centring_decelerates_into_its_target` (existing) | sine shape: outer steps < 0.35 × peak |
| FR-002 | `static/web/obs-dock.js` (`startToggleMorph`) | `inspection` — 230 ms `easeInOut` unchanged in the diff | hand toggle is a separate motion |
| FR-003 (reduced) | `static/web/obs-dock.js` (`reduceMotion` paths) | `test` → `tests/e2e/test_obs_dock_follow.py::test_reduced_motion_jumps_instead_of_gliding` | instant jump unchanged |
| FR-003 (clamp/cancel) | `static/web/obs-dock.js` (`glideScroll` clamp; wheel/pointerdown cancel) | `inspection` — unchanged in the diff | ends clamp; hand cancels |
| US1/AC4 | `static/web/obs-dock.js` (`startMorph` carry) | `inspection` — `duration = CENTRE_MS`, same `ease` | expand/collapse/scroll one motion |
| SC-001 | `preview/probe.py` single-move | `manual` | landing 0 px, 0 reversals, ~12 moving frames |
| SC-002 | `preview/probe.py` rapid runs | `manual` | mean_off 13.7/9.4/6.6 vs 16.0/14.6/11.9; max_step 100/82/80 vs 148/99/88 |
| SC-003 | `tests/e2e/test_obs_dock_follow.py::test_the_centring_decelerates_into_its_target` | `test` | guard green on the new curve |

**Verification split**: 4 test · 3 inspection · 2 manual

## Complexity Tracking

| Violation | Why needed | Simpler alternative rejected because |
| --- | --- | --- |
| | | |

## Project Structure

### Documentation

```
specs/205-dock-centre-pace/
  spec.md  plan.md  research.md  data-model.md  quickstart.md  tasks.md  analysis.md
  contracts/README.md  checklists/requirements.md  preview/
```

### Source

```
static/web/obs-dock.js                       # CENTRE_MS, ease, three call sites
tests/e2e/test_obs_dock_follow.py            # one new pace test
```

### Structure Decision

The pace lives in one constant beside the glide section so the three re-centre paths cannot drift;
the curve stays the single `ease` helper the morph already shares. The new test joins the existing
centring module (`test_obs_dock_follow.py`) rather than a new file — it reuses that module's fixture
and helpers. No template, migration, settings or CSS change.