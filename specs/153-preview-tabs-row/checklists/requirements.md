# Reading Checklist: the preview's verse tabs get their own row

**Spec**: `specs/153-preview-tabs-row/spec.md` · **Created**: 2026-10-29 · **Depth**: Lite

- [ ] CHK001 Are both defects stated with develop's own numbers (the title at 569.6 of 730px, the dialog's focus on `BUTTON.preview__tab`) rather than as a preference? [Measurability, Spec §What the dialog does today]
- [ ] CHK002 Does the spec name the cause — one flex row holding the title and the tabs since spec 085 — so no other explanation fits the squeeze? [Clarity, Spec §What the dialog does today]
- [ ] CHK003 Is the focus target pinned by element (`#previewContent`) rather than by "not a tab", so a third behaviour cannot satisfy the requirement? [Precision, Spec §FR-004, §US3]
- [ ] CHK004 Does the spec say what must not move — the 22px between the rule and the first lyric line, and the passage header's 704×52 — so padding the header is excluded by name? [Consistency, Spec §US2, §FR-005]
- [ ] CHK005 Is the one design choice (which side of the tabs the rule falls on) recorded as an assumption, with its alternative measured, rather than hidden in the preview? [Transparency, Spec §Assumptions]
- [ ] CHK006 Is the keyboard case stated separately from the pointer case, so "no ring" cannot be read as "no focus"? [Coverage, Spec §US3 scenarios 1–2, §SC-003]
- [ ] CHK007 Does the spec keep the verse tabs one `Tab` away once they lose the initial focus, and say why the loop stops there rather than becoming a whole-dialog trap? [Coverage, Spec §US3 scenario 4, §FR-007, §Assumptions]
- [ ] CHK008 Are the three E2E locators that move with the tabs named, so a reviewer can tell a legitimate test change from a rewritten one? [Traceability, Spec §Assumptions]

**Gate 2**: presented unticked on 2026-10-29 and approved as they stand — the tick list stays the
owner's; the agent never ticks it.
