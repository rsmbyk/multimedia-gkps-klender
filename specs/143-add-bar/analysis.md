# Analysis: the add bar opens over the seam, and nothing moves

**Date**: 2026-10-28 · **Spec**: `specs/143-add-bar/spec.md`, accepted at gate 1 the same day · **Plan/tasks**: this commit ·
**Preview**: live — `/tatib/142/`, `/tatib/144/`

**Metrics**: 8 requirements · 6 success criteria · 19 tasks (19 done) · requirement coverage **100%**
· traceability rows **8/8 declared** · verification split **8 test · 0 inspection · 0 manual** · open
findings **1 LOW**, 0 HIGH, 0 CRITICAL.

## Findings

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| F1 | LOW | `test_touch_controls_remain_visible_after_dismissal` remains red — the same 62 tap retries and "element is not visible", identical on unmodified `develop`. | **Carded** as ITEM-153. Not this slice's to fix; the card records only what is known. |
| F2 | LOW | FR-007's second half — that the first seam measures the same **53px of white** as the seams between entries — is asserted only in part: the tests check the box values (34px head margin, 20px between blocks), not the ink. The ink equality was measured in the preview by reading pixels. | **Accepted with the split declared**: the requirement is verified by `inspection` of the measurements recorded in `spec.md` §UI/UX, and the test pins what can be pinned without a pixel decoder in the suite. |

## What the twelve rewritten tests now assert

| Before (in-flow model) | After |
| --- | --- |
| the revealed row is 43.6px tall and keeps 8px above and below its buttons | the row's inner bar is `34px`, absolutely positioned, centred on the row |
| the page moves, and the shift is *bounded* (`≤ row height + 1`) | the page does not move at all: every block's document top is identical |
| a row at rest is `0px` tall | every row keeps a **20px** slot |
| the start bar reveals by `margin-top: -30px` and moves the first entry by `height − 30` | the start bar is centred on its line and the first entry does not move (±0.5px) |
| the seam line does not exist | it paints at `.15` at rest and `.6` when open |

## Coverage

Every requirement and criterion maps to a named test in `plan.md` §Traceability, and all eight run
green. FR-007 is the one row whose evidence is split: its box half is a test, its ink half is the
measurement in `spec.md`. FR-004's hit-area rule is proven by `elementFromPoint` at three points of
the Edit button rather than by a width comparison, so the test fails if a future overlay lands on a
control for any reason.

## History

| Run | Metric line | Result |
| --- | --- | --- |
| 2026-10-28 · pass 1 | 8 req · 6 criteria · 19 tasks · 8 rows · 100% coverage · 1 LOW | gate 2: 39/40 E2E green, the one red being ITEM-153 |
