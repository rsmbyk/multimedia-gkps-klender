# Requirements checklist: Enter accepts a delete confirmation

Reviewer-owned. The agent generates and never ticks these boxes.

| ID | Question | Quality dimension | Traceability |
| --- | --- | --- | --- |
| CHK001 | Does FR-001 name the trigger (Enter), the state (open destructive confirmation) and the observable (its control activated)? | Clarity | [FR-001] |
| CHK002 | Do FR-002 and FR-004 separate focus independence from the guards that must still refuse activation? | Completeness | [FR-002, FR-004] |
| CHK003 | Does FR-006 enumerate every live destructive surface found in the survey instead of saying "all modals"? | Coverage | [FR-006] |
| CHK004 | Does FR-005 state both exactly-once activation and suppression of the default key action? | Completeness | [FR-005] |
| CHK005 | Can US1 and US2 each fail on a distinct before/after observation in `## UI/UX`? | Verifiability | [US1, US2] |
| CHK006 | Are the `UI/UX` values request counts, click counts and visibility states rather than adjectives? | Measurability | [UI/UX] |
| CHK007 | Does each SC name the probe or test that produces its number? | Measurability | [SC-001, SC-002, SC-003, SC-004] |
| CHK008 | Does the assumption list name the retired-surface scope, the media inclusion, the focus rule and the preview-first chronology? | Completeness | [Assumptions] |
| CHK009 | Does every non-destructive confirmation named in the survey have a rule that leaves its Enter behaviour untouched? | Coverage | [FR-003, FR-007] |
| CHK010 | Does the capability target one durable keyboard rule rather than a list of edited files? | Consistency | [FR-001] |

10 of 10 items carry a traceability marker (100%). Focus areas: clarity/completeness,
measurability, verifiability, coverage — four, within the cap.

## Validation (agent, before gate 1)

**Iteration 1** — each item checked against `spec.md`: CHK001 yes (trigger/state/observable);
CHK002 yes (focus rule separate from hidden/disabled/repeat/modifier guards); CHK003 yes (five named
surfaces, retired modals excluded with measured reason); CHK004 yes (once and default suppressed);
CHK005 yes (POST counts versus click counter); CHK006 yes (counts, visibility, no geometry claims);
CHK007 yes (`probe.py` and `tests.e2e.test_enter_delete_confirm`); CHK008 yes (six assumptions including
chronology); CHK009 yes (copy/leave/generate/screen-mode named); CHK010 yes (one `reading/R68`).
No failing item; no second iteration needed.

**[Gap]** — none identified.
