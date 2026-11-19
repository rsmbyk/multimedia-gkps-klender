# Requirements checklist — spec 205 (dock centre pace)

Reviewer-owned. The agent generates these and never ticks them; gate 2 presents them unticked.
Each item asks about the requirements, not whether the code works.

| ID | Dimension | Item | Traceability |
| --- | --- | --- | --- |
| CHK001 | Clarity | Is the new pace and curve stated as exact values (200 ms, `½ − cos(πt)/2`) rather than adjectives, so a reader can reproduce the motion? | FR-001 |
| CHK002 | Consistency | Does FR-001 name all three re-centre paths (glideScroll, glideRow, crossing morph) so none keeps the old 400 ms blend by omission? | FR-001, US1/AC4 |
| CHK003 | Consistency | Is the hand block-toggle explicitly excluded (FR-002) so the change cannot be read as retuning R14's 230 ms morph? | FR-002, US2/AC3 |
| CHK004 | Completeness | Are the unchanged behaviours (reduced motion, end clamping, hand cancellation) stated so the slice's boundary is explicit? | FR-003, Edge Cases |
| CHK005 | Measurability | Does each SC name a measurable quantity and the probe/test that reads it, with before/after numbers? | SC-001..003, UI/UX |
| CHK006 | Coverage | Is the reported condition (advancing faster than the glide completes) covered by a scenario at more than one cadence? | US1/AC2-3, SC-002 |
| CHK007 | Honesty | Is the limit that the pace change does NOT remove (the per-crossing collapse-clamp reversal) recorded rather than claimed fixed? | Assumptions, UI/UX |
| CHK008 | Verifiability | Is the proposed duration/curve recorded as an owner-judged candidate so a gate-1 correction is a preview change, not a silent requirement edit? | Assumptions |