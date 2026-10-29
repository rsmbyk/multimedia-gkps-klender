# Convergence: The Transfers scrollbar sits at the dialog's edges

**Spec**: `specs/152-transfer-scrollbar-edge/spec.md` (revision 2)
**Passes**: 1 of 3

## Pass 1 — 2026-10-29

Checked every row of `plan.md`'s traceability table by the method it declared, against the code in
the worktree (`feat/152-transfer-scrollbar-edge`, one stylesheet and one test module outside the
pack) and the runs recorded at the bottom.

| Gap | Type | Requirement | Evidence |
| --- | --- | --- | --- |
| Spec 149's `test_a_long_transfer_list_scrolls_inside_the_dialog` measured the list's box against the dialog's **padding** edge (`box.bottom − border − paddingBottom`) and read the end-of-scroll gap as `innerBottom − last.bottom + paddingBottom`. FR-001 moved that edge to the border, so the test reported `past = 22` and would have reported `endGap = 44`. The code was right; the older test still pinned the contract revision 2 replaced. | `contradicts` | FR-001, FR-004 | the suite's first run: `AssertionError: 22 not less than or equal to 0.5 : the list paints past the dialog padding`. **Not deleted and not weakened**: `innerBottom` is now `box.bottom − border`, and `endGap` is `innerBottom − last.bottom`, so the test still asserts "the list paints nowhere past the dialog" and "the last row ends 22px above the border" — the same two outcomes, measured against the edge that now applies. Re-run: green |

**Outcome**: one finding, fixed inside the slice. Nothing appended as a task, nothing accepted as a
gap.

### Per-row verification

| Row | Method | Evidence |
| --- | --- | --- |
| FR-001, SC-002, US1/AC2 | `test` | `test_the_transfer_list_reaches_the_dialog_edges` — green: `dialog.right − list.right − 1 = 0`, `dialog.bottom − list.bottom − 1 = 0`, `list.left − dialog.left − 1 = 0`, `getComputedStyle(dialog).overflow = clip`, and the list reports `scrollHeight > clientHeight`. Red before the rule at `right = 22` |
| FR-003, SC-003, US2/AC1 | `test` | `test_the_transfer_content_keeps_its_insets` — green: row left 23, `dialog.right − row.right = 23 + (offsetWidth − clientWidth)` = 28, separator `1px` |
| FR-005, US2/AC2 | `test` | `test_a_short_transfer_list_has_no_reserved_gutter` — green: two rows, `offsetWidth − clientWidth = 0`, row right 23. **A pin**: it passed before the change too, which is what it is for |
| FR-004, SC-004, US2/AC3 | `test` | `test_the_dialog_frame_and_scroll_end_do_not_move` — green: title left 23, `list.top − title.bottom = 14`, heading left 23, and at `scrollTop = scrollHeight` the last row is 23.0px from the dialog's border (22px padding + the rounding) |
| FR-007 (mechanism) | `test` | `test_the_transfer_list_reaches_the_dialog_edges` asserts the computed `overflow: clip` |
| FR-002, SC-001, US1/AC1, US1/AC3 | `inspection` | running worktree server, headed Chromium, fifteen transfers at 1440×760: the thumb paints x 1003–1007 against the border at 1009 (`0px` of canvas; 22px on develop); scrolled to the end the lane's bottom is the dialog's inner border and the thumb's tip is cut by the 12px corner |
| FR-006 | `inspection` | `git diff` on `components.css` adds no `::-webkit-scrollbar*`, `scrollbar-width` or `scrollbar-color` line; the bar photographed is the app's own 5px `--scroll-thumb` bar |
| SC-005, US1/AC4, US2/AC4 | `inspection` | shipped server, three more states: dark 1440×760 — right 1, bottom 1, rows 23/28, bar 5; narrow 420×820 — right 1, bottom 1, rows 23/28, bar 5; two rows — right 1, bottom 1, row right 23, bar 0, no thumb |
| SC-006, Edge — scrolled | `inspection` | the bottom-right corner at the end of the scroll: the bar's pixels stop inside the border's curve; before the clip the thumb ran through it (research D005) |
| Edge — one row / rail-opened / closed / keyboard | `inspection` | the two-row probe covers the short path; the rail origin draws no age headings and the same box; the rules add no display, visibility or script change, and the module's keyboard and rail tests are green |

### Where the implementation went beyond the plan

Nowhere. Two rules, five declarations, four tests — the diff is the plan.

### Run

- `manage.py test tests.e2e.test_media_library tests.test_design_tokens` (48 tests, 196s and 235s on
  two runs): **1 failure**, `test_media_entry_has_roomy_spacing_and_wraps_on_narrow_screen`
  (`19.9998779296875 != 12`) — ITEM-156, already carded in Backlog as red on unmodified `develop`, so
  this slice needs no card of its own and adds no red.
- The four new tests: green; the first was red before the rule (`22 != 0`) for the right reason.
- `preview/probe.py` (headed Chromium, four states): `canvas bar → right border` 22 → 0,
  `list bottom inside dialog border box` 23 → 1, `thumb bottom → dialog bottom edge` 24.4 → ~2.4, and
  every content distance equal between the columns.
- The worktree's dev server (`runserver 8832`, the same machine's Postgres): the shipped dialog at
  1440×760 light, 1440×760 dark, 420×820 and two rows reports right 1, bottom 1, rows 23/28.

## Pass 2

Not needed — pass 1 left no actionable gap.

## Accepted gaps

| Gap | Type | Severity | Accepted on |
| --- | --- | --- | --- |
| The corner cuts the thumb's last ~2px, so the painted tip sits 2.4px above the bottom border rather than 0px | `unrequested` | LOW | 2026-10-29 (the alternative — not clipping — paints the bar over the radius; the lane itself reaches the border) |

## Cap reached

Not reached — one pass, one contradiction found and fixed.
