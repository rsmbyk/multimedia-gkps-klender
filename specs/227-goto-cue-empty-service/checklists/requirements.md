# Requirements checklist: A Go To still names itself with no service under it

Reviewer-owned. The agent generates this file and never ticks it.

- [ ] CHK001 Does FR-001 name both empty states — no service and a service with no entries? [FR-001, completeness]
- [ ] CHK002 Is the cue's required content — label, flip, baits, progress, Back — stated without
      relying on an implementation detail? [FR-002, clarity]
- [ ] CHK003 Does FR-003 protect the populated-service cue path from the reordered guard? [FR-003, consistency]
- [ ] CHK004 Is the return to the empty notice after Back specified separately from the Go To's
      own paint? [FR-004, coverage]
- [ ] CHK005 Is the "no new state or message" boundary measurable, not merely asserted? [FR-005, measurability]
- [ ] CHK006 Does each SC have a read-back or a named test module? [SC-001, SC-002, SC-003, traceability]
- [ ] CHK007 Is the no-service case distinguishable from the empty-service case in the acceptance
      scenarios? [US1/AC1, US1/AC2, coverage]
- [ ] CHK008 Are the states a dock- or reading-started Go To can reach covered? [US1/AC6, coverage]
