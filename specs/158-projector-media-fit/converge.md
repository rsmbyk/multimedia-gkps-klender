# Convergence: a small image or PDF page fills the stage

**Spec**: `specs/158-projector-media-fit/spec.md`
**Plan**: `specs/158-projector-media-fit/plan.md`
**Pass**: 1 · **Date**: 2026-10-29

## What was checked

Every row of `plan.md`'s traceability table, by the method it declares. The sixteen `test` rows through
the two media modules and the projector module in one run — `manage.py test tests.e2e.test_image_display
tests.e2e.test_pdf_display tests.e2e.test_projector` → **Ran 80 tests, OK** (1266 s, an isolated
`test_gkps158q` database) — and the three `inspection` rows by reading the diff and the measurements
already recorded in `research.md` and `spec.md §UI/UX`.

## Findings

| Row | Checked by | Evidence | Outcome |
| --- | --- | --- | --- |
| FR-001, SC-001, SC-003, SC-006 | `test` | `test_projector_enlarges_a_small_image_to_the_stage`, `test_a_landscape_image_fits_by_its_width`, `test_a_large_image_still_shrinks` — green | matched |
| FR-002, SC-002 | `test` | `test_projector_enlarges_a_pdf_page_to_the_stage` — green: 603×804 from a 300×400 page | matched |
| FR-003, FR-004, FR-005, SC-004, SC-005 | `test` | `test_projector_t_toggles_fit_width_and_height`, `test_projector_t_toggles_the_page_fit_and_keeps_it_across_pages` — green: 1608×804, 1376×1834, 1376×825 on page 2, back to 603×804 on the next entry | matched |
| FR-006 | `test` | the resize inside `test_projector_enlarges_a_small_image_to_the_stage`: 1376×688 → 960×480 | matched |
| FR-007, SC-007 | `test` | `test_shortcut_sheet_lists_the_fit_key` — green (group, label, `T`, and the sheet inside a 1024×768 window) | matched |
| FR-007's height claim | `inspection` | checked by inspection: the sheet measures 1124×677 at 1920×1200 and 1280×720 in the preview and on the page (`research.md` D007, `spec.md §UI/UX`) | matched |
| FR-008 | `inspection` + `test` | checked by inspection: the diff adds no branch to the passage, audio or video paths; the passage `T` and the cue are covered by `tests/e2e/test_projector.py`, green in the same run | matched |
| FR-009, FR-010, SC-008, SC-009 | `test` | `test_projector_pans_the_overflow_by_drag_and_wheel` — green: −200 by drag, clamped at 515, 215 after the wheel, cleared at the fit, wheel inert with no overflow | matched |
| FR-011, SC-010 | `test` | `test_projector_press_without_drag_still_steps` — green: a 2 px press leaves no transform and the click still steps the entry | matched |
| FR-012 | `test` | the same pan case asserts the zone's computed cursor is `grab` while the media overflows | matched |
| US2 AC4 | `inspection` | checked by inspection: the pixel-ratio expression in `media-pdf.js` is untouched by the diff | matched |

**No `missing`, `partial`, `contradicts` or `unrequested` rows.** The implementation stayed inside the
plan's "what is deliberately not done": no cue indicator, no saved fit, no wheel page turn, no second
painter, no change to `preview.js` or the reader's dialog, no new key.

## Two test corrections during Implement (recorded, not silent)

Both were faults in the cases, not in the behaviour, and both were red for the wrong reason before the fix:

1. `test_projector_press_without_drag_still_steps` first clicked the **next** zone on the last entry, where
   `move(1)` has nowhere to go — the case asserted a step that could not happen. It now clicks the
   **previous** zone, and reads the screen index after the press rather than before the page's first
   click.
2. `test_projector_pans_the_overflow_by_drag_and_wheel` asserted the absolute screen index (`'5'`), which
   is 7 because text entries render more than one screen. It now compares the index against itself
   before and after the panning.

## Outcome

**Converged**, pass 1: 19 test rows accounted for by 9 E2E cases inside an 80-test green run, 3
inspection rows read, 0 gaps, no accepted gaps to carry. Ready to Fold.
