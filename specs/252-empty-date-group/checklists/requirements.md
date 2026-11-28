# Requirements checklist: No empty groups after the last row is deleted

Reviewer-owned. The agent generates and never ticks these boxes.

| ID | Question | Quality dimension | Traceability |
| --- | --- | --- | --- |
| CHK001 | Does FR-001 name the owning element and the observable condition (no `.book` rows)? | Clarity | [FR-001] |
| CHK002 | Does FR-002 distinguish hiding from removing a filtered group and name the restore path? | Completeness | [FR-002] |
| CHK003 | Is FR-003 limited to the one renderer that emitted an empty group? | Coverage | [FR-003] |
| CHK004 | Does FR-004 enumerate the surfaces checked instead of asserting "everything"? | Completeness | [FR-004] |
| CHK005 | Can US1 and US2 each fail independently, with its own live-preview observation? | Verifiability | [US1, US2] |
| CHK006 | Are the `UI/UX` values counts, heading text and class state rather than adjectives? | Measurability | [UI/UX] |
| CHK007 | Do SC-001 and SC-002 name concrete commands and comparisons? | Measurability | [SC-001, SC-002] |
| CHK008 | Does the assumption list state every default taken without an owner answer? | Completeness | [Assumptions] |
| CHK009 | Does the preview state both routes and the instruments that produced its numbers? | Verifiability | [UI/UX] |
| CHK010 | Does the capability target one durable rule rather than a list of edited files? | Consistency | [FR-001] |

10 of 10 items carry a traceability marker (100%). Focus areas: clarity/completeness, measurability,
verifiability, consistency — four, within the cap.

## Validation (agent, before gate 1)

**Iteration 1** — each item checked against `spec.md`: CHK001 yes (`section.group`, no `.book` rows);
CHK002 yes (hide vs remove, filter cleared); CHK003 yes (template mode only); CHK004 yes (nine named
surfaces); CHK005 yes (separate live observations in `UI/UX`); CHK006 yes (counts/text/class); CHK007
yes (module path and byte-identical base comparison); CHK008 yes (five assumptions, including re-run
chronology and card state); CHK009 yes (8776/8777 and `probe.py`); CHK010 yes (one rule for all grouped
sidebars). No failing item; no second iteration needed.

**[Gap]** — none identified.
