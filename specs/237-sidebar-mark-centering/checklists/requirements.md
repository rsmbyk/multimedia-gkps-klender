# Reading Checklist: sidebar mark centring

**Spec**: `specs/237-sidebar-mark-centering/spec.md` · **Created**: 2026-11-24 · **Depth**: Lite

- [ ] CHK001 Is the reported surface — the kind icon in the Tata Ibadah contents row — named in a testable scenario? [Completeness, Spec §US1]
- [ ] CHK002 Is the root cause — baseline alignment while the number uses `align-self: center` — stated with the exact selectors? [Clarity, Spec §Introduction]
- [ ] CHK003 Is "centred" measurable as box-centre minus row-centre within ±1px, not as a visual adjective? [Clarity, Spec §UI/UX, §SC-001]
- [ ] CHK004 Are the before numbers given for both one-line (−4px) and two-line (−11.5px) rows? [Completeness, Spec §UI/UX]
- [ ] CHK005 Is the drag copy covered, given spec 063 centred its number too? [Coverage, Spec §US3, §FR-003]
- [ ] CHK006 Is the slot badge's movement with its mark stated with measured offsets? [Coverage, Spec §US3, §SC-002]
- [ ] CHK007 Are horizontal geometry, row heights, clamp and wrap protected from the change? [Consistency, Spec §US2, §FR-002]
- [ ] CHK008 Is the songbook sidebar explicitly out of scope, since it shares `.songrow`? [Consistency, Spec §Edge Cases]
- [ ] CHK009 Are both themes and 1440/1024/390px widths reachable on the live preview? [Coverage, Spec §UI/UX, Preview README]
- [ ] CHK010 Is the patch bump recorded as an expectation rather than a gate-1 decision? [Ambiguity, Spec §Assumptions]
- [ ] CHK011 Is every functional requirement traced to at least one scenario? [Coverage, Spec §Requirements]
