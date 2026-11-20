# Requirements checklist — spec 208 (dock stuck corner)

Reviewer-owned. The agent generates these and never ticks them; gate 2 presents them unticked.
Each item asks about the requirements, not whether the code works.

| ID | Dimension | Item | Traceability |
| --- | --- | --- | --- |
| CHK001 | Clarity | Is "pinned" defined as exact geometry (top at the edge within 0.5 px AND the block still reaching below it) rather than "looks stuck", so the far-above-row case is decided by the definition? | FR-001 |
| CHK002 | Completeness | Does FR-002 name every path that moves or resizes the list — scroll, sync, glide frames, crossing-morph frames, hand-toggle frames, landings, resize — so none keeps the stale class by omission? | FR-002, root causes 1–3 |
| CHK003 | Consistency | Does FR-004 name exactly what of the NEXT band is unchanged (click, label, truncation, label motion guard) and what is superseded (placement, yield), so the two are not conflated? | FR-004, FR-011 |
| CHK004 | Coverage | Are both reported states covered by their own P1 story and their own E2E pin, at rest, without a hand scroll reconciling them? | US1, US2, SC-001, SC-002 |
| CHK005 | Coverage | Is the height-only path (hand toggle, no scroll event) covered, not just the scroll and crossing paths? | US2/AC2, SC-003 |
| CHK006 | Measurability | Does each SC name the quantity (class presence, painted radius, offset) and the test or probe that reads it, with before/after numbers? | SC-001..006, UI/UX |
| CHK007 | Consistency | Does the live-tracking requirement (US3) agree with R15's one-motion rule, and is the per-frame cost stated rather than hidden? | US3, Assumptions |
| CHK008 | Honesty | Is the scope boundary explicit — the go to strip and the reading page's pinned header carry no corner state and are untouched? | FR-006, Assumptions, Edge Cases |
| CHK009 | Verifiability | Is the reduced-motion instant paint required to reconcile in the same paint, so the instant path is not left a frame stale? | FR-005, SC-006 |
| CHK010 | Clarity | Is the bottom pin's trigger stated as exact geometry (the header's bottom past the scrollport's bottom edge — including while the header is still partly visible), not "looks cut" or "fully off"? | FR-007, US4/AC1 |
| CHK011 | Consistency | Does the stack ruling name both list-level slots, who holds the edge (NEXT) and where the pin sits (abutting the band's measured top), with no gap, and is the band's click/label explicitly unchanged? | FR-009, FR-004, US4/AC3 |
| CHK012 | Verifiability | Is the strip's click pinned to the centre control's act with the display state unchanged, so "re-centre" cannot silently become "re-project"? | FR-010, SC-010, US4/AC4 |
| CHK013 | Honesty | Is the mechanism boundary recorded — the header node itself cannot bottom-pin (first child), the pin is a list-level cloned representation, and the NEXT band is list-level to escape its own cage — rather than claiming the header or band moves? | US4 mechanism finding, Assumptions |
| CHK014 | Completeness | Does FR-011 keep the NEXT band always visible and pinned flush via a list that fills the scrollport (min-height, flex-bottom slots, no body bottom padding), so it never dangles after the last row, with a verifiable SC? | FR-011, SC-013 |
