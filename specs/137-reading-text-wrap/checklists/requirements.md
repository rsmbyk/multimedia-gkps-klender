# Reading Checklist: A reading page's text wraps at its pane

**Spec**: `specs/137-reading-text-wrap/spec.md` · **Created**: 2026-10-27 · **Depth**: Standard

- [ ] CHK001 Is "wraps at its pane" stated as an observable outcome a reviewer can check without reading CSS — no part of the text past the box, no sideways scroll? [Clarity, Spec §FR-001, §SC-001, §SC-002]
- [ ] CHK002 Does every surface named in the request have a requirement, so "other kind of pages" is enumerated rather than implied? [Completeness, Spec §FR-001–§FR-004]
- [ ] CHK003 Is the Preview modal covered, given that it is not inside the reading pane and would not inherit the rule by location? [Coverage, Spec §FR-004, §US2 scenario 4]
- [ ] CHK004 Is the difference between *this* fix and the deliberate truncations stated, so unclipping them is visibly out of scope? [Consistency, Spec §FR-006, §US3]
- [ ] CHK005 Is "the layout must not re-measure" a requirement with a number, rather than an intention? [Measurability, Spec §FR-007, §SC-005]
- [ ] CHK006 Are the widths and type sizes quoted from a measurement a reader can repeat, with the command named? [Measurability, Spec §UI/UX]
- [ ] CHK007 Does the spec say what happens to text that already fits, so a no-op page is a stated outcome? [Clarity, Spec §FR-008, §SC-003]
- [ ] CHK008 Is the unanswered Clarify question recorded as an assumption with its recommendation, rather than left open? [Ambiguity, Spec §Clarifications]
- [ ] CHK009 Are the surfaces deliberately left alone named — `/manage/`, the admin, the projector, the OBS dock? [Coverage, Spec §Assumptions]
- [ ] CHK010 Is the fixture distinguished from a product limit, so a 1,000-character title is not read as a new maximum? [Clarity, Spec §Assumptions]
- [ ] CHK011 Supersedes CHK008: the scope question was reopened and answered by the owner, and the spec now records the answer under `## Clarifications` with the assumption that had stood in its place removed. Is the answer consistent with FR-002 to FR-004, and does no other section still call it an assumption? [Consistency, Spec §Clarifications, §FR-002–§FR-004, §Assumptions]
- [ ] CHK012 Supersedes the figure in CHK010: the spec first called the fixture a 1,000-character title, but `TataIbadah.name` and `Song.title` are 64 characters — that is the widest storable value, and it is what the live records carry. Does every artifact now name the real limits, and does the fixture still read as a measurement rather than a new maximum? [Accuracy, Spec §US1, §SC-002, §Assumptions, §UI/UX]
