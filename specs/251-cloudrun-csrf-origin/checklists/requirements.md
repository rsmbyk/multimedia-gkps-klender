# Requirements checklist: Cloud Run writes pass CSRF

Reviewer-owned. The implementing agent generates these items and never ticks them.

- [ ] CHK001 Does FR-001 name the exact proxy header and the value that makes a request secure? [FR-001]
- [ ] CHK002 Does FR-002 state an observable outcome at the write endpoint, not just a setting value? [FR-002]
- [ ] CHK003 Is FR-003 measurable from the slice diff, with no endpoint/template/static edits? [FR-003]
- [ ] CHK004 Is US1's independent test able to fail on unfixed code without a deployment? [US1]
- [ ] CHK005 Are SC-001 and SC-002 numbers or concrete observations (403→200, 403→404)? [SC-001, SC-002]
- [ ] CHK006 Does the negative case prove CSRF is still enforced when the setting is absent? [SC-003]
- [ ] CHK007 Is `UI/UX` an honest `n/a` for a settings-only change? [UI/UX]
- [ ] CHK008 Are all assumptions defaults the owner did not state, each with a reason? [Assumptions]
- [ ] CHK009 Does the capability fold name one durable requirement, not the deployment steps? [FR-001]
- [ ] CHK010 Is the deployment step recorded as manual evidence rather than claimed as done? [SC-002]

**[Gap]** — none identified at generation.
