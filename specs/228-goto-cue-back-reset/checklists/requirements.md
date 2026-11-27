# Requirements checklist: Back clears the Go To from the cue over an empty stage

Reviewer-owned. The agent generates this file and never ticks it.

- [ ] CHK001 Does FR-001 name every part of the Go To cue that must be cleared, not just the label? [FR-001, completeness]
- [ ] CHK002 Is the reset of `#cue-next` stated precisely enough to test — hidden, unpressed, unnamed? [FR-002, measurability]
- [ ] CHK003 Are all three exit paths named, and is the reason they share `renderCue()` given? [FR-003, traceability]
- [ ] CHK004 Is the spec 227 behaviour protected explicitly while the removal changes? [FR-004, consistency]
- [ ] CHK005 Is the "no other file changes" boundary checkable from a diff? [FR-005, measurability]
- [ ] CHK006 Does each SC name the assertion or the test module that measures it? [SC-001, SC-002, SC-003, coverage]
- [ ] CHK007 Are the two empty situations separated in the acceptance scenarios? [US1/AC1, US1/AC2, coverage]
- [ ] CHK008 Is the never-opened cue state distinguished from the after-Back state? [US1/AC4, clarity]
- [ ] CHK009 Does FR-006 say the separator is hidden rather than removed, and name both idle situations? [FR-006, completeness]
- [ ] CHK010 Are the preserved mouse functions — fullscreen, service list, keys, find — stated as explicitly as the disabled ones? [FR-007, FR-009, consistency]
- [ ] CHK011 Is the cursor requirement checkable without depending on an internal class name? [FR-008, measurability]
- [ ] CHK012 Is the Go To detour explicitly excluded from the idle rules? [US2/AC5, coverage]
- [ ] CHK013 Is the hidden next button required to be actually not displayed, not just carry the attribute? [FR-002, correctness]
