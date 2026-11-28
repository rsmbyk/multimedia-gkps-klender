# Fold: refit the Go To detour on a stage resize

**Capability**: `docs/spec/projector.md`
**Folded at**: 2026-11-27

## Delta

| Type | Requirement | Change |
| --- | --- | --- |
| `modified` | `R14` | Complete replacement block: R14 now requires the resize path to fit the screen actually on the stage, so a Go To detour follows a stage change whether the resize comes alone or after a `fullscreenchange`. A regression scenario "a Go To detour on a resize" is added; the spec-247 paragraph and its scenario, the fit walk, cap, cut and faces rules are unchanged. (spec 249) |

## Operations

- Header prepended `249-goto-fullscreen-fit` to `slices`, keeping the 20 incoming entries in place.
- One `modified` block on R14; no `added`, `removed` or `renamed` operation, and no new `R<n>`.
  This is a regression note on spec 247's fix: the detour is a screen on the stage, so R14's
  "size does not depend on how it was reached" already covers it.

## Evidence

- `converge.md` pass 1: all 12 traceability rows met by their declared method; zero gaps.
- Three named E2E cases: red `FF.` with the merged 247 file under a trap, green `...` with the fix;
  `preview/probe.py` froze `87 → 109 → 87px` against a flat base in both signal orderings.
- Before / after counts: `### R` blocks 16 → 16; `#### Scenario` entries 67 → 68; `slices`
  entries 20 → 21; R14 scenarios 6 → 7.
- Capability diff (`git diff --numstat`): 11 insertions, 1 deletion — only the header and R14.

## Drift guard

- **Files changed in this capability**: `docs/spec/projector.md` only.
- **Declared no behaviour change**: no — a resize that changes the stage while a Go To detour is
  up now re-fits the detour; the capability file carries the new requirement and scenario.
