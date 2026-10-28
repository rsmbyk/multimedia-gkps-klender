# Analysis: a service entry draws no box until it is pointed at

**Date**: 2026-10-28 · **Spec**: `f5ca87f0` (pack, `spec.md` as accepted) · **Plan/tasks**:
uncommitted at the time of writing · **Preview**: `specs/142-entry-surface/preview/preview.html`

**Metrics**: 6 requirements · 6 success criteria · 14 tasks (14 done) · requirement coverage
**100%** · traceability rows **12/12 declared** · verification split **7 test · 5 inspection · 0
manual** · open findings **0 CRITICAL, 0 HIGH, 2 LOW** — F1 resolved by the split.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | **HIGH** | The branch carries slice 143's add-bar work as `951afa6f` plus uncommitted CSS, so 13 of the 42 E2E tests are red on this branch — 12 asserting the old add-row mechanism (`0px at rest`, `8px` padding when open, the `13.6px` start-bar shift) and 1 pre-existing. None is caused by this slice's two removed declarations. | **Split before merge.** `feat/143-add-bar` off this branch, then this branch's suite is green on its own terms. Reported, not silently fixed: the fix is a branch operation the owner has not authorised. |
| F2 | LOW | `test_touch_controls_remain_visible_after_dismissal` is red on unmodified `develop` — the same 62 tap retries and "element is not visible". Found while running this slice's suite. | **Carded** as ITEM-153. Not this slice's to fix, and the card records only what is known: the tap never becomes actionable; which of the four taps has not been narrowed. |
| F3 | LOW | The static preview carries copies of `tokens.css` and `components.css` frozen at `ca71c850`, so it drifts from the live stylesheets by design. | **Accepted.** The freeze is what keeps the **Now** column showing the retired box; `preview/README.md` records the commit and `build_preview.py` regenerates both. |

## Coverage

Every requirement and criterion in `spec.md` has a row in `plan.md` §Traceability, and each row
names either a test function or what an inspector looks at. The two rows resting on `inspection`
(FR-005, SC-005 — the deleted tokens; FR-006 — that nothing else moved) are un-testable by
construction: one is proven by absence, the other by the diff's shape. The rule SDD-13 exists to
protect is respected — both are verifiable, so neither is an un-ticked gap.

The one requirement whose evidence is weakest is **FR-004's media half**: no test asserts the media
row's 80px floor or its 64px tile inset, so the row rests on the owner's look at `/tatib/144/` at
gate 1. Recorded here rather than upgraded, because a test written after the fact proves the
stylesheet, not the requirement.

## History

| Run | Metric line | Result |
| --- | --- | --- |
| 2026-10-28 · pass 1 | 6 req · 6 criteria · 12 rows · 100% coverage · 2 HIGH · 1 LOW | gate 2, findings F1–F3 reported; F1 blocks the merge, not the slice |
