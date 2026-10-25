# Requirements checklist — the Tata Ibadah list groups by age

**Spec**: `specs/132-tatib-sidebar-date-buckets/spec.md`
**Owner**: reviewer-owned; the agent generates and never ticks.
**Focus areas**: the boundary rule · the label set · the two surfaces · what stays unchanged

## The boundary rule

- [x] CHK001 — Is every date accounted for by exactly one bucket, with no gap and no overlap? [Completeness, Spec §FR-002]
- [x] CHK002 — Are the two edges (day 0, day 30, day 31) stated so they can be tested without reading the code? [Measurability, Spec §SC-002]
- [x] CHK003 — Is "today" defined once, and does the definition say which calendar day it is? [Clarity, Spec §FR-003]
- [x] CHK004 — Does the spec say what happens when the window and the calendar year disagree (early January)? [Coverage, Spec §Edge Cases]
- [x] CHK005 — Is it clear that the bucket is derived, never stored, so nothing goes stale at midnight? [Consistency, Spec §Key Entities]
- [x] CHK006 — Is a future service in a later calendar year still covered by a bucket? [Coverage, Spec §Edge Cases]

## The label set

- [x] CHK007 — Are the four labels given verbatim, once, and in their drawing order? [Clarity, Spec §FR-001]
- [x] CHK008 — Does the spec say whether the labels are stored in sentence case or uppercase? [Consistency, Spec §FR-001]
- [x] CHK009 — Is the vocabulary stated as fixed — no setting, no per-user window? [Assumption, Spec §Assumptions]
- [x] CHK010 — Does the spec say what the accessible name is, given the uppercase drawing? [Accessibility, Spec §Edge Cases]
- [x] CHK011 — Is the choice of English for the labels reconciled with the Indonesian month names inside a row? [Consistency, Spec §Assumptions]

## The two surfaces

- [x] CHK012 — Does every surface that groups dated services name the same four buckets? [Completeness, Spec §FR-006, §FR-007]
- [x] CHK013 — Is the saved copy's present day defined, and does the spec say a page re-buckets when it is opened later? [Coverage, Spec §FR-007]
- [x] CHK014 — Is the dock's own row furniture (today/upcoming marks, Indonesian dates) explicitly preserved? [Completeness, Spec §FR-006]
- [x] CHK015 — Is the in-page reconciler's group identity covered, so two groups are never confused on navigation? [Consistency, Spec §FR-008]
- [x] CHK016 — Are the removed things named — the month heading and the month key? [Completeness, Spec §FR-008]

## What stays unchanged

- [x] CHK017 — Does a requirement state that the heading's typography, stickiness and the divider rule are untouched? [Consistency, Spec §FR-011]
- [x] CHK018 — Is template mode explicitly out of scope, with its own heading? [Coverage, Spec §FR-010]
- [x] CHK019 — Is the filter's behaviour across the new buckets specified — hiding rows, hiding an emptied bucket, clearing? [Coverage, Spec §FR-009]
- [x] CHK020 — Is an empty bucket's absence stated, rather than left to "no rows"? [Clarity, Spec §FR-005]
- [x] CHK021 — Are the surfaces that are deliberately out of scope named (media library, search, date picker)? [Boundary, Spec §Assumptions]
- [x] CHK022 — Is the order inside `Upcoming` stated as a rule with a tiebreak, not as an example? [Measurability, Spec §FR-004]
