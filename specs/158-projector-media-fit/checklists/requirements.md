# Reading Checklist: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Is the defect measured in painted pixels and named with both causes — the CSS cap and the `Math.min(1, …)` — so a reader can check the claim without running the app? [Measurability, Spec §What the projector does today]
- [ ] CHK002 Is "the smallest possible" defined as one rule (`min(width ratio, height ratio)`) rather than left as an adjective an implementer could read either way? [Clarity, Spec §Assumptions 1]
- [ ] CHK003 Does the spec say what happens on the *first* `T` press, given the default fit already equals one of the two states — so no reader expects a third state? [Ambiguity, Spec §Assumptions 2, §FR-004]
- [ ] CHK004 Is the clipped overflow stated as reachable — panned by drag and wheel, never by a scrollbar — instead of being lost? [Consistency, Spec §FR-009, §Assumptions 6]
- [ ] CHK005 Is the fit state's lifetime stated — per media screen, reset on another entry, kept across a document's pages? [Completeness, Spec §FR-005, §Assumptions 3]
- [ ] CHK006 Does the spec keep every other screen kind out of the change, naming the passage's `T` explicitly? [Coverage, Spec §FR-008, §US3.5]
- [ ] CHK007 Is the shortcut's home stated with its layout limit — the sheet must still fit at 1024×768 — rather than "add a row"? [Measurability, Spec §FR-007, §SC-007]
- [ ] CHK008 Is the reading page's Preview dialog explicitly out of scope, with the reason and the follow-up, so its unchanged sizing is not read as an oversight? [Coverage, Spec §Assumptions 4]
- [ ] CHK009 Can the success criteria be checked from the preview and the page without reading the implementation — numbers, window sizes and media named? [Measurability, Spec §Success Criteria]
- [ ] CHK010 Does the spec say how panning and the corner's click-to-navigate coexist, so a drag cannot silently remove previous/next? [Consistency, Spec §FR-011, §US4.6]

**Gate 2**: accepted by the owner on 2026-10-29 — this list (presented unticked, as gate 2 requires),
`plan.md` with its traceability table (19 test · 3 inspection · 0 manual), `tasks.md` and `analysis.md`
were shown together, and the same answer authorised implementation. The boxes above stay unticked: they
are the reviewer's, and the owner's accept is the gate.
