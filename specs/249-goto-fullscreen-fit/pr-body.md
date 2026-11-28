## What changed

The spec-247 fix re-fitted the screen on the stage on fullscreen signals, but a Go To detour was
never part of the `resize` path: `render()` fits service screens only and `fitNeighbours()` skips
the detour. F11, or a page fullscreen whose `fullscreenchange` arrives before the viewport grows,
therefore left the detour's words at the windowed size. The resize listener now calls the existing
stage-screen fit after `render()`, so the detour follows the same stage geometry in both orderings.

## Verification

- Split: 8 test · 4 inspection · 0 manual.
- Three named E2E cases: red `FF.` with the merged 247 file under a trap, green `...` with the fix,
  on throwaway `test_gkps249`; the no-detour guard is green on the base too.
- Live probe, both resize-only and signal-first: base `87 → 87 → 87px`, slice `87 → 109 → 87px`,
  stage 804 → 984 → 804.
- Converge pass 1: 12/12 traceability rows met, zero gaps. Analysis: 0 CRITICAL, 1 LOW (the
  fonts-ready detour gap, reported and left out of scope).

## Records

- Board: ITEM-266 (Done).
- Spec: `specs/249-goto-fullscreen-fit/spec.md`.
- Fold: `docs/spec/projector.md`, `projector/R14` modified with a Go To regression scenario.
