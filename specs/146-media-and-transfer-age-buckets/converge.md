# Converge: the Media Library and the transfer history group by age

**Slice**: `specs/146-media-and-transfer-age-buckets` · **Pass 1** · 2026-10-28

Each row of `plan.md`'s traceability table is re-checked by the method it declared: `test` rows by running
them, `inspection` rows by reading the diff and the grep they name. A task's checkbox is not evidence
(`SDD-22`).

## What was checked

| requirement | method | evidence | outcome |
| --- | --- | --- | --- |
| FR-001 list buckets, labels, order | test | `test_the_list_draws_three_age_buckets` | converged |
| FR-002 file edges: 30 days, then the year | test | `test_a_file_buckets_at_its_edges` | converged |
| FR-003 the present day is `Asia/Jakarta` | test | `test_the_present_day_is_the_congregations_day` | converged |
| FR-004 an empty bucket draws nothing | test | `test_a_bucket_with_no_file_draws_no_heading` | converged |
| FR-005 headings only for date sorts; ascending reverses | test | `test_a_size_sort_draws_no_heading`, `test_an_ascending_sort_reverses_the_buckets` | converged |
| FR-006 heading class, `data-bucket`, numbers | test + inspection | `test_the_heading_keeps_its_class_and_carries_the_bucket_key`; a live read of `/media-library/` gives `12px / 700 / 0.84px / 28px 0 6px / rgb(100,99,87)` | converged |
| FR-007 chips empty a bucket, heading hides | test | `test_a_chip_that_empties_a_bucket_hides_its_heading`, `test_the_unused_chip_empties_a_bucket_and_hides_its_heading` | **gap found, fixed** (C1) |
| FR-008 the row is unchanged | inspection | `git diff 05379336 -- static/web/media-library.js`: the `row()` builder, icon, meta, uses, cloud and remove are untouched; the diff is the grouping block and the `todayJakarta` delegation | converged |
| FR-009 the dialog's five buckets, labels, order | test | `test_the_dialog_draws_five_age_buckets` | converged |
| FR-010 dated by start; rolling windows | test | `test_a_transfer_buckets_by_its_start`, `test_a_transfer_buckets_at_its_edges` | converged |
| FR-011 an active row leads its own bucket | test | `test_an_active_transfer_leads_its_own_bucket` | converged |
| FR-012 order inside a bucket | test | `test_rows_inside_a_bucket_keep_their_end_time_order` | converged |
| FR-013 `h3.media-transfers__group`, keys, numbers | test + inspection | `test_the_dialog_heading_is_a_third_level_heading`; live read gives `12px`, first margin `4px` | converged |
| FR-014 the rail draws no headings | test | `test_the_rail_draws_no_bucket_headings` | converged |
| FR-015 the transfer row is unchanged | inspection | same diff: the row's five lines (glyph, name, state, append) are byte-identical, only named `draw` and called from the bucket walk | converged |
| FR-016 one shared rule | inspection | `grep -rn gkpsAgeBuckets static/web/*.js multimedia/web/templates/reading/base.html` → one definition (`age-buckets.js:84`), two callers; the bucket keys appear nowhere else in `static/web/` | converged |
| FR-017 empty states unchanged | test | `test_the_empty_states_are_unchanged` | converged |
| SC-001 … SC-006 | test | the tests named for each row | converged |
| SC-007 nothing else moves | suite | the slice's own suite 18 tests OK; `multimedia.web` 353 tests OK; the three media-library browser tests that touch this area OK | converged at this stage; the full browser suites run at the push step, as the owner's workflow asks |
| UI/UX numbers | inspection | live `/media-library/`: list heading `12px / 700 / 0.84px / 28px 0 6px`, dialog heading `12px`, first `4px`; dialog `580px` at 1440 and `282px` at a 320 window, longest heading fits, the name still ellipsizes, no horizontal page overflow | converged |

## Findings

**C1 — `partial` — FR-007's `Unused` half was unexercised.** The plan pointed FR-007 at one test, which
presses a *type* chip; the requirement names the `Unused` chip as well. The mechanism is shared (`shown` is
narrowed before the grouping), but "the mechanism is the same" is the reasoning that leaves a requirement
unverified. **Fixed:** `test_the_unused_chip_empties_a_bucket_and_hides_its_heading` seeds one file used by
an active service, so the `Unused` chip empties the file's bucket and the heading goes with it; `plan.md`'s
FR-007 row and `tasks.md`'s T007 now name both tests.

**C2 — `none` — the dialog is `282px` wide at a 320px window, not the `288px` the spec's arithmetic
predicts.** `min(580px, calc(100vw - 32px))` is unchanged code; `100vw` includes the window's scrollbar, so
the frame lands six pixels short. Nothing in the requirement depends on the exact figure — the UI/UX line
asks that the longest heading fit and the name still ellipsize, and both hold — so this is recorded, not
changed.

**C3 — `none` — a test that reads one node twice can read `''` for a computed value.** Both surfaces redraw
on the companion's two-second poll, so `getComputedStyle` on a node resolved moments earlier can run against
a detached element. Both heading tests now read tag, class, key, text and computed style in one
`page.evaluate`. Worth knowing for the next slice that touches a polled surface.

## Outcome

No `missing`, no `contradicts`, no `unrequested`. One `partial` (C1), found and closed. The code matches the
traceability table; the slice is Converged and may Fold. Gap C1 was a test gap, not a behaviour gap: the
shipped code already hid the heading under the `Unused` chip, and the new test proves it.
