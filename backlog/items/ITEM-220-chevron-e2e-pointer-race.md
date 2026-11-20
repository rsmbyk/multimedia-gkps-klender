---
id: ITEM-220
status: backlog
title: 'The chevron-eligibility E2E races the pointer on this machine'
type: fix
priority: P2
effort: S
created: 2026-11-20
updated: 2026-11-20
spec:
branch:
pr:
issue:
closed_at:
closed_reason:
bump:
release_version:
---

# ITEM-220: The chevron-eligibility E2E races the pointer on this machine

## Summary

`tests/e2e/test_obs_dock.py::test_the_chevron_marks_the_state_and_the_eligible_rows` waits for
the live row's background to equal the pure `--sidebar-selected-bg` token after
`_project_first_entry`. The screen-row click lands while the entry's block is still morphing
open, so the row can settle a few pixels below the fixed pointer — leaving the pointer over the
live header. The live-hover rule (`obs-dock.css:641`, specs 198/206) then paints the
selected-and-ink mix, which never equals the pure token, and the wait times out at 30 s. The
product behaviour is correct (FR-011's live clause); the test's wait is pointer-position fragile.

## Notes

- Measured 2026-11-20 during spec 208: **unmodified base fails 4 of 5 alone runs** (the slice's
  JS stashed); the slice fails 3 of 5 — statistically the same. A diagnostic timeline caught the
  failing state directly: `hovered: true`, hover chain ending `entryrow`, background
  `color(srgb 0.34149 0.36 0.409569)` vs token `rgb(57, 63, 79)`, stable for 5 s.
- CI ran this test green through spec 206 (PR #550) — the race is machine-local (this machine's
  headless Chromium timing), not a develop regression.
- Fix direction (a test fix, not a product change): move the pointer off the live row before the
  settle wait, or assert the live-hover tone when the row is hovered. TDD-07: the test was wrong
  (it asserts a state that depends on accidental pointer position), the behaviour did not change.
- Also observed once under full-suite load: `test_the_toggle_swaps_instantly_under_reduced_motion`
  ("the block never reported open" — its captured-node watch misses a rebuilt inner); 6/6 green
  alone on the slice, green on the base module run. Same family of load-sensitive waits.

## Acceptance sketch

- The chevron-eligibility test passes reliably on this machine (≥10 consecutive runs) with no
  product behaviour change; the live-hover tone stays as specs 198/206 settled it.

## Links

- Spec: — (found during `specs/208-dock-stuck-corner` verification; recorded so the next session
  does not re-attribute it)
- Related items: ITEM-215, ITEM-217 (the board's other known-red records)
