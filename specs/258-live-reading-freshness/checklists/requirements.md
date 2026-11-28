# Requirements Checklist: live reading freshness

**Spec**: `specs/258-live-reading-freshness/spec.md` · **Created**: 2026-11-28 · **Depth**: Standard

- [ ] CHK001 Are the four polling endpoints named in FR-001 and FR-002 reflected in the Key Entities? [Completeness, Spec §Requirements]
- [ ] CHK002 Does FR-002 define the fingerprint input precisely enough to reproduce it? [Clarity, Spec §Requirements]
- [ ] CHK003 Does FR-004 name every control class that invalidation disables? [Completeness, Spec §Requirements]
- [ ] CHK004 Is “top-centre” measured in the preview rather than left as a prose adjective? [Ambiguity, Spec §UI/UX]
- [ ] CHK005 Does FR-006 say what happens to the badge while the reload request is pending? [Clarity, Spec §Requirements]
- [ ] CHK006 Are the songbook, song and service list scopes named for each list endpoint? [Consistency, Spec §Requirements]
- [ ] CHK007 Does FR-008 cover all three reconciliation actions — update, remove, insert? [Coverage, Spec §Requirements]
- [ ] CHK008 Does FR-010 state the animation's duration and curve from the preview? [Ambiguity, Spec §UI/UX]
- [ ] CHK009 Does FR-011 make the dated-services/template isolation testable? [Measurability, Spec §Requirements]
- [ ] CHK010 Are light and dark badge states named for review? [Coverage, Spec §UI/UX]
- [ ] CHK011 Does SC-003 measure in-place reload without relying on an implementation detail? [Measurability, Spec §Success Criteria]
- [ ] CHK012 Does SC-004 check node identity rather than only visual output? [Measurability, Spec §Success Criteria]
- [ ] CHK013 Are overlapping polls and failed polls covered by a scenario? [Coverage, Spec §Edge Cases]
- [ ] CHK014 Is the two-cards-one-spec decision recorded with a rationale? [Consistency, Spec §Clarifications]
- [ ] CHK015 Is the 10 s cadence consistent across page and sidebar rules? [Consistency, Spec §Requirements]
- [ ] CHK016 Is the stage left untouched by sidebar-only changes stated in a requirement? [Gap]
