## What changed

A fullscreen transition could change the projector's stage without a window `resize` event, so the
fitted words kept their windowed size and the bigger stage sat empty. The projector now re-fits the
screen on the stage on the next frame after `fullscreenchange` (the F key and mouse zones) and after
a change in `(display-mode: fullscreen)` (the browser's own F11). The Go To detour is fitted while
it is up, the neighbours are fitted in idle time, and a signal that leaves the stage unchanged
writes no new size. The fit walk, typography, controls and endpoints are untouched.

## Verification

- Split: 10 test · 6 inspection · 1 manual.
- Six named E2E cases: red `F.F.F.` with the base projector script under a trap, green `......` with
  the fix, on throwaway `test_gkps247`. The three guard cases are green on the base too.
- Live probe: base `87 → 87 → 87px`, slice `87 → 93 → 87px`; heading `53.769 → 57.4772 → 53.769px`.
  The live Go To detour reads `87 → 93 → 87px` with its fit key following the stage.
- Converge pass 1: 17/17 traceability rows met, zero gaps. Analysis: 0 CRITICAL, 4 LOW.

## Records

- Board: ITEM-264 (Done).
- Spec: `specs/247-projector-fullscreen-fit/spec.md`.
- Fold: `docs/spec/projector.md`, `projector/R14` modified with a fullscreen regression scenario.
