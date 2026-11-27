# Fold: refit the projector words when fullscreen changes the stage

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-11-27

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R14` | Complete replacement block: R14 now requires a re-fit of the screen on the stage on the next frame after a fullscreen signal — `fullscreenchange` for the page's gesture and `(display-mode: fullscreen)` for the browser's own control — with the detour fitted while it is up, the neighbours re-fitted in idle time, and no write when the stage is unchanged. A regression guard scenario "a fullscreen transition" is added; the existing four scenarios and the fit walk, cap, cut and faces rules are unchanged. (spec 247) |

## Operations

- Header moved `last folded` from 2026-11-23 to 2026-11-27 and prepended
  `247-projector-fullscreen-fit` to the `slices` line, keeping every incoming slice ID in place.
- One `modified` block on R14; no `added`, `removed` or `renamed` operation, and no new `R<n>`.
  The defect was a missing trigger for behaviour R14 already claims ("the size a screen shows does
  not depend on how it was reached"), so it folds as a modification with a regression note.

## Evidence

- `converge.md` pass 1: all 17 traceability rows met by their declared method; zero gaps.
- Six named E2E cases: red `F.F.F.` with the base file under a trap, green `......` with the slice
  file; `preview/probe.py` froze `87 → 93 → 87px` against a flat base; the live Go To detour read
  `87 → 93 → 87px` with its fit key following the stage.
- Before / after counts: `### R` blocks 16 → 16; `#### Scenario` entries 66 → 67 (one added to
  R14); `slices` entries 19 → 20; R14 scenarios 5 → 6.
- Capability diff (`git diff --numstat`): 13 insertions, 2 deletions — only the header and R14.

## Drift guard

- **Files changed in this capability**: `docs/spec/projector.md` only.
- **Declared no behaviour change**: no — a browser that changes the stage without a `resize` now
  re-fits the words; the capability file carries the new trigger and regression scenario.
