# Convergence: A Go To still names itself with no service under it

**Spec**: `specs/227-goto-cue-empty-service/spec.md`
**Passes**: 1 of 3

## Pass 1 — 2026-11-23

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| none | — | FR-001 … FR-005, SC-001 … SC-003, US1/AC1 … AC6 | Each row checked by its declared method below. |

**Outcome**: zero findings, so no `## Phase N: Convergence` tasks were appended.

### Read-back by declared method

- **test** — the two new cases were red on the untouched code with
  `AssertionError: 'Matius 5' not found in ''` and `AssertionError: 'NKB 43' not found in ''`
  (the detour painted, the cue prefix did not); green after the guard reorder, `OK` in 5.754s.
- **test** — the related lane `tests.e2e.test_goto_shared_state` + `tests.e2e.test_dock_goto`:
  25 tests, `OK` in 89.035s. The pre-existing no-service picker case and the dock/overlay
  agreement cases stayed green, so the populated-service cue path did not move.
- **inspection** — `git diff` on source touches only `static/web/projector.js` `renderCue()`:
  the `!cue` guard, the cleared labels, the detour dispatch and the empty check below it.
  `display.js`, `renderDetourCue()`, templates and endpoints are byte-identical to the base.
- **inspection** — the Back path stays in `applyGoto()`: `goto: null` → `paintIdle()` →
  `syncEmptyNotice()`, which the existing picker case exercises.
- **test** — the live probe at `http://127.0.0.1:8765/projector` reads prefix
  `HAL 1 Jahowa Sihol Pujionku ·`, seven baits, and `back to service` with no service open.

## Pass 2

Not needed — Pass 1 converged.

## Accepted gaps

None.

## Cap reached

Not reached.
