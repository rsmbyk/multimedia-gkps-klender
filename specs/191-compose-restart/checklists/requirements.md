# Local Stack Checklist: Stack Restart Policy

**Spec**: `specs/191-compose-restart/spec.md` · **Created**: 2026-11-14 · **Depth**: Lite

- [ ] CHK001 Is every service that lacks a restart policy covered by a requirement (web and db),
      with media's existing policy named as unchanged? [Completeness, Spec §Requirements]
- [ ] CHK002 Is "returns" quantified — which services, under which daemon event (machine reboot or
      daemon restart), observed how? [Ambiguity, Spec §User Scenarios]
- [ ] CHK003 Is the deliberate-stop case covered, so the policy cannot fight the operator?
      [Coverage, Spec §User Scenarios]
- [ ] CHK004 Is the start-order window (web starting before the database is healthy) named with its
      expected outcome rather than left silent? [Coverage, Gap]
- [ ] CHK005 Does every FR map to a capability requirement (`local-stack/R3`) instead of
      duplicating an existing one? [Traceability, Spec §Requirements]
- [ ] CHK006 Are the scenarios checkable as written — observable through `docker ps` and the HTTP
      status on the published port, not through adjectives? [Measurability, Spec §Success Criteria]
