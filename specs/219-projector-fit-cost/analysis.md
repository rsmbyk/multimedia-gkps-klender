# Analyze: a text screen arrives as fast as the entries beside it

**Date**: 2026-11-22
**Read**: `spec.md` @ `91ff3d13b506`, `plan.md` @ `5ab4f35b6378`, `research.md`, `tasks.md`,
`checklists/requirements.md` (15 items, 0 ticked — reviewer-owned)
**Metrics**: 6 FR · 6 SC · 13 tasks · 15 checklist items · 0 CRITICAL · coverage 100%

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F001 | — | Every FR-001…FR-006 carries a component and a `Verified by` row in `plan.md`; every SC-001…SC-006 carries a command or a test. | none needed |
| F002 | — | Terminology is stable: "fitting" for the search, "cut" for the single-screen truncation, "arrival morph" for `screenIn`. The words "fit at rest" and "fitted ahead of time" each name one thing. | none needed |
| F003 | LOW | `SC-003` (the rapid advance) reports a median that improves while its worst case does not (70.4 → 67 ms). The spec says so in the table; a reader skimming the criterion alone could read it as an improvement across the board. | reported, not fixed — the spec's §Assumptions already says the rapid run is the floor, and the table carries both numbers |
| F004 | LOW | `SC-006` and FR-005 are verified `manual` while a test could pin the cut's output (the existing single-screen test asserts the whole body fits but not the row and character count of a body too long for any size). | reported; the existing test already fails if the cut changes shape enough to matter, and a synthetic 400-row body in the suite would cost seconds |
| F005 | — | `checklists/requirements.md` is generated and unticked, as gate 2 expects. | none needed |
| F006 | — | No requirement in the spec contradicts the capability tree: `projector/R14` is new, and nothing in R1–R13 speaks to when a screen is fitted. | none needed |

## Mechanical fixes applied

- None. The spec and plan were written against the measured behaviour in one pass; the numbers in
  `## UI/UX` and the success criteria come from the same two probe runs.

## Intent items left to the owner

- **Gate 1**: whether the visible delta is acceptable — a screen of words may now be one to eight
  pixels larger, because it is fitted where it rests instead of 14 px below it. Every size equals the
  one the display already gave after a resize; the owner decides whether that reads as a correction.
- **Gate 2**: whether `SC-003`'s unchanged worst case is acceptable as stated (F003), or whether the
  rapid path deserves its own slice.

## History

- 2026-11-22 — first run: 0 CRITICAL, 0 HIGH, 2 LOW (F003, F004), coverage 100%.
