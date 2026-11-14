# Reading Checklist: the active Tata Ibadah lasts only the browser session

**Spec**: `specs/184-display-session-scope/spec.md` · **Created**: 2026-11-03 · **Depth**: Lite

- [ ] CHK001 Is the boundary defined on the state's own stamp rather than on the act that usually
  produces it, so a restored tab or a hand-set value is judged by the same rule? [Consistency,
  Spec §FR-008]
- [ ] CHK002 Is "browser session" defined operationally — a session cookie's lifetime — with the
  session-restore and crash cases recorded, so a reviewer knows what the rule does and does not
  promise? [Clarity, Spec §The display state, §Assumptions]
- [ ] CHK003 Are the writers and readers enumerated, so the slice cannot miss the projector's own
  storage code or the overlay's read? [Coverage, Spec §The display state]
- [ ] CHK004 Is spec 119's "closing every surface changes nothing" carried forward as a kept
  contract, with the scenario that proves it, rather than left to inference? [Consistency, Spec
  §US2 scenario 3]
- [ ] CHK005 Is first paint addressed explicitly — not "eventually empty" — in both the requirement
  and the success criterion? [Measurability, Spec §FR-002, §SC-002]
- [ ] CHK006 Is the two-surfaces-mint-together race solved by an outcome the state can be checked
  against, not by an assumed sequence? [Precision, Spec §FR-010]
- [ ] CHK007 Is the upgrade path stated — a state without a stamp reads as none, no migration — so
  the first load after the deploy is not a surprise? [Completeness, Spec §FR-009]
- [ ] CHK008 Does the spec say what happens when cookie storage is unavailable, including the cost
  (a reload starts idle), rather than hand-waving a fallback? [Coverage, Spec §FR-006]
- [ ] CHK009 Is "no display data reaches the server" measurable now that a cookie travels, with the
  marker's contents stated? [Measurability, Spec §FR-005, §SC-004]
- [ ] CHK010 Is the cookie's scope stated (path, no expiry, same-site) so all four routes are covered
  without a second marker? [Precision, Spec §The display state]
- [ ] CHK011 Are today's numbers recorded with the probe that produced them, so the defect is
  evidenced rather than asserted? [Traceability, Spec §What the surfaces do today]
- [ ] CHK012 Is the UI/UX skip justified against SDD-06 — every state this slice produces already
  exists and is designed — and is the live restart walkthrough named? [Completeness, Spec §UI/UX]
- [ ] CHK013 Does the spec avoid inventing a new empty state, a new control or a new store? [Scope,
  Spec §Assumptions]
- [ ] CHK014 Are the acceptance tests named for both directions — a new session idle, the same
  session kept — rather than only the report's direction? [Traceability, Spec §SC-001–§SC-003]

**Gate 1**: presented unticked on 2026-11-03 — the tick list stays the owner's; the agent never
ticks it.
