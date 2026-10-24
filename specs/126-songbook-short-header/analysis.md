# Analysis: A song page cites its songbook by its short name

**Date**: 2026-10-24 (run 2, after the gate-2 fix round)
**Artifacts read**: `spec.md` @ `07b024a9`, `plan.md` @ `6c8dc552`, `tasks.md` @ `2b3e9126`
**Metrics**: 7 requirements · 5 success criteria · 8 acceptance scenarios · 21 tasks · 100% coverage · 0 CRITICAL · 0 open findings

## Findings

| ID | Category | Severity | Location | Summary | Recommendation | Cost if left | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A1 | Coverage gap | MEDIUM | `plan.md` §Traceability (FR-005) vs `tasks.md` | The plan verified FR-005 (the tab title) with `ReadingViewTests::test_song_detail_tab_title_uses_the_short_reference`, but no task created that test — the requirement had a file and no owner in the task list. | Added `T006` for the pin and shifted the phase's later tasks by one, so the tab title is red-first like the header. | Converge would flag FR-005 `partial` against a test that does not exist. | **fixed 2026-10-24** |
| G1 | Capability alignment | MEDIUM | `spec.md` §Requirements · `plan.md` §Phase 1 · `tasks.md` T020 | The requirements cited `new: reading` and `new: saved-reading`, but the repo has no `docs/spec/` capability tree, so the declared capabilities had no home and a later reader could not tell where the requirement lives. | The owner's fix-round decision: the slice **starts the tree** at `docs/spec/reading.md`, with the saved copy as a requirement inside `reading` rather than a capability of its own. Applied to the spec (FR-004's capability, plus the assumption and the two Clarifications entries), the plan (Phase 1, structure) and the tasks (T020 now writes the delta). | The capability names would live only in dated slice specs, and the next reading slice would repeat the note. | **fixed 2026-10-24** (owner, fix round before gate 2) |

Passes A (duplication), B (ambiguity), C (underspecification), D (constitution — no `CONSTITUTION.md`), F (inconsistency) found nothing.

## Coverage

| Requirement | Has task? | Task IDs | Notes |
| --- | --- | --- | --- |
| FR-001 | yes | T003, T008 | the view's citation expression |
| FR-002 | yes | T007, T008 | fallback for a blank short name |
| FR-003 | yes | T010 | ordinary songbook, blank short name |
| FR-004 | yes | T013, T015 | saved renderer parity |
| FR-005 | yes | T006, T008 | tab title follows the citation |
| FR-006 | yes | T011 | ordinary songbook with a short name set |
| FR-007 | yes | T009, T012, T016 | untouched surfaces, via re-runs and one inspection |
| SC-001 | yes | T003 | header text is exactly the reference |
| SC-002 | yes | T004, T005, T007 | sub-number, unnumbered, fallback |
| SC-003 | yes | T010 | ordinary page unchanged |
| SC-004 | yes | T014 | saved/server agreement on text and title |
| SC-005 | yes | T009, T012, T016 | existing assertions re-run |
| US1/AC1–AC4 | yes | T003, T004, T005, T007 | one pin each |
| US2/AC1–AC2 | yes | T010, T012 | the second is the inspection row |
| US3/AC1–AC2 | yes | T014, T016 | parity plus the existing ordinary eyebrow case |

**Unmapped tasks**: T001, T002 (declared `n/a`), T017–T021 (delivery steps from the repo's git, versioning and board conventions — Spec Kit's Tasks has no requirement for them, and SDD's delivery phase generates them from what the repo declares).

## Notes on severity

No CRITICAL: no constitution exists, all three artifacts are present, and every requirement has an owner.
A1 was mechanical and was applied by the agent. G1 was an intent question — where capability declarations
live — so it was the owner's at the fix round; his answer changed the spec as well as the plan, so the spec
records the revision in its status line and `## Clarifications` rather than silently, and gate 1 was
reaffirmed when gate 2 was presented.

## History

- 2026-10-24 · 0 crit · 2 findings · 1 fixed · 1 open
- 2026-10-24 (run 2) · 0 crit · 2 findings · 2 fixed · 0 open
