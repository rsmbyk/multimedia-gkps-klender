# Requirements checklist — spec 246

Reviewer-owned; the agent generates and never ticks these items.

| ID | Quality dimension | Item | Traceability |
| --- | --- | --- | --- |
| CHK001 | Completeness | Every acceptance scenario is covered by a requirement or an assumption. | US1/US2 → FR-001..006 |
| CHK002 | Clarity | `media-library` is named as a destination value, not a fourth reading section. | FR-001, Assumptions |
| CHK003 | Consistency | The direct-load and in-place-fetch paths promise the same section identity. | FR-001, Edge cases |
| CHK004 | Measurability | SC-001..003 name exact request counts, row counts and visibility. | SC-001..003 |
| CHK005 | Coverage | All three section rail tiles are covered after Media Library. | US1 AC2/3 |
| CHK006 | Coverage | The unchanged own-tile toggle is stated as a guard. | FR-004, US2 AC1 |
| CHK007 | Consistency | R62's pending-state rules are named as out of scope, not silently replaced. | Out of scope, FR-005 |
| CHK008 | Completeness | The visible empty-list copy is accounted for on both base and fixed paths. | UI/UX table |
