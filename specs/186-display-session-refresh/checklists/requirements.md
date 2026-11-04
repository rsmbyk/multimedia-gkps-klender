# Requirements Checklist: a surface re-reads the session it is showing

**Spec**: `specs/186-display-session-refresh/spec.md` · **Created**: 2026-11-04 · **Depth**: Standard

- [ ] CHK001 Does the spec state every trigger that makes a surface look again, and the ones it deliberately leaves alone? [Completeness, Spec §Requirements FR-001, §Assumptions]
- [ ] CHK002 Is "in the same turn" measurable — is it clear that no timeout or interval is allowed? [Clarity, Spec §Requirements FR-001, §Assumptions]
- [ ] CHK003 Does the spec say what an idle surface must paint after a refused re-read, control by control? [Completeness, Spec FR-003]
- [ ] CHK004 Is the no-change case decided — notify nobody, repaint nothing — rather than left to the implementation? [Ambiguity, Spec FR-005]
- [ ] CHK005 Does the spec avoid inventing a mechanism: no new key, message, verb or timer, with the existing `read()` and subscribers named? [Consistency, Spec FR-004]
- [ ] CHK006 Is the overlay's existing behaviour kept rather than replaced, so the slice cannot double-paint? [Consistency, Spec FR-006]
- [ ] CHK007 Is the defect's evidence in the spec, with the measured read/paint contradiction, rather than described in prose? [Measurability, Spec §What the surfaces do today]
- [ ] CHK008 Are the edge cases the session rule already has — no cookie, corrupt state, back/forward cache — covered by the re-read rather than assumed away? [Coverage, Spec §Edge Cases]
