# Requirements checklist: A passage cue carries its current and end verse

Reviewer-owned. The agent generates this file and never ticks it.

- [ ] CHK001 Does FR-001 name both pieces of data the counter needs — the entry's verse bounds and
      each verse screen's number? [FR-001, completeness]
- [ ] CHK002 Is the `current/end` text and its position after the reference, before the flip, stated
      independently of the DOM? [FR-002, clarity]
- [ ] CHK003 Does FR-003 say what holds steady (the end number, the reference) while the current
      number moves? [FR-003, consistency]
- [ ] CHK004 Is the Go To's end number tied to the chapter actually loaded, not a remembered one?
      [FR-004, consistency]
- [ ] CHK005 Are all three surfaces that can open a Go To covered by one measurable requirement?
      [FR-005, coverage]
- [ ] CHK006 Are the no-counter cases and the incomplete-data case specified, including a song Go To?
      [FR-006, coverage]
- [ ] CHK007 Does FR-007 say what must not change — font, colour, height, button, flip behaviour?
      [FR-007, measurability]
- [ ] CHK008 Does each SC name a read-back or a test module, including the geometry regression?
      [SC-001, SC-002, SC-003, SC-004, traceability]
- [ ] CHK009 Is the single-verse case (`3/3`) stated rather than left to the reader? [US1/AC3, completeness]
- [ ] CHK010 Does the UI/UX section give the before and after strings at a named viewport, not an
      adjective? [UI/UX, measurability]
