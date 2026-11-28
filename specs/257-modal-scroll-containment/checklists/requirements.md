# Requirements checklist: An open modal keeps the scroll to itself

Reviewer-owned. The agent generates and never ticks these boxes.

| ID | Question | Quality dimension | Traceability |
| --- | --- | --- | --- |
| CHK001 | Does FR-001 name the state (`dialog[open]`) and the forbidden observable (document scroll)? | Clarity | [FR-001] |
| CHK002 | Do FR-002 and FR-003 separate the reaching-the-end case from the zero-range case? | Completeness | [FR-002, FR-003] |
| CHK003 | Does FR-004 enumerate every scrollport found in the survey instead of saying "all modals"? | Coverage | [FR-004] |
| CHK004 | Does FR-005 state both restored scrolling and the absence of layout shift? | Completeness | [FR-005] |
| CHK005 | Can US1, US2 and US3 each fail on their own observation in the before/after table? | Verifiability | [US1, US2, US3] |
| CHK006 | Are the `UI/UX` values offsets, computed styles and box geometry rather than adjectives? | Measurability | [UI/UX] |
| CHK007 | Do SC-001 to SC-004 name the probe that produces each number? | Measurability | [SC-001, SC-002, SC-003, SC-004] |
| CHK008 | Does the assumption list name the dialog scope, the sibling-pane measurement, the input under test and the re-run chronology? | Completeness | [Assumptions] |
| CHK009 | Do both preview shapes say how to reach every state by hand? | Verifiability | [UI/UX] |
| CHK010 | Does the capability target one durable rule rather than a list of edited CSS lines? | Consistency | [FR-001] |

10 of 10 items carry a traceability marker (100%). Focus areas: clarity/completeness, measurability,
verifiability, consistency — four, within the cap.

## Validation (agent, before gate 1)

**Iteration 1** — each item checked against `spec.md`: CHK001 yes (`dialog[open]`, document scroll);
CHK002 yes (end-of-range vs zero-range, with separate measured cases); CHK003 yes (ten named
scrollports plus the dialogs); CHK004 yes (normal scrolling at the prior offset, `clientWidth` and box
unchanged); CHK005 yes (three distinct before/after observations); CHK006 yes (scrollY/scrollTop,
computed styles, box geometry); CHK007 yes (`probe.py` and `geometry.py`); CHK008 yes (seven
assumptions, including the top-layer sibling measurement and chronology); CHK009 yes (static toggle
plus two live URLs); CHK010 yes (one `reading/R66` rule). No failing item; no second iteration needed.

**[Gap]** — none identified.
