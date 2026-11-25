# Requirements checklist — spec 242 (dock top pin)

Reviewer-owned. The agent generates these and never ticks them; gate 2 presents them unticked.
Each item asks about the requirements, not whether the code works.

| ID | Dimension | Item | Traceability |
| --- | --- | --- | --- |
| CHK001 | Clarity | Is "off-screen" defined as exact geometry (the live block's bottom at or above the scrollport's top edge) rather than "looks gone", so the boundary with the native sticky top-pin is decided by a number? | FR-001, Assumptions, US1 |
| CHK002 | Completeness | Does FR-001 require a faithful copy (number, name, subtitle, chevron, selected face) and the exact pinned geometry, so a plain caption strip cannot satisfy the requirement? | FR-001, SC-001 |
| CHK003 | Consistency | Is the pin's scope stated as live-entry-only, with the owner's answer recorded, and are non-live headers and the go to's `.offstrip` explicitly out of scope rather than silently omitted? | FR-005, Assumptions, US3/AC2 |
| CHK004 | Coverage | Are both halves of the pin pair covered — the top clone's stand and its give-way — with a test each, including the frame that crosses the fold? | US1, US2, SC-001..003 |
| CHK005 | Measurability | Does each SC name a quantity (visibility, offset, radius, frame count, centre offset, byte-identical state) and the probe or test that reads it, with before/after values? | SC-001..006, UI/UX |
| CHK006 | Verifiability | Is the click act pinned to the centre control's act with the display state explicitly unchanged, so "re-centre" cannot quietly become "re-project"? | FR-004, SC-004, US3/AC1 |
| CHK007 | Consistency | Does the per-frame requirement agree with R15's one-motion rule and R17's existing corner tracking, naming the extra paint-only reconciliation without changing the motion curve? | FR-002, Assumptions |
| CHK008 | Honesty | Is the mechanism boundary recorded — sticky cannot leave its `li`, so the block-above range needs a list-level clone — instead of claiming the real header itself stays pinned? | US1 mechanism finding, Assumptions |
| CHK009 | Completeness | Are regression surfaces named (bottom pin, NEXT band, header wash, entry anatomy, go to strip) so a change to them cannot pass as "unchanged" by silence? | FR-005, SC-006 |
| CHK010 | Clarity | Is the reduced-motion requirement a same-paint guarantee, not a "short transition", and is it measurable? | FR-002, SC-005 |
