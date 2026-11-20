# Converge: the live entry header's corners follow its pin state

**Spec**: `specs/208-dock-stuck-corner/spec.md` · **Date**: 2026-11-20 · **Status**: Converged

## Passes

1. **Top corner fix** — six E2E pins RED on base, then GREEN after `updateStuck()`; the before/after
   probe measured 328/328 → 0/328 mismatched pinned frames; full dock regression green apart from
   the recorded ITEM-220 pointer race.
2. **Bottom pin and band** — US4 E2E pins RED then GREEN through the live-ruling iterations:
   faithful clone, no-doubling, per-frame tracking, click act, reduced motion, always-visible Next
   band, band-top clip. 12/12 module, 67/67 full regression.

## Gaps

- **ITEM-220** — the chevron-eligibility E2E races the pointer on this machine. Reproduced on the
  unmodified base (4/5 failures alone); recorded as a separate backlog card, not attributed to this
  slice. Accepted, guarded.

## Gate

Converged: no CRITICAL findings, every requirement covered, the one HIGH finding (SC-007's reliance
on suites outside the edited file) guarded by the full 67-test regression and the ITEM-220
attribution. Fold follows.
