# Requirements checklist: Add verse sits beside Project in the song header

**Spec**: `specs/231-add-verse-in-header/spec.md`

| ID | Quality | Check | Status |
| --- | --- | --- | --- |
| CHK001 | Completeness | Does every stated placement have a named destination (header left of Project, centre invitation for empty)? | [x] |
| CHK002 | Completeness | Is the visibility gate stated for both the header control and the empty invitation? | [x] |
| CHK003 | Clarity | Are "at least one verse" and "empty song" defined by the same `verse_rows` test used in code? | [x] |
| CHK004 | Consistency | Does FR-002's removal of the dashed row agree with US1/AC3 and SC-002? | [x] |
| CHK005 | Measurability | Do SC-001 and SC-002 give a selector and a number that a probe can read? | [x] |
| CHK006 | Coverage | Is the single-`[data-add-verse]` invariant from D003 represented by a requirement and a criterion? | [x] |
| CHK007 | Coverage | Is the edit-permission gate (hymn / read-only) covered by a scenario and a criterion? | [x] |
| CHK008 | Consistency | Do FR-005 and the UI/UX section state the same height, padding and border values? | [x] |
| CHK009 | Traceability | Does every FR and SC have a row in plan.md's traceability table? | [x] |
| CHK010 | Scope | Are models, endpoints, permissions, tokens and motion explicitly excluded? | [x] |

Reviewer-owned. The agent generates this file and never ticks it.
