# Reading Checklist: Song-row focus ring is clipped at the list top

**Spec**: `specs/223-songrow-focus-ring-clip/spec.md` · **Created**: 2026-11-22 · **Depth**: Lite

- [ ] CHK001 Does US1 name the exact symptom — the top edge of the ring cut by the scrollport when the first row is focused — with an independent browser check? [Coverage, Spec §US1]
- [ ] CHK002 Are the measured current values (row top, host top, 0px padding, UA outline, pixel-diff boundary) stated as numbers rather than adjectives? [Measurability, Spec §UI/UX]
- [ ] CHK003 Does the spec separate the two candidates and leave one explicit clarification marker for the choice? [Clarity, Spec §FR-006, §Assumptions]
- [ ] CHK004 Is the non-defect explanation — no scroll, `scrollTop = 0` and `scrollHeight = clientHeight` — stated so a scroll fix cannot pass? [Consistency, Spec §Edge Cases, §SC-002]
- [ ] CHK005 Are unchanged row height, 1px pitch, hover fill and selected fill called out? [Scope, Spec §FR-002]
- [ ] CHK006 Are both focus paths (Tab, and key after pointer focus) covered rather than only one? [Coverage, Spec §SC-004]
- [ ] CHK007 Are dark and light themes and all three named viewports in scope? [Coverage, Spec §FR-004]
- [ ] CHK008 Is the first sidebar and every other focusable control explicitly out of scope? [Scope, Spec §FR-005]
- [ ] CHK009 Can each criterion be observed in a browser without mocking the DOM or reading CSS internals? [Measurability, Spec §Success Criteria]
- [ ] CHK010 Does the preview name every state reachable by hand, including unfocused and scrolled-to-last-row? [Coverage, Spec §UI/UX]
- [ ] CHK011 Is the candidate's effect on the bottom edge stated so the existing 8px padding is not lost? [Consistency, Spec §US1 scenario 4]
