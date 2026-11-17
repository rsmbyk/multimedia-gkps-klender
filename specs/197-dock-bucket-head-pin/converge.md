# Converge: The dock's bucket head owns the strip above its label

**Spec**: `specs/197-dock-bucket-head-pin/spec.md`
**Pass**: 1 · **Checked**: every row of `plan.md`'s traceability table, by the method it declared
**Outcome**: converged

## Pass 1

What was checked, row by row:

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001 | test | `tests/e2e/test_dock_bucket_head.py::test_a_pinned_bucket_head_leaves_no_row_above_it` — green; head top equals the scroller's top (0.00px) and the strip's topmost element is the head. Red on develop's stylesheet (`68 != 64`). |
| FR-002 | test | `::test_the_label_holds_its_place_between_rest_and_pinned` — green; the label reads one offset at rest and pinned. |
| FR-003 | inspection | `static/styles/design/obs-dock.css` still declares `scroll-padding-top: 37px`; the head's foot measures 100.52px at rest and pinned, so the reserve still covers it. The consequence is `::test_the_cursor_still_parks_below_the_head`. |
| FR-004 | test | `::test_nothing_below_the_head_moves` — green; the first row starts at the head's foot at rest, the head's height is unchanged when pinned, and the row under a pinned head starts at its foot. The diff touches no runner rule (`git diff develop -- static/styles/design/obs-dock.css` = three declarations, all inside the picker's rules). |
| FR-005 | test | `::test_consecutive_buckets_keep_their_air` — green; each boundary reads the first label's offset + 12px. Red on develop (`10 != 26`). |
| US2/AC1 | test | `::test_the_cursor_still_parks_below_the_head` — green; every parked row sits at or below the pinned head's foot. It also passes on develop, which is correct: it guards a behaviour this slice must not change. |
| US1/AC2 | manual | Owner scroll of `/obs/dock` at 449×604 during the preview rounds; the strip showed "25 OKT 2026" on develop and nothing after the fix. |
| SC-001 | test (hit test stands in for the pixel count) | the count itself was the preview's evidence: 0 non-background pixels across 514 offsets, against up to 9,715 on develop. |
| SC-002 | test | same test as FR-001. |
| SC-003 | test | same test as FR-002, at 1,600 offsets in the preview probe and at rest/pinned in the suite. |
| SC-004 | test | FR-004's test plus the cursor test. |
| SC-005 | test | FR-004's test. |
| SC-006 | test | FR-005's test. |
| preview parity | inspection | `preview/index.html` opens at the pinned offset and prints `4.0px / span.servicerow__n / 10.0px` against `0.0px / h3.group__head / 26.0px` — the same numbers the suite asserts (`14 + 12`). |

## Findings

| # | Type | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | observed consequence | `.dock__note` — the picker's empty-state line ("No Tata Ibadah yet.") — sits 4px higher than before, because it shares the scroll body whose top padding moved into the head. It appears only when the picker holds no row, and no requirement names its offset. | left as is; recorded here and in the fold's `modified` block is not needed (no requirement changes) |
| 2 | — | The suite's two regression rows (label invariant, nothing below the head) pass on develop as well as after the fix. | by design: they guard what the change must not disturb, and the analysis (A3) predicted exactly this |

No `missing`, `partial`, `contradicts` or `unrequested` gap was found. The two red tests on develop's
stylesheet (`FR-001`, `FR-005`) are the slice's own defect, and they are green with the slice's
stylesheet.

## Suite

- `tests.e2e.test_dock_bucket_head` — 5 tests, green.
- `tests.e2e.test_obs_dock` + `multimedia.web.test_obs_dock` — 19 tests, green (no regression in the dock's
  display state, the go to, or the picker's page tests).